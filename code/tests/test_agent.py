"""No-network provider, evidence, spending, CLI and end-to-end regression tests."""
import json
import io
import socket
import sys
import tempfile
import unittest
from dataclasses import replace
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal as D
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from test_baseline import DAY, context, event, profile, request
from agent import BuyOrWaitAgent, evaluate_context
from audit import write_trace
from data_loader import load_dataset
from evidence import Claim, choose_claim, resolve_evidence
from evidence_schemas import ExtractedFacts, ImageFact, MessageFact
from forecast import earliest_full_payment, safe_capacity, simulate
from main import build_parser, write_predictions
from models import Candidate, ImageEvidence, Message, Payment, PaymentOption, SpendingChange
from output_validation import validate_row, verify_output_row
from planner import rank, rank_valid_plans, verify_candidate_plans
from providers import (CachedEvidenceProvider, EvidenceSource, EvidenceUnavailable,
                       FakeEvidenceProvider, OpenAIEvidenceProvider, cache_key, source_for)
from reconstruction import reconstruct
from spending import apply_changes, search_changes, validate_changes


def message(identity='m', event_id='e', day=DAY, source='employer'):
    return Message(identity, 'u', None, event_id,
                   datetime.combine(day, datetime.min.time(), timezone.utc), source, 'Synthetic financial evidence')


def message_fact(identity='m', event_id='e', **kwargs):
    values = dict(source_id=identity, related_event_id=event_id, action='amend', new_amount=None,
                  new_currency=None, new_date=None, new_status=None, creates_new_event=False,
                  confidence=1.0, evidence_summary='Synthetic amendment')
    values.update(kwargs)
    return MessageFact(**values)


def facts(*items):
    return ExtractedFacts(images=[i for i in items if isinstance(i, ImageFact)],
                          messages=[i for i in items if isinstance(i, MessageFact)])


def recurring_expenses(count=1, flexible='stoppable'):
    return tuple(replace(event(f'e{stream}_{month}', date(2025, month, 10), '50',
                         description=f'Stream {stream}', category=f'optional{stream}'),
                         flexibility=flexible, minimum_allowed_amount=D('10'))
                 for stream in range(count) for month in (10, 11, 12))


def spending_context(count=1, amount='800', flexible='stoppable'):
    p = replace(profile(), expense_categories_user_is_willing_to_stop=frozenset(f'optional{i}' for i in range(count)),
                expense_categories_user_is_willing_to_reduce=frozenset(f'optional{i}' for i in range(count)))
    return context(events=recurring_expenses(count, flexible), prof=p, req=request(amount))


class OfflineCase(unittest.TestCase):
    def setUp(self):
        self.connect = patch.object(socket.socket, 'connect', side_effect=AssertionError('Network forbidden in tests'))
        self.create = patch('socket.create_connection', side_effect=AssertionError('Network forbidden in tests'))
        self.connect.start()
        self.create.start()
        self.addCleanup(self.connect.stop)
        self.addCleanup(self.create.stop)


class ProviderTests(OfflineCase):
    def test_malformed_cached_amount_remains_unavailable(self):
        source, c = source_for(message()), context([event()])
        with tempfile.TemporaryDirectory() as folder:
            provider = CachedEvidenceProvider(Path(folder), 'fake', FakeEvidenceProvider({'m': facts(message_fact(new_amount='20'))}))
            provider.resolve(source, c)
            path = next(Path(folder).glob('*.json'))
            entry = json.loads(path.read_text())
            entry['facts']['messages'][0]['new_amount'] = 'not a decimal'
            path.write_text(json.dumps(entry))
            with self.assertRaises(EvidenceUnavailable):
                CachedEvidenceProvider(Path(folder), 'fake').resolve(source, c)

    def test_sdk_builds_strict_pydantic_output_schema_offline(self):
        from openai.lib._parsing._responses import type_to_text_format_param
        schema = type_to_text_format_param(ExtractedFacts)
        self.assertEqual(schema['type'], 'json_schema')
        self.assertTrue(schema['strict'])
        self.assertFalse(schema['schema']['additionalProperties'])

    def test_live_gate_prevents_client_creation(self):
        with self.assertRaises(PermissionError):
            OpenAIEvidenceProvider()

    def test_fake_and_offline_miss_do_not_invent_zero(self):
        source = source_for(message())
        with tempfile.TemporaryDirectory() as folder:
            cache = CachedEvidenceProvider(Path(folder), 'model')
            with self.assertRaises(EvidenceUnavailable):
                cache.resolve(source, context())
            self.assertEqual(cache.usage.live_calls, 0)
            self.assertEqual(list(Path(folder).iterdir()), [])

    def test_cache_round_trip_and_all_identity_inputs(self):
        source, c = source_for(message()), context([event()])
        f = facts(message_fact(new_amount='20'))
        with tempfile.TemporaryDirectory() as folder:
            cache = CachedEvidenceProvider(Path(folder), 'fake', FakeEvidenceProvider({'m': f}))
            self.assertEqual(cache.resolve(source, c), f)
            offline = CachedEvidenceProvider(Path(folder), 'fake')
            self.assertEqual(offline.resolve(source, c), f)
            self.assertEqual(offline.usage.cached_resolutions, 1)
            key = cache_key(source, c, 'fake')
            alternatives = [cache_key(replace(source, content=b'changed'), c, 'fake'),
                            cache_key(source, replace(c, events=(replace(c.events[0], amount=D('999')),)), 'fake'),
                            cache_key(source, c, 'another-model'), cache_key(source, c, 'fake', 'another-version')]
            self.assertNotIn(key, alternatives)

    def test_cache_corruption_is_auditable(self):
        source, c = source_for(message()), context()
        with tempfile.TemporaryDirectory() as folder:
            cache = CachedEvidenceProvider(Path(folder), 'm')
            (Path(folder) / f'{cache_key(source, c, "m")}.json').write_text('{broken')
            with self.assertRaises(EvidenceUnavailable):
                cache.resolve(source, c)

    def test_mocked_responses_parse_and_usage(self):
        f = facts(message_fact(new_amount='20'))
        client = Mock()
        client.responses.parse.return_value = SimpleNamespace(output_parsed=f, status='completed',
            usage=SimpleNamespace(input_tokens=100, output_tokens=20))
        with patch.dict('os.environ', {'EVIDENCE_INPUT_COST_PER_MILLION': '1', 'EVIDENCE_OUTPUT_COST_PER_MILLION': '2'}):
            provider = OpenAIEvidenceProvider(live=True, model='mock-model', client=client)
        self.assertEqual(provider.resolve(source_for(message()), context()), f)
        self.assertIs(client.responses.parse.call_args.kwargs['text_format'], ExtractedFacts)
        self.assertFalse(client.responses.parse.call_args.kwargs['store'])
        self.assertEqual(provider.usage.report()['estimated_cost'], '0.00014')

    def test_mocked_refusal_failure_and_secret_redaction(self):
        client = Mock()
        client.responses.parse.side_effect = ValueError('Authorization: Bearer secret-value')
        provider = OpenAIEvidenceProvider(live=True, client=client)
        with self.assertRaises(EvidenceUnavailable) as raised:
            provider.resolve(source_for(message()), context())
        self.assertNotIn('secret-value', str(raised.exception))
        client.responses.parse.side_effect = None
        client.responses.parse.return_value = SimpleNamespace(output_parsed=None, status='incomplete', usage=None)
        with self.assertRaises(EvidenceUnavailable):
            provider.resolve(source_for(message()), context())

    def test_cache_never_contains_image_payload_or_credentials(self):
        image = ImageFact(source_id='im', related_event_id='e', document_type='bill', amount='20', currency='USD',
                          effective_date=DAY, status='pending', direction='debit', confidence=1,
                          evidence_summary='sk-synthetic-secret Bearer hidden data:image/png;base64,YWJj')
        source = EvidenceSource('im', 'image', b'unique-image-bytes', 'e', {})
        with tempfile.TemporaryDirectory() as folder:
            cache = CachedEvidenceProvider(Path(folder), 'fake', FakeEvidenceProvider({'im': facts(image)}))
            cache.resolve(source, context([event()]))
            text = next(Path(folder).glob('*.json')).read_text()
            for secret in ('unique-image-bytes', 'sk-synthetic-secret', 'Bearer hidden', 'base64,YWJj'):
                self.assertNotIn(secret, text)

    def test_cli_only_extraction_accepts_live(self):
        parser = build_parser()
        self.assertFalse(parser.parse_args(['extract-evidence', '--samples']).live)
        self.assertTrue(parser.parse_args(['extract-evidence', '--all', '--live']).live)
        for args in [['predict', '--output', 'output.csv', '--live'], ['evaluate-samples', '--live']]:
            with self.assertRaises(SystemExit), patch('sys.stderr', new_callable=io.StringIO):
                parser.parse_args(args)


class EvidenceTests(OfflineCase):
    def test_same_source_currency_amendment_is_not_an_unresolved_conflict(self):
        c = context([event(day=DAY + timedelta(days=3), status='scheduled')],
                    messages=[message('old', day=DAY-timedelta(days=1)), message('new')])
        provider = FakeEvidenceProvider({'old': facts(message_fact('old', new_currency='EUR')),
                                         'new': facts(message_fact('new', new_currency='USD'))})
        result = resolve_evidence(c, provider)
        self.assertEqual(result.events[0].currency, 'USD')
        self.assertFalse(any(i.code == 'currency_conflict' for i in result.issues))

    def test_lifecycle_does_not_suppress_across_distinct_cash_legs(self):
        from reconstruction import resolve_lifecycle
        pending = event('original', status='pending')
        refund = event('refund', direction='credit', linked_event_id='original')
        new_debit = event('new_debit', linked_event_id='refund')
        self.assertIn(pending, resolve_lifecycle((pending, refund, new_debit)))

    def test_percentage_amendment_is_calculated_with_decimal_outside_provider(self):
        c = context(recurring_expenses(), messages=[message(event_id='e0_12')])
        amendment = message_fact(event_id='e0_12', scope='future_recurrence', percentage_change='12')
        result = evaluate_context(c, {}, FakeEvidenceProvider({'m': facts(amendment)}))
        self.assertEqual([f.amount for f in result.result.reconstruction.flows], [D('-56'), D('-56'), D('-56')])

    def test_recurring_cancellation_and_payday_delay(self):
        history = recurring_expenses()
        c = context(history, messages=[message(event_id='e0_12')])
        cancelled = message_fact(event_id='e0_12', action='cancel', scope='future_recurrence', new_date=date(2026, 2, 1))
        result = evaluate_context(c, {}, FakeEvidenceProvider({'m': facts(cancelled)}))
        self.assertEqual([f.day for f in result.result.reconstruction.flows], [date(2026, 1, 10)])
        delayed = message_fact(event_id='e0_12', action='delay', scope='future_recurrence', new_date=date(2026, 1, 23))
        result = evaluate_context(c, {}, FakeEvidenceProvider({'m': facts(delayed)}))
        self.assertEqual([f.day for f in result.result.reconstruction.flows],
                         [date(2026, 1, 23), date(2026, 2, 23), date(2026, 3, 23)])

    def test_recurring_currency_change_preserves_historical_currency(self):
        c = context(recurring_expenses(), messages=[message(event_id='e0_12')])
        amendment = message_fact(event_id='e0_12', action='amend', scope='future_recurrence',
                                 new_currency='EUR', new_amount='20', new_date=date(2026, 2, 1))
        rates = {(date(2026, m, 10), 'EUR', 'USD'): D('2') for m in (2, 3)}
        result = evaluate_context(c, rates, FakeEvidenceProvider({'m': facts(amendment)}))
        self.assertEqual(result.result.reconstruction.resolved_events[-1].currency, 'USD')
        self.assertEqual([f.amount for f in result.result.reconstruction.flows], [D('-50'), D('-40'), D('-40')])

    def test_amendment_resolves_copy_not_original(self):
        raw = event(day=DAY + timedelta(days=2), status='scheduled')
        c = context([raw], messages=[message()])
        resolution = resolve_evidence(c, FakeEvidenceProvider({'m': facts(message_fact(new_amount='25'))}))
        self.assertEqual(raw.amount, D('100'))
        self.assertEqual(resolution.events[0].amount, D('25'))
        self.assertEqual(resolution.events[0].evidence_ids, ('m',))

    def test_image_fills_missing_amount_and_missing_cache_leaves_none(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'im.png'
            path.write_bytes(b'fake image, never sent')
            image = ImageEvidence('im', 'u', None, 'e', path)
            c = replace(context([event(amount=None, status='pending')]), images=(image,))
            f = ImageFact(source_id='im', related_event_id='e', document_type='bill', amount='125.50', currency='USD',
                          effective_date=DAY, status='pending', direction='debit', confidence=1, evidence_summary='Amount due')
            good = evaluate_context(c, {}, FakeEvidenceProvider({'im': facts(f)}))
            self.assertEqual(good.result.reconstruction.resolved_events[0].amount, D('125.50'))
            self.assertFalse(good.result.reconstruction.blocked)
            missing = evaluate_context(c, {}, FakeEvidenceProvider())
            self.assertIsNone(missing.result.reconstruction.resolved_events[0].amount)
            self.assertTrue(missing.result.reconstruction.blocked)

    def test_cancel_and_settle_cash_states(self):
        for action, direction, expected in [('cancel', 'debit', []), ('settle', 'credit', [D('100')])]:
            c = context([event(day=DAY + timedelta(days=1), status='pending', direction=direction)], messages=[message()])
            result = evaluate_context(c, {}, FakeEvidenceProvider({'m': facts(message_fact(action=action))}))
            self.assertEqual([f.amount for f in result.result.reconstruction.flows], expected)

    def test_conflict_priority_newer_same_source_and_safer(self):
        c = context([event(status='scheduled', day=DAY + timedelta(days=3))],
                    messages=[message('old'), message('new', day=DAY + timedelta(days=1))])
        fake = FakeEvidenceProvider({'old': facts(message_fact('old', new_amount='500')),
                                     'new': facts(message_fact('new', new_amount='30'))})
        self.assertEqual(resolve_evidence(c, fake).events[0].amount, D('30'))
        # An explicit amendment outranks a newer mere confirmation.
        fake.facts['new'] = facts(message_fact('new', action='confirm', new_amount='10'))
        self.assertEqual(resolve_evidence(c, fake).events[0].amount, D('500'))
        stamp = datetime(2026, 1, 1, tzinfo=timezone.utc)
        claims = [Claim('amount', D('20'), 'a', 'bank', stamp, True, False),
                  Claim('amount', D('40'), 'b', 'merchant', stamp, True, False)]
        self.assertEqual(choose_claim(claims, 'debit').value, D('40'))
        self.assertEqual(choose_claim(claims, 'credit').value, D('20'))
        self.assertEqual(choose_claim([replace(claims[0], settled=True), claims[1]], 'debit').value, D('20'))

    def test_reject_cross_user_and_embedded_decision_fields(self):
        c = context([event()], messages=[message()])
        result = resolve_evidence(c, FakeEvidenceProvider({'m': facts(message_fact(event_id='other_user_event', new_amount='0'))}))
        self.assertEqual(result.events[0].amount, D('100'))
        self.assertTrue(result.skipped)
        with self.assertRaises(ValueError):
            ExtractedFacts.model_validate({'images': [], 'messages': [], 'affordability_status': 'affordable_now'})

    def test_user_level_fact_links_and_new_event(self):
        c = context([event()], messages=[message(event_id=None)])
        f = message_fact(event_id=None, action='create_fact', creates_new_event=True, new_amount='200', new_currency='USD',
                         new_date=DAY + timedelta(days=2), new_status='scheduled', event_description='Confirmed salary',
                         event_category='salary', event_direction='credit', event_type='income')
        result = evaluate_context(c, {}, FakeEvidenceProvider({'m': facts(f)}))
        self.assertTrue(any(flow.amount == D('200') for flow in result.result.reconstruction.flows))

    def test_next_salary_confirmation_preserves_history(self):
        c = context([event(day=DAY - timedelta(days=20), direction='credit', category='salary', description='Payroll credit')],
                    messages=[message()])
        f = message_fact(action='confirm', new_date=DAY + timedelta(days=10), new_amount='500')
        resolution = resolve_evidence(c, FakeEvidenceProvider({'m': facts(f)}))
        self.assertEqual(len(resolution.events), 2)
        self.assertEqual(resolution.events[0], c.events[0])
        self.assertEqual(resolution.events[1].settlement_date, DAY + timedelta(days=10))

    def test_recurring_amendment_applied_before_expansion(self):
        history = recurring_expenses()
        c = context(history, messages=[message(event_id='e0_12')])
        f = message_fact(event_id='e0_12', new_amount='80', new_date=date(2026, 2, 1), scope='future_recurrence')
        result = evaluate_context(c, {}, FakeEvidenceProvider({'m': facts(f)}))
        flows = result.result.reconstruction.flows
        self.assertEqual([f.amount for f in flows], [D('-50'), D('-80'), D('-80')])
        self.assertEqual(flows[1].evidence_ids, ('m',))
        self.assertTrue(all(f.recurrence_reason for f in flows))


class SpendingTests(OfflineCase):
    def test_stoppable_expense_enables_plan_without_changing_baseline(self):
        c = spending_context()
        result = evaluate_context(c, {}, FakeEvidenceProvider())
        self.assertEqual(result.result.decision.status, 'affordable_with_plan')
        self.assertEqual(result.result.decision.safe_amount, D('750'))
        self.assertEqual(result.row['spending_changes_needed'], 'stop:e0_12')
        self.assertTrue(result.result.decision.candidate.change_reasons)

    def test_reduction_floor_and_smallest_sufficient_amount(self):
        c = spending_context(flexible='reducible')
        result = evaluate_context(c, {}, FakeEvidenceProvider())
        change = result.result.decision.candidate.changes[0]
        self.assertEqual(change.action, 'reduce_to')
        self.assertEqual(change.amount, D('33.33'))
        self.assertTrue(validate_changes((replace(change, amount=D('9')),), c, result.result.reconstruction))

    def test_protected_and_fixed_cannot_change(self):
        for c in [spending_context(flexible='fixed'),
                  replace(spending_context(), profile=replace(spending_context().profile, expense_categories_to_protect=frozenset({'optional0'})))]:
            result = evaluate_context(c, {}, FakeEvidenceProvider())
            self.assertIsNone(result.result.decision.candidate)

    def test_three_changes_maximum_and_mutual_exclusion(self):
        c = spending_context(count=4, amount='850')
        result = evaluate_context(c, {}, FakeEvidenceProvider())
        self.assertIsNone(result.result.decision.candidate)  # Needs all four stopped; disallowed.
        changes = tuple(SpendingChange('stop', f'e{i}_12') for i in range(4))
        self.assertIn('maximum three spending changes', validate_changes(changes, c, result.result.reconstruction))
        self.assertTrue(validate_changes((changes[0], SpendingChange('reduce_to', changes[0].event_id, D('10'))), c, result.result.reconstruction))

    def test_search_uses_smallest_cardinality(self):
        c = spending_context(count=2, amount='700')
        result = evaluate_context(c, {}, FakeEvidenceProvider())
        self.assertEqual(len(result.result.decision.candidate.changes), 1)

    def test_no_change_rank_precedes_cheaper_changed_plan(self):
        plain = Candidate('installments', (Payment(DAY, D('110')),), D('110'), 'b')
        changed = Candidate('full_payment', (Payment(DAY, D('100')),), D('100'), 'a', (SpendingChange('stop', 'e'),))
        self.assertLess(rank(plain), rank(changed))


class EndToEndTests(OfflineCase):
    def test_all_four_statuses(self):
        salary = event('salary', DAY + timedelta(days=10), '500', 'scheduled', 'credit',
                       category='salary', event_type='income', description='Next confirmed salary')
        cases = [
            (context(), 'affordable_now'),
            (spending_context(), 'affordable_with_plan'),
            (context([salary], req=replace(request('1000'), allows_partial_payment=False),
                     prof=replace(profile(), payment_methods_user_will_consider=frozenset({'full_payment'}))), 'affordable_later'),
            (context(req=request('2000')), 'not_affordable'),
        ]
        for c, expected in cases:
            result = evaluate_context(c, {}, FakeEvidenceProvider())
            self.assertEqual(result.result.decision.status, expected)
            self.assertEqual(validate_row(result.row, c.request), [])

    def test_inclusive_endpoints_and_safe_maximality(self):
        r, p = request('1000'), profile()
        from models import CashFlow
        flows = [CashFlow(r.horizon, D('-50.005'), 'last_day')]
        amount = safe_capacity(r, p, flows)
        self.assertEqual(amount, D('849.99'))
        self.assertTrue(simulate(r, p, flows, (Payment(DAY, amount),)).safe)
        self.assertFalse(simulate(r, p, flows, (Payment(DAY, amount + D('.01')),)).safe)
        self.assertEqual(len(simulate(r, p, flows).days), 91)

    def test_no_one_time_expense_recurrence(self):
        result = evaluate_context(context([event(day=DAY-timedelta(days=1))]), {}, FakeEvidenceProvider())
        self.assertEqual(result.result.reconstruction.flows, [])

    def test_audit_has_candidate_checks_daily_records_and_sources(self):
        result = evaluate_context(spending_context(), {}, FakeEvidenceProvider())
        self.assertTrue(result.trace['candidates'])
        self.assertEqual(len(result.trace['baseline_daily']), 91)
        self.assertTrue(all(c['ranking_key'] is None for c in result.trace['candidates'] if not c['valid']))
        with tempfile.TemporaryDirectory() as folder:
            js, md = write_trace(result.trace, Path(folder))
            self.assertIn('selected', json.loads(js.read_text()))
            self.assertIn('Daily selected forecast', md.read_text())

    def test_output_rejects_invalid_status_and_partial_plan(self):
        c = context()
        result = evaluate_context(c, {}, FakeEvidenceProvider())
        bad = dict(result.row, affordability_status='not_affordable')
        self.assertTrue(validate_row(bad, c.request))
        bad = dict(result.row, recommended_payment_method='partial_payment', affordability_status='affordable_with_plan')
        self.assertTrue(validate_row(bad, c.request))

    def test_prediction_writer_dataset_guard_and_synthetic_output(self):
        data = load_dataset()
        p, r = profile(), request()
        data.profiles = {'u': p}
        data.events = {}
        data.requests = (r,)
        data.options = ()
        data.messages = ()
        data.images = ()
        agent = BuyOrWaitAgent(data, FakeEvidenceProvider())
        with self.assertRaises(ValueError):
            write_predictions(agent, Path('dataset/output.csv'))
        with tempfile.TemporaryDirectory() as folder, patch('main.write_trace'), patch('main.write_usage'):
            output = Path(folder) / 'synthetic.csv'
            self.assertEqual(write_predictions(agent, output), 1)
            self.assertEqual(len(output.read_text().splitlines()), 2)
            self.assertEqual(verify_output_row(agent.evaluate(r).row, r, agent), [])


if __name__ == '__main__':
    unittest.main()

"""Synthetic financial scenarios and label-free sample invariant checks."""
import sys
import unittest
from dataclasses import fields, replace
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal as D
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from data_loader import OUTPUT_FIELDS, convert, load_dataset, parse_request
from forecast import earliest_full_payment, safe_capacity, simulate
from formatter import format_decision, format_plan
from models import (Candidate, CashFlow, Event, Message, Payment, PaymentOption,
                    Profile, Reconstruction, Request, RequestContext)
from planner import predict, rank, validate_candidate
from reconstruction import add_months, reconstruct, resolve_lifecycle
from spending import apply_changes

DAY = date(2026, 1, 5)


def profile(balance: str = '1000', minimum: str = '100') -> Profile:
    return Profile('u', 'USD', D(balance), D(minimum), frozenset(), frozenset({'rent'}),
                   frozenset(), frozenset(), frozenset({'full_payment', 'partial_payment', 'installments'}), 6)


def request(amount: str = '400', deadline: int = 80) -> Request:
    return Request('r', 'u', DAY, 'purchase', D(amount), DAY + timedelta(days=deadline), True, 'Buy something')


def event(identity: str = 'e', day: date = DAY, amount: str | None = '100',
          status: str = 'settled', direction: str = 'debit', **kwargs) -> Event:
    return Event(identity, 'u', kwargs.get('event_type', 'expense'), kwargs.get('description', 'Monthly bill'),
                 kwargs.get('category', 'rent'), direction, D(amount) if amount is not None else None,
                 kwargs.get('currency', 'USD'), day, day, status, kwargs.get('linked_event_id'), 'fixed', None)


def context(events=(), req=None, prof=None, options=(), messages=()) -> RequestContext:
    return RequestContext(req or request(), prof or profile(), tuple(events), tuple(options), tuple(messages), ())


class LoadingTests(unittest.TestCase):
    def test_decimal_directional_dated_fx(self):
        rates = {(DAY, 'EUR', 'USD'): D('1.09')}
        self.assertEqual(convert(D('0.10'), 'EUR', 'USD', DAY, rates), D('0.109'))
        self.assertEqual(convert(D('9.123'), 'USD', 'USD', DAY, {}), D('9.123'))
        for source, target, day in [('USD', 'EUR', DAY), ('EUR', 'USD', DAY + timedelta(days=1))]:
            with self.assertRaises(ValueError):
                convert(D('10'), source, target, day, rates)

    def test_input_cannot_carry_labels(self):
        row = dict(request_id='r', user_id='u', request_date='2026-01-05', request_type='purchase',
                   requested_amount='400', desired_completion_date='2026-03-01', allows_partial_payment='true',
                   request_text='Example', amount_safe_to_pay='999999', affordability_status='malicious')
        first = parse_request(row)
        row.update(amount_safe_to_pay='0', affordability_status='different')
        self.assertEqual(first, parse_request(row))
        self.assertNotIn('amount_safe_to_pay', {f.name for f in fields(Request)})

    def test_data_and_context_types_and_cutoff(self):
        data = load_dataset()
        self.assertEqual(len(data.samples), 25)
        self.assertEqual(len(data.requests), 250)
        c = data.context(data.samples[0])
        self.assertIsInstance(c.profile.current_available_balance, D)
        self.assertIsInstance(c.events[0].settlement_date, date)
        future = Message('future', c.request.user_id, None, None,
                         datetime(2099, 1, 1, tzinfo=timezone.utc), 'bank', 'Unusable future evidence')
        shared = replace(future, message_id='shared', sent_at=datetime(2000, 1, 1, tzinfo=timezone.utc))
        unrelated = replace(shared, message_id='other', user_id='someone_else')
        wrong_request = replace(shared, message_id='wrong', request_id='different')
        linked = replace(shared, message_id='linked', related_event_id=c.events[0].event_id)
        data.messages = (future, shared, unrelated, wrong_request, linked)
        self.assertEqual({m.message_id for m in data.context(c.request).messages}, {'shared', 'linked'})
        self.assertTrue(all(r.amount_safe_to_pay is None for r in data.output_template))


class ReconstructionTests(unittest.TestCase):
    def test_transitive_replacement_cancellation_and_cycle(self):
        auth = event('auth', status='pending')
        queued = event('queued', status='scheduled', linked_event_id='auth')
        settled = event('settled', linked_event_id='queued')
        self.assertEqual(resolve_lifecycle((auth, queued, settled)), (settled,))
        cancellation = replace(settled, status='cancelled')
        self.assertEqual(resolve_lifecycle((auth, queued, cancellation)), ())
        with self.assertRaises(ValueError):
            resolve_lifecycle((replace(auth, linked_event_id='queued'), queued))

    def test_snapshot_and_pending_cash_states(self):
        events = [event('historical'), event('pending', DAY + timedelta(days=5), status='pending'),
                  event('pending_credit', status='pending', direction='credit'),
                  event('failed', status='failed'), event('cancelled', status='cancelled'),
                  event('valuation', status='unrealized', direction='non_cash')]
        state = reconstruct(context(events), {})
        self.assertEqual([(f.day, f.amount, f.source_id) for f in state.flows], [(DAY, D('-100'), 'pending')])
        self.assertEqual(state.flows[0].direction, 'debit')

    def test_pending_reservation_once_even_beyond_forecast(self):
        state = reconstruct(context([event('pending', DAY + timedelta(days=120), status='pending')]), {})
        self.assertEqual(sum((f.amount for f in state.flows), D('0')), D('-100'))
        self.assertEqual(state.flows[0].day, DAY)

    def test_settled_replaces_authorization_but_refund_is_distinct(self):
        pending = event('auth', status='pending')
        settled = event('settled', DAY + timedelta(days=2), linked_event_id='auth')
        refund = event('refund', DAY + timedelta(days=3), direction='credit', linked_event_id='settled', event_type='refund')
        state = reconstruct(context([pending, settled, refund]), {})
        self.assertEqual([(f.source_id, f.amount) for f in state.flows], [('settled', D('-100')), ('refund', D('100'))])
        disputed = event('disputed', status='pending', linked_event_id='settled', description='Possible duplicate charge')
        self.assertIn(disputed, resolve_lifecycle((settled, disputed)))

    def test_failed_retry_counted_once(self):
        state = reconstruct(context([event('failed', status='failed'),
                                     event('retry', DAY + timedelta(days=1), status='scheduled', linked_event_id='failed')]), {})
        self.assertEqual(len(state.flows), 1)
        self.assertEqual(state.flows[0].source_id, 'retry')

    def test_missing_active_debit_blocks_and_history_not_zero(self):
        c = context([event('unknown', DAY + timedelta(days=1), None, 'pending')])
        result = predict(c, {})
        self.assertTrue(result.reconstruction.blocked)
        self.assertEqual(result.decision.safe_amount, D('0'))
        self.assertEqual(result.decision.method, 'not_recommended')
        state = reconstruct(context([event('old_unknown', DAY - timedelta(days=1), None)]), {})
        self.assertFalse(state.blocked)
        self.assertTrue(any(i.code == 'missing_historical_amount' for i in state.issues))

    def test_three_monthly_observations_and_latest_contractual_debit(self):
        events = [event(str(i), date(2025, month, 10), amount) for i, (month, amount) in
                  enumerate([(10, '100'), (11, '120'), (12, '90')])]
        state = reconstruct(context(events), {})
        self.assertEqual([f.day for f in state.flows], [date(2026, 1, 10), date(2026, 2, 10), date(2026, 3, 10)])
        self.assertEqual({f.amount for f in state.flows}, {D('-90')})
        self.assertEqual(reconstruct(context(events[:2]), {}).flows, [])

    def test_category_recurrence_across_merchants(self):
        events = [event(str(i), DAY - timedelta(days=21 - 7*i), str(20 + i),
                        category='groceries', description=f'Merchant {i}') for i in range(3)]
        state = reconstruct(context(events), {})
        self.assertTrue(state.flows)
        self.assertEqual(state.flows[0].day, DAY)
        self.assertEqual(state.flows[0].amount, D('-21'))

    def test_salary_one_offs_and_confirmed_override(self):
        history = [event(str(m), date(2025, m, 15), '500', direction='credit',
                         event_type='income', category='salary', description='Payroll credit') for m in (10, 11, 12)]
        scheduled = event('next', date(2026, 1, 20), '600', 'scheduled', 'credit',
                          event_type='income', category='salary', description='Next confirmed salary')
        state = reconstruct(context(history + [scheduled]), {})
        january = [f for f in state.flows if f.day.month == 1]
        self.assertEqual([(f.day, f.amount, f.source_id) for f in january], [(date(2026, 1, 20), D('600'), 'next')])
        bonuses = [replace(e, description='Performance commission') for e in history]
        self.assertEqual(reconstruct(context(bonuses), {}).flows, [])

    def test_missing_future_fx_omits_credit_but_blocks_unknown_debit(self):
        credit = event('fx', DAY + timedelta(days=1), '100', 'scheduled', 'credit',
                       currency='EUR', category='salary', description='Next confirmed salary')
        state = reconstruct(context([credit]), {})
        self.assertFalse(state.blocked)
        self.assertTrue(any(i.code == 'missing_fx' for i in state.issues))
        self.assertEqual(state.flows, [])
        state = reconstruct(context([replace(credit, direction='debit')]), {})
        self.assertTrue(state.blocked)

    def test_calendar_anchor(self):
        self.assertEqual(add_months(date(2024, 1, 31), 1), date(2024, 2, 29))
        self.assertEqual(add_months(date(2024, 1, 31), 2), date(2024, 3, 31))


class ForecastPlannerTests(unittest.TestCase):
    def test_capacity_monotonicity_under_expenses_and_reserve(self):
        for amount in ('0', '0.01', '100', '899.99', '1000'):
            flows = [CashFlow(DAY + timedelta(days=20), -D(amount), 'bill')]
            cap = safe_capacity(request('1000'), profile(), flows)
            larger_bill = [replace(flows[0], amount=flows[0].amount - D('1'))]
            self.assertLessEqual(safe_capacity(request('1000'), profile(), larger_bill), cap)
            self.assertLessEqual(safe_capacity(request('1000'), profile(minimum='101'), flows), cap)

    def test_predict_installments_when_full_capacity_but_no_full_preference(self):
        option = PaymentOption('offer', 'r', 'installments', D('140'), 3, DAY, 31, D('20'), D('420'))
        c = context(options=[option], prof=replace(profile(), payment_methods_user_will_consider=frozenset({'installments'})))
        result = predict(c, {})
        self.assertEqual(result.decision.method, 'installments')
        self.assertEqual(result.decision.safe_amount, D('400'))
        self.assertEqual(result.decision.earliest, DAY)
        self.assertEqual(result.decision.payments, option.payments())

    def test_installment_rounding_preserves_supplied_amount(self):
        option = PaymentOption('rounded', 'r', 'installments', D('133.34'), 3, DAY, 28, D('0.02'), D('400.02'))
        c = context(options=[option])
        candidate = Candidate('installments', option.payments(), D('400.02'), 'rounded')
        self.assertEqual(validate_candidate(candidate, c, Reconstruction(), D('400'), DAY), [])
        inconsistent = replace(option, payment_amount=D('133.30'))
        self.assertTrue(validate_candidate(replace(candidate, payments=inconsistent.payments()),
                                          replace(c, options=(inconsistent,)), Reconstruction(), D('400'), DAY))

    def test_wait_requires_full_payment_preference(self):
        future = DAY + timedelta(days=2)
        state = Reconstruction(flows=[CashFlow(future, D('200'), 'salary')])
        c = context(req=request('1000'), prof=replace(profile(), payment_methods_user_will_consider=frozenset({'partial_payment'})))
        candidate = Candidate('wait', (Payment(future, D('1000')),), D('1000'))
        self.assertIn('payment method excluded by user', validate_candidate(candidate, c, state, D('900'), future))

    def test_future_trough_limits_capacity_and_decimal_floor(self):
        r, p = request('1000'), profile()
        flows = [CashFlow(DAY + timedelta(days=3), D('-333.333'), 'bill')]
        self.assertEqual(safe_capacity(r, p, flows), D('566.66'))
        self.assertTrue(simulate(r, p, flows, (Payment(DAY, D('566.66')),)).safe)
        self.assertFalse(simulate(r, p, flows, (Payment(DAY, D('566.67')),)).safe)

    def test_same_day_debit_before_credit_and_earlier_breach(self):
        flows = [CashFlow(DAY + timedelta(days=1), D('-950'), 'bill'),
                 CashFlow(DAY + timedelta(days=1), D('2000'), 'salary')]
        self.assertFalse(simulate(request(), profile(), flows).safe)
        self.assertIsNone(earliest_full_payment(request(), profile(), flows))

    def test_partial_and_wait_validation(self):
        c = context(req=request('1000'))
        state = Reconstruction(flows=[CashFlow(DAY + timedelta(days=10), D('500'), 'salary')])
        safe = safe_capacity(c.request, c.profile, state.flows)
        earliest = earliest_full_payment(c.request, c.profile, state.flows)
        self.assertEqual(safe, D('900'))
        self.assertEqual(earliest, DAY + timedelta(days=10))
        good = Candidate('partial_payment', (Payment(DAY, safe), Payment(earliest, D('100'))), D('1000'))
        self.assertEqual(validate_candidate(good, c, state, safe, earliest), [])
        for bad in [replace(good, payments=good.payments[::-1]),
                    replace(good, payments=(Payment(DAY, D('800')), Payment(earliest, D('200')))),
                    replace(good, payments=good.payments + (Payment(earliest, D('1')),))]:
            self.assertTrue(validate_candidate(bad, c, state, safe, earliest))
        self.assertTrue(validate_candidate(good, replace(c, request=replace(c.request, allows_partial_payment=False)), state, safe, earliest))

    def test_supplied_installments_schedule_fee_limit_and_deadline(self):
        option = PaymentOption('offer', 'r', 'installments', D('140'), 3, DAY, 31, D('20'), D('420'))
        c = context(options=[option])
        good = Candidate('installments', option.payments(), D('420'), 'offer')
        self.assertEqual(good.payments[1].day, DAY + timedelta(days=31))
        self.assertEqual(validate_candidate(good, c, Reconstruction(), D('400'), DAY), [])
        for bad in [replace(good, option_id='invented'), replace(good, total_cost=D('400')),
                    replace(good, payments=(Payment(DAY, D('141')), *good.payments[1:]))]:
            self.assertTrue(validate_candidate(bad, c, Reconstruction(), D('400'), DAY))
        for prof in [replace(c.profile, max_installment_months=None), replace(c.profile, max_installment_months=2)]:
            self.assertTrue(validate_candidate(good, replace(c, profile=prof), Reconstruction(), D('400'), DAY))
        self.assertTrue(validate_candidate(good, replace(c, request=request(deadline=30)), Reconstruction(), D('400'), DAY))

    def test_preferences_and_ranking(self):
        c = context(prof=replace(profile(), payment_methods_user_will_consider=frozenset({'installments'})))
        candidate = Candidate('full_payment', (Payment(DAY, D('400')),), D('400'))
        self.assertTrue(validate_candidate(candidate, c, Reconstruction(), D('400'), DAY))
        cheap_later = Candidate('wait', (Payment(DAY + timedelta(days=10), D('400')),), D('400'))
        costly_now = Candidate('installments', (Payment(DAY, D('410')),), D('410'))
        self.assertLess(rank(cheap_later), rank(costly_now))
        self.assertLess(rank(candidate), rank(cheap_later))
        self.assertLess(rank(replace(candidate, option_id='offer_01')), rank(replace(candidate, option_id='offer_02')))

    def test_formatter_exact_columns_and_no_scientific_notation(self):
        result = predict(context(), {})
        formatted = format_decision(result.decision)
        self.assertEqual(tuple(formatted), OUTPUT_FIELDS)
        self.assertEqual(format_plan((Payment(DAY, D('1E+6')),)), '2026-01-05:1000000')

    def test_all_samples_label_free_invariants(self):
        data = load_dataset()
        for req in data.samples:
            with self.subTest(request=req.request_id):
                c = data.context(req)
                result = predict(c, data.rates)
                d = result.decision
                self.assertLessEqual(D('0'), d.safe_amount)
                self.assertLessEqual(d.safe_amount, req.requested_amount)
                if d.candidate:
                    self.assertEqual(validate_candidate(d.candidate, c, result.reconstruction, d.safe_amount, d.earliest), [])
                    self.assertTrue(simulate(req, c.profile, apply_changes(result.reconstruction.flows, d.candidate.changes), d.payments).safe)
                    self.assertLessEqual(d.payments[-1].day, req.desired_completion_date)
                if d.status == 'affordable_now':
                    self.assertEqual(d.earliest, req.request_date)


if __name__ == '__main__':
    unittest.main()

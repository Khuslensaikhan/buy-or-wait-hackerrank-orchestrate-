"""Extraction control-flow tests: all evidence responses and network clients are fake."""
import io
import json
import tempfile
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from test_agent import OfflineCase, facts, message
from test_baseline import context
from extraction import collect_evidence, dry_run_summary, run_extraction
from main import build_parser, main
from models import ImageEvidence
from providers import (CachedEvidenceProvider, EvidenceUnavailable, OpenAIEvidenceProvider,
                       Usage, atomic_json_write, source_for)


class ExtractionTests(OfflineCase):
    def setUp(self):
        super().setUp()
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.context = replace(context(), messages=(message('m1'), message('m2'), message('m3')))
        self.fallback = Mock(usage=Usage('fake', 'fake'))
        self.fallback.resolve.return_value = facts()
        self.cache = CachedEvidenceProvider(self.folder / 'cache', 'fake', self.fallback)

    def run_items(self, items=None):
        with patch('builtins.print') as output:
            self.output = output
            report = run_extraction(items if items is not None else collect_evidence([self.context]),
                                    self.cache, self.folder / 'audit')
        self.output = output
        return report

    def test_global_deduplication_messages_and_images(self):
        image_path = self.folder / 'image.png'
        image_path.write_bytes(b'fake image')
        image = ImageEvidence('i1', 'u', None, None, image_path)
        c = replace(self.context, images=(image,))
        other = replace(c, request=replace(c.request, request_id='other'))
        items = collect_evidence([c, other, c])
        self.assertEqual([i.source_id for i in items], ['i1', 'm1', 'm2', 'm3'])
        self.run_items(items)
        self.assertEqual(self.fallback.resolve.call_count, 4)
        self.assertEqual(items[0].request_ids, [c.request.request_id, 'other'])

    def test_immediate_persistence_before_next_call_and_progress_flushed(self):
        def resolve(source, c):
            calls = self.fallback.resolve.call_count
            self.assertIn(f'START message {source.source_id}', self.output.call_args.args[0])
            self.assertTrue(self.output.call_args.kwargs['flush'])
            self.assertEqual(len(list(self.cache.cache_dir.glob('*.json'))), calls - 1)
            self.cache.usage.input_tokens += 10
            self.cache.usage.output_tokens += 2
            return facts()
        self.fallback.resolve.side_effect = resolve
        report = self.run_items()
        self.assertEqual(report['summary']['completed'], 3)
        printed = [call.args[0] for call in self.output.call_args_list]
        self.assertTrue(printed[0].startswith('[1/3] START message m1'))
        self.assertTrue(printed[1].startswith('[1/3] DONE m1'))
        self.assertTrue(printed[1].endswith(' 10 2'))
        self.assertTrue(all(call.kwargs.get('flush') for call in self.output.call_args_list))

    def test_timeout_continues_and_failure_has_no_facts(self):
        self.fallback.resolve.side_effect = [TimeoutError('sk-do-not-print'), facts(), facts()]
        report = self.run_items()
        self.assertEqual(report['summary']['failed'], 1)
        self.assertEqual(report['summary']['completed'], 2)
        self.assertEqual(report['sources'][0]['error_type'], 'TimeoutError')
        self.assertNotIn('facts', report['sources'][0])
        self.assertNotIn('sk-do-not-print', json.dumps(report))
        self.assertEqual(len(list(self.cache.cache_dir.glob('*.json'))), 2)
        audit = json.loads((self.folder / 'audit/evidence_extraction.json').read_text())
        self.assertEqual(audit['sources'][0]['status'], 'ERROR')

    def test_limit_after_deduplication_includes_cached_items(self):
        self.cache.resolve(source_for(message('m1')), self.context)
        self.fallback.reset_mock()
        report = self.run_items(collect_evidence([self.context, self.context], limit=2))
        self.assertEqual(report['summary']['selected'], 2)
        self.assertEqual(report['summary']['cached'], 1)
        self.assertEqual(self.fallback.resolve.call_count, 1)
        self.assertEqual(collect_evidence([self.context], limit=0), [])

    def test_source_id_selection(self):
        self.run_items(collect_evidence([self.context], source_id='m2', limit=1))
        self.assertEqual(self.fallback.resolve.call_args.args[0].source_id, 'm2')
        self.fallback.resolve.assert_called_once()
        with self.assertRaises(ValueError):
            collect_evidence([self.context], source_id='absent')

    def test_dry_run_never_calls_fallback_or_writes(self):
        self.cache.resolve(source_for(message('m1')), self.context)
        self.fallback.reset_mock()
        before = {p: p.read_bytes() for p in self.folder.rglob('*') if p.is_file()}
        result = dry_run_summary(collect_evidence([self.context]), self.cache)
        self.assertEqual((result['unique_messages'], result['unique_images']), (3, 0))
        self.assertEqual(result['already_cached'], 1)
        self.assertEqual(result['requiring_live_calls'], 2)
        self.assertEqual(result['estimated_call_count'], 2)
        self.assertEqual(result['evidence_ids_in_processing_order'], ['m1', 'm2', 'm3'])
        self.fallback.resolve.assert_not_called()
        self.assertEqual(before, {p: p.read_bytes() for p in self.folder.rglob('*') if p.is_file()})

    def test_cli_live_dry_run_never_constructs_live_provider(self):
        dataset = SimpleNamespace(samples=[self.context.request], requests=[], context=lambda r: self.context)
        with patch('main.load_dataset', return_value=dataset), patch('main.OpenAIEvidenceProvider') as live, \
             patch('main.CachedEvidenceProvider', return_value=self.cache), patch('builtins.print'):
            self.assertEqual(main(['extract-evidence', '--all', '--live', '--dry-run']), 0)
        live.assert_not_called()
        self.fallback.resolve.assert_not_called()

    def test_ctrl_c_preserves_completed_entries_and_can_resume(self):
        self.fallback.resolve.side_effect = [facts(), KeyboardInterrupt()]
        report = self.run_items()
        self.assertTrue(report['summary']['interrupted'])
        self.assertEqual(report['summary']['completed'], 1)
        self.assertEqual(report['sources'][1]['status'], 'INTERRUPTED')
        saved = {p: p.read_bytes() for p in self.cache.cache_dir.glob('*.json')}
        self.assertEqual(len(saved), 1)
        self.fallback.resolve.side_effect = None
        report = self.run_items()
        self.assertEqual(report['summary']['cached'], 1)
        self.assertEqual(report['summary']['completed'], 2)
        for p, content in saved.items():
            self.assertEqual(p.read_bytes(), content)
            json.loads(content)
        self.assertTrue(any('CACHE_HIT m1' in call.args[0] for call in self.output.call_args_list))

    def test_interrupted_atomic_commit_and_existing_partial_are_preserved(self):
        target = self.folder / 'entry.json'
        partial = self.folder / 'entry.tmp'
        partial.write_bytes(b'{old interrupted data')
        with patch('providers.os.fsync', side_effect=[KeyboardInterrupt(), None]):
            with self.assertRaises(KeyboardInterrupt):
                atomic_json_write(target, {'complete': True})
        self.assertEqual(json.loads(target.read_text()), {'complete': True})
        self.assertEqual(partial.read_bytes(), b'{old interrupted data')

    def test_sdk_options_reasoning_and_typed_errors(self):
        import httpx
        from openai import APITimeoutError, APIConnectionError, RateLimitError
        request = httpx.Request('POST', 'https://example.invalid')
        errors = [APITimeoutError(request=request), APIConnectionError(request=request),
                  RateLimitError('secret', response=httpx.Response(429, request=request), body=None),
                  ValueError('sensitive malformed output')]
        client = Mock()
        client.responses.parse.side_effect = errors
        with patch('openai.OpenAI', return_value=client) as constructor:
            provider = OpenAIEvidenceProvider(live=True, model='fake', timeout_seconds=12, max_retries=2)
            for category in ('APITimeoutError', 'APIConnectionError', 'RateLimitError', 'StructuredOutputError'):
                with self.assertRaises(EvidenceUnavailable) as caught:
                    provider.resolve(source_for(message()), self.context)
                self.assertEqual(caught.exception.error_type, category)
                self.assertNotIn('secret', str(caught.exception))
        constructor.assert_called_once_with(timeout=12, max_retries=2)
        self.assertEqual(client.responses.parse.call_args.kwargs['reasoning'], {'effort': 'none'})
        self.assertEqual(provider.usage.unmetered_calls, 4)

    def test_cli_defaults_and_invalid_limits(self):
        args = build_parser().parse_args(['extract-evidence', '--all'])
        self.assertEqual((args.timeout_seconds, args.max_retries), (60, 1))
        for option, value in [('--limit', '-1'), ('--max-retries', '-1'), ('--timeout-seconds', '0'),
                              ('--timeout-seconds', 'nan')]:
            with self.subTest(option=option, value=value), patch('sys.stderr', new=io.StringIO()):
                with self.assertRaises(SystemExit):
                    build_parser().parse_args(['extract-evidence', '--all', option, value])

    def test_cli_interruption_exit_code_and_audit(self):
        dataset = SimpleNamespace(samples=[self.context.request], requests=[], context=lambda r: self.context)
        self.fallback.resolve.side_effect = KeyboardInterrupt()
        with patch('main.load_dataset', return_value=dataset), patch('main.REPO_ROOT', self.folder), \
             patch('main.CachedEvidenceProvider', return_value=self.cache), \
             patch('main.OpenAIEvidenceProvider', return_value=self.fallback), patch('builtins.print'):
            self.assertEqual(main(['extract-evidence', '--samples', '--live']), 130)
        report = json.loads((self.folder / 'code/evaluation/evidence_extraction.json').read_text())
        self.assertTrue(report['summary']['interrupted'])

    def test_corrupt_cache_is_reported_and_never_replaced(self):
        self.cache.resolve(source_for(message('m1')), self.context)
        path = next(self.cache.cache_dir.glob('*.json'))
        path.write_bytes(b'{partial JSON')
        self.fallback.reset_mock()
        item = collect_evidence([self.context], source_id='m1')
        summary = dry_run_summary(item, self.cache)
        self.assertEqual(summary['estimated_call_count'], 0)
        self.assertEqual(len(summary['unavailable_sources']), 1)
        report = self.run_items(item)
        self.assertEqual(report['summary']['failed'], 1)
        self.fallback.resolve.assert_not_called()
        self.assertEqual(path.read_bytes(), b'{partial JSON')

    def test_all_sdk_failures_continue_to_success(self):
        import httpx
        from openai import APITimeoutError, APIConnectionError, RateLimitError
        request = httpx.Request('POST', 'https://example.invalid')
        client = Mock()
        client.responses.parse.side_effect = [APITimeoutError(request=request),
            RateLimitError('private body', response=httpx.Response(429, request=request), body=None),
            APIConnectionError(request=request), ValueError('invalid structured output'),
            SimpleNamespace(output_parsed=facts(), status='completed', usage=None)]
        self.cache.fallback = OpenAIEvidenceProvider(live=True, model='fake', client=client)
        self.cache.usage = self.cache.fallback.usage
        c = replace(self.context, messages=tuple(message(f'm{i}') for i in range(5)))
        report = self.run_items(collect_evidence([c]))
        self.assertEqual(report['summary']['failed'], 4)
        self.assertEqual(report['summary']['completed'], 1)
        self.assertEqual(len(list(self.cache.cache_dir.glob('*.json'))), 1)

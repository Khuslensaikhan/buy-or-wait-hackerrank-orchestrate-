# Complete-agent implementation findings

No live OpenAI calls were made. The evidence cache was empty during the sample run. No root output.csv was generated and dataset files were unchanged.

## Architecture

Input Request -> Retrieve Context -> Reconstruct Financial Reality -> Build 90-Day Baseline -> Generate Payment Candidates -> Verify and Rank -> Produce output row/CSV.

The BuyOrWaitAgent preserves typed loading, Decimal arithmetic and baseline simulation, adding immutable evidence amendments, fake/cached/live providers, auditable flow provenance, a daily ledger, permitted spending-change search, candidate check results, deterministic explanations and CLI audit/validation commands.

## Verification

**60 tests passed** in the final run (7.364 seconds).

Python 3.12 unit and integration tests use fake evidence or a mocked Responses client. The installed SDK also builds the strict Pydantic response schema without making a request. The trace command and cache-only extraction command were exercised; the prediction writer was tested on synthetic data in a temporary directory only.

## Sample accuracy

All 25 requests evaluated before labels were loaded. No monetary tolerance; normalization only parses equivalent Decimal and schedule spellings. Explanation equality is lexical, not semantic.

| Field | Normalized | Exact text |
|---|---:|---:|
| request_id | 25/25 (100%) | 25/25 (100%) |
| amount_safe_to_pay | 0/25 (0%) | 0/25 (0%) |
| affordability_status | 12/25 (48%) | 12/25 (48%) |
| recommended_payment_method | 14/25 (56%) | 14/25 (56%) |
| payment_plan | 13/25 (52%) | 11/25 (44%) |
| earliest_date_for_full_payment | 11/25 (44%) | 11/25 (44%) |
| spending_changes_needed | 19/25 (76%) | 19/25 (76%) |
| decision_explanation | 0/25 (0%) | 0/25 (0%) |

Request accuracy is 0/25 with or without explanation. Compared with Phase 1, status accuracy rose from 40% to 48%, method from 44% to 56%, and normalized plans from 40% to 52%. Spending-change equality fell from 88% to 76% because the inaccurate forecast sometimes requires changes where samples do not.

## Remaining mismatches

* Safe amounts mismatch all 25 samples; recurring spending estimation and supported income continuation remain the main baseline limitations. Sample 21 overestimates safe capacity, demonstrating that conservative heuristics alone do not establish correct reconstruction.
* All 17 sample messages and five sample images remain unresolved offline. Samples 16 and 20 have missing active debit amounts and cannot certify payment capacity. Other evidence affects salary amounts, payday changes, rent amendments and historical expense estimation.
* Samples 04, 11, 17 and 23 now obtain plans using spending changes, but those changes do not match the sample recommendations. Implemented search mechanics do not fix errors in the baseline forecast.
* Exact explanations mismatch every sample; deterministic explanations are grounded in the implemented trace, not copied from expected strings.
* See sample_results.md for every mismatched field and expected/predicted values. Each sample has a full JSON and Markdown trace under traces/.

## Commands

Activate the repository environment with `source .venv/bin/activate`.

```sh
python3.12 -m unittest discover -s code/tests -v
python3.12 code/main.py evaluate-samples
python3.12 code/main.py trace --sample request_16
```

Future one-time live evidence extraction (not run during implementation):

```sh
python3.12 code/main.py extract-evidence --all --live
```

This command extracts all sample and evaluation evidence and populates the cache; it does not write predictions. Matching cache entries are reused on reruns. Model and cost rates come from environment configuration; unknown rates/usage are reported as unknown, never fabricated.

After inspecting and validating the extracted evidence, rerun sample evaluation before authorizing final prediction generation. The current low accuracy is explicit and unresolved.

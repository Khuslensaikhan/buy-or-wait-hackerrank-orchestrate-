# Financial model verification

`output.csv` at the repository root contains all 250 evaluation requests in input order, with the exact eight required columns. `dataset/` is unchanged. The prediction engine does not read sample labels or organizer-only files.

Validation: 88 offline tests passed; `validate-output output.csv` re-evaluated all 250 rows successfully. Every one of the 136 selected payment plans also passed an independent scan of the saved daily traces for the minimum-balance rule. This verifies consistency with the implemented forecast, not hidden-answer accuracy.

Output SHA-256: `7bf59bc60ab11fcaf2b82184c20e0e141c3c9cbe8f80f266683c7380c3ebc1dc`.

## Sample results

| Metric | Baseline | Final |
|---|---:|---:|
| amount_safe_to_pay | 0/25 | 2/25 |
| affordability_status | 12/25 | 19/25 |
| recommended_payment_method | 12/25 | 21/25 |
| payment_plan | 11/25 | 21/25 |
| earliest_date_for_full_payment | 12/25 | 16/25 |
| spending_changes_needed | 22/25 | 20/25 |

All operational fields match exactly on 2/25 samples. Mean absolute safe-amount error divided by requested amount fell from 25.73% to 8.33%. Each request has equal weight despite different currencies. Explanation text equality is not a semantic quality metric.

## Checkpoints

All 25 samples were rerun at every financial-model checkpoint. Full per-request values and regressions are in `forecast_regressions.json`.

| Stage | Method matches | Spending-change matches |
|---|---:|---:|
| baseline | 12/25 | 22/25 |
| evidence | 14/25 | 20/25 |
| salary | 16/25 | 19/25 |
| variable_ownership | 16/25 | 19/25 |
| expense_classification | 15/25 | 19/25 |
| receipt_separation | 16/25 | 18/25 |
| bound_payroll | 16/25 | 18/25 |
| explicit_amendments | 16/25 | 18/25 |
| selected_mean | 21/25 | 20/25 |
| omitted_unknown_credit | 21/25 | 20/25 |

## Estimator comparison

Run `python3.12 code/compare_estimators.py` to reproduce the comparison. The seven estimators are fixed conventional choices. Rolling 30-day historical holdouts use only earlier observations; expected sample outputs are loaded only after predictions finish. The selected historical mean has the lowest historical absolute and squared relative error and the lowest sample amount error. Contractual amounts and explicit amendments retain their separate rules.

| Estimator | Historical absolute error | Method matches | Spending-change matches |
|---|---:|---:|---:|
| max_recent3 | 16.99% | 16/25 | 18/25 |
| mean_recent3 | 10.39% | 21/25 | 19/25 |
| median_recent3 | 12.48% | 20/25 | 19/25 |
| mean_all | 8.76% | 21/25 | 20/25 |
| median_all | 9.94% | 20/25 | 19/25 |
| q75_all | 14.17% | 16/25 | 19/25 |
| upper_mean | 9.68% | 19/25 | 19/25 |

There were 958 historical holdouts. Repeating the maximum recent purchase overstated recurring budgets; averaging all observations reduced that bias. This is an estimate of spending, not a guarantee of future spending.

## Remaining mismatches and regressions

* `request_19` regressed from the expected partial-payment method to no recommendation. The earlier model dropped groceries entirely because a separate delivered-order receipt broke the cadence. Restoring the weekly budget lowers capacity; the conservative debit-before-salary ordering also reserves childcare due on payday. We did not remove real expenses or change ordering just to match the sample.
* Spending-change equality regressed on `request_08` and `request_12`. Their selected schedules match the samples, but the current 90-day simulation requires spending cuts. Removing them would breach the implemented forecast. These account for the drop from 22/25 to 20/25.
* `request_21` still overestimates capacity: the requested 1574.40 is fully affordable under this forecast, versus the sample capacity of 1543.35 with spending changes. No request-specific adjustment was added.
* `request_06`, `request_09` and `request_13` also retain payment-method mismatches. The incomplete optional evidence no longer blocks `request_06`; its remaining failure comes from projected cash flow.
* The expected methods are restored on `request_01`, `request_04`, `request_07`, `request_08`, `request_11`, `request_12`, `request_16`, `request_17`, `request_22` and `request_23`. Exact amounts remain estimates; see `sample_results.md` for each difference.

## Full evaluation output and evidence

49 full payments, 40 installment plans, 38 waits, 9 partial payments and 114 no-payment recommendations. Four requests (`request_87`, `request_119`, `request_127`, `request_153`) use the explicitly uncertified zero/not-recommended fallback because incomplete evidence proves an unresolved debit. They still have valid output rows.

The full prediction used 203 cached AI resolutions and six literal percentage-amendment fallbacks. The same fallback also resolved one sample message. No image amount was invented. A live attempt to refresh seven missing messages failed with provider RateLimitError; the exact lease-amendment fallback was used instead. Other incomplete optional facts remain visible in traces and do not become new income.

`prediction_validation.json` lists output counts, input preservation, evidence issues and the four blocked requests. `usage_report.md` covers the actual 250-request run: zero new calls/tokens/cost, with the extraction model identified. Those zeros exclude earlier cached extraction cost; failed refresh calls have unknown usage in `evidence_extraction.json`.

## Re-run

```sh
.venv/bin/python3.12 -m unittest discover -s code/tests -v
.venv/bin/python3.12 code/main.py evaluate-samples
.venv/bin/python3.12 code/main.py predict --offline --output output.csv
.venv/bin/python3.12 code/main.py validate-output output.csv
```

Keep the existing evidence cache when reproducing this run. Changing extraction model or omitting the ignored cache changes which financial facts can be resolved.

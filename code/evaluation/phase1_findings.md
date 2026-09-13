# Phase 1 findings

Python 3.12.3; 25 unittest tests passed. Sample evaluation completed for all 25
public requests. No evaluation-request predictions, AI calls, dataset changes,
or root output.csv. See sample_results.md for every mismatch and candidate
rejection, and sample_results.json for exact predictions, labels, cash flows,
input hashes and evidence metadata/text.

## Accuracy

| Field | Exact text | Normalized value |
|---|---:|---:|
| request_id | 25/25 (100%) | 25/25 (100%) |
| amount_safe_to_pay | 0/25 (0%) | 0/25 (0%) |
| affordability_status | 10/25 (40%) | 10/25 (40%) |
| recommended_payment_method | 11/25 (44%) | 11/25 (44%) |
| payment_plan | 8/25 (32%) | 10/25 (40%) |
| earliest_date_for_full_payment | 11/25 (44%) | 11/25 (44%) |
| spending_changes_needed | 22/25 (88%) | 22/25 (88%) |
| decision_explanation | 0/25 (0%) | 0/25 (0%) |

Request accuracy is 0/25 including explanation and 0/25 excluding explanation.
Normalization only removes differences in decimal spelling; there is no monetary
tolerance. Explanation equality is lexical, not a judgment of explanation quality.
Passing invariant tests establishes mechanical consistency under the documented
forecast assumptions; it does not establish accurate financial reconstruction.

## Image-backed amounts affecting samples

| Sample | Image / event | Missing fact | Baseline effect |
|---|---|---|---|
| 03 | image_01 / event_253 | August net salary | Historical cash not replayed; salary composition/recurrence unresolved |
| 16 | image_02 / event_1442 | Outstanding rent balance, scheduled August 16 | Unknown active debit blocks certification; safe amount is zero fallback |
| 17 | image_03 / event_1545 | Bulk groceries and pantry purchase | Historical amount absent from conservative grocery amount estimation |
| 19 | image_04 / event_1700 | Delivered grocery order | Unknown amount and irregular category history leave recurrence unresolved |
| 20 | image_05 / event_1786 | Outstanding telecom bill, pending February 9 | Unknown active debit blocks certification; safe amount is zero fallback |

All image files exist. Pixels were not interpreted and no amount was guessed.
Images 02 and 05 definitely prevent certification in this implementation. The
others may change recurrence or evidence interpretation; their counterfactual
score contribution has not been measured. The remaining eleven image links
belong to evaluation requests and have not been used to produce predictions.

## Uninterpreted sample messages

These summaries describe input text, not implemented amendments. Every listed
message remains unresolved in the engine. Some restate cash-state rules already
handled, so unresolved does not imply that the message caused a mismatch.

| Sample | Message | Input content needing reconciliation |
|---|---|---|
| 02 | message_01 | Salary increase to IDR 42,750,000 effective August 15 |
| 03 | message_02 | Regular salary and one-time adjustment shown separately |
| 04 | message_03 | Unapproved quarterly bonus |
| 06 | message_04 | Temporary reduced pay continues for next payroll |
| 07 | message_05 | Confirmed payday amended to September 23 |
| 08 | message_06 | Next salary EUR 1,422.85; unpaid-leave adjustment |
| 10 | message_07 | Platform payout remains pending and unavailable |
| 11 | message_08 | Confirmed base salary IDR 38,760,000; commissions unapproved |
| 12 | message_09 | Seasonal contract ended; no confirmed renewal |
| 14 | message_10 | Salary resumes August 15; recurring childcare starts |
| 15 | message_11 | First salary EUR 1,661 confirmed for January 15 |
| 16 | message_12 | Rent increases by 12% next payment |
| 18 | message_13 | Matching debit/credit is an internal account transfer |
| 20 | message_14 | Refund initiated but not credited |
| 22 | message_15 | Portfolio increase is valuation, not sale proceeds |
| 23 | message_16 | Prize still processing, not credited |
| 24 | message_17 | Prize settled once, no recurring payment |

02, 07, 08, 11, 14, 15 and 16 contain particularly consequential future salary,
payday or expense amendments. Implementing them is likely useful; it is not yet
proven sufficient to correct those samples. 06, 10, 12, 20, 22, 23 and 24 partly
overlap with existing structured-state or nonrecurring-income safeguards.

## Open interpretation questions

1. Is the cash snapshot before or after request-day activity and pending holds?
   The baseline assumes settled request-day cash is included and pending holds
   are not. The CSV has no explicit snapshot timestamp or hold-accounting flag.
2. What conservative estimator best models variable essentials: category cadence,
   rolling monthly budgets, recent maxima or a buffered average? Maximum of the
   last three observations is intentionally simple and fails exact capacity on
   every sample. Irregular patterns can also be missed rather than overestimated.
3. What establishes continued salary after only one or two observations, a
   shifted payday, a temporary reduction, or a pause? Phase 1 requires strict
   recurring history, counts explicit scheduled salary once, and does not apply
   message confirmations. This is a major source of omitted or stale income.
4. Should the 90-day interval include day +90, and what intraday ordering should
   apply when essential debits and salary settle on the same date? The baseline
   checks the opening balance and debits before credits, with payments afterward.
5. Does max_installment_months constrain payment count, elapsed months or both?
   What rounding tolerance should reconcile supplied repeated payments and total?
   The baseline documents its count/duration and half-cent-per-payment choices.
6. Unresolved evidence has no status in the required output enum. The engine
   reports a provisional explanation, and unknown active debits produce zero /
   not_recommended as an explicitly uncertified fallback, not a proven rejection.

## Next fixes, ranked by likely score benefit

1. Improve cash-flow reconstruction and validate aggregate spending assumptions.
   Exact amounts fail 25/25; history rules omit first-job income, shifted payday
   streams and some irregular essentials. Investigate these with input-grounded
   fixtures rather than fitting constants to sample labels.
2. Implement auditable message-to-fact amendments, with provenance, dates, source
   precedence and confidence. Prioritize the salary/date/lease messages above.
   Keep model interpretation separate from deterministic monetary validation.
3. Extract and validate the five sample image amounts, especially active debits
   in 16 and 20. Decompose net salary/one-time pay before inferring recurrence.
4. Add permitted spending-change search. Samples 06, 11 and 21 require changes;
   those expected actions cannot be produced by this Phase 1 candidate set.
5. Revisit day-boundary and installment interpretations only after reconstruction
   improves; keep exact option schedules and semantic Decimal comparisons.
   Improve explanations from final trace facts; copying sample wording is not a fix.

This ranking is qualitative. No counterfactual runs with interpreted evidence or
spending changes were performed, so no numerical score improvement is promised.

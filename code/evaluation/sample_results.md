# Offline agent sample evaluation

Cached evidence only; flexible spending search enabled. Cache misses remain unresolved.
Normalized equality parses decimals and schedules exactly; there is no tolerance.
Explanation accuracy is exact text equality, not semantic grading.

| Field | Normalized correct | Exact text correct |
|---|---:|---:|
| request_id | 25/25 (100%) | 25/25 (100%) |
| amount_safe_to_pay | 0/25 (0%) | 0/25 (0%) |
| affordability_status | 12/25 (48%) | 12/25 (48%) |
| recommended_payment_method | 14/25 (56%) | 14/25 (56%) |
| payment_plan | 13/25 (52%) | 11/25 (44%) |
| earliest_date_for_full_payment | 11/25 (44%) | 11/25 (44%) |
| spending_changes_needed | 19/25 (76%) | 19/25 (76%) |
| decision_explanation | 0/25 (0%) | 0/25 (0%) |

All fields correct: 0/25.
All operational fields excluding explanation: 0/25.
Exact-text full rows: 0/25.

## Mismatch table

| Request | Safe amount: predicted / expected | Method: predicted / expected | Incorrect fields |
|---|---|---|---|
| request_01 | 3424.13 / 25256 | not_recommended / full_payment | A, S, M, P, D, E |
| request_02 | 16202550.61 / 17229139.2 | not_recommended / installments | A, S, M, P, D, E |
| request_03 | 872452.6 / 873000 | wait / wait | A, E |
| request_04 | 7757592.36 / 8401800 | wait / wait | A, S, D, C, E |
| request_05 | 0 / 737 | not_recommended / not_recommended | A, E |
| request_06 | 389.24 / 603.3 | not_recommended / full_payment | A, S, M, P, D, C, E |
| request_07 | 0 / 87170.56 | not_recommended / installments | A, S, M, P, D, E |
| request_08 | 0 / 284.57 | not_recommended / wait | A, S, M, P, D, E |
| request_09 | 0 / 166.61 | not_recommended / full_payment | A, S, M, P, D, E |
| request_10 | 0 / 12700 | not_recommended / not_recommended | A, E |
| request_11 | 10155966.94 / 12510645 | wait / full_payment | A, M, P, C, E |
| request_12 | 55861.14 / 65164 | not_recommended / installments | A, S, M, P, D, E |
| request_13 | 202.7 / 433.4 | not_recommended / wait | A, S, M, P, D, E |
| request_14 | 0 / 597.74 | not_recommended / not_recommended | A, E |
| request_15 | 0 / 83.05 | not_recommended / not_recommended | A, E |
| request_16 | 0 / 122500 | not_recommended / full_payment | A, S, M, P, D, E |
| request_17 | 236925.14 / 243849.58 | installments / installments | A, D, C, E |
| request_18 | 399.86 / 462 | wait / wait | A, E |
| request_19 | 22139.94 / 28820 | partial_payment / partial_payment | A, P, E |
| request_20 | 0 / 5400 | not_recommended / not_recommended | A, E |
| request_21 | 1574.4 / 1543.35 | full_payment / full_payment | A, S, D, C, E |
| request_22 | 429.68 / 475.46 | not_recommended / installments | A, S, M, P, D, E |
| request_23 | 2791.91 / 9152 | wait / wait | A, S, D, C, E |
| request_24 | 12369.96 / 13420 | not_recommended / not_recommended | A, E |
| request_25 | 0 / 1425000 | not_recommended / not_recommended | A, E |

A=safe amount; S=status; M=method; P=plan; D=earliest date; C=spending changes; E=explanation.

## Detailed diagnostics

### request_01

* amount_safe_to_pay:
  * predicted: `3424.13`
  * expected: `25256`
* affordability_status:
  * predicted: `not_affordable`
  * expected: `affordable_now`
* recommended_payment_method:
  * predicted: `not_recommended`
  * expected: `full_payment`
* payment_plan:
  * predicted: `none`
  * expected: `2024-03-03:25256`
* earliest_date_for_full_payment:
  * predicted: ``
  * expected: `2024-03-03`
* decision_explanation:
  * predicted: `Safe today before changes: 3424.13 ZAR; protected minimum: 18000. No safe eligible plan completes by the deadline under the resolved forecast. Limiting expense: event_84 (549.05 on 2024-06-01).`
  * expected: `Pay ZAR 25,256 today. This leaves at least ZAR 18,000 available over the next 90 days.`

Minimum projected balance: 21424.13

Evidence/issues:

Candidate rejections:
* full_payment payment_option_01: minimum balance breached on 2024-05-02: -3831.87
* installments payment_option_02: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit
* installments payment_option_03: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit
* installments payment_option_04: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit

Inferred streams:
* event_29: education loan instalment; monthly=11; observations=5; conservative recent amount=3487
* event_97: dining; interval=14; observations=13; conservative recent amount=1222.49
* event_28: professional training fee; monthly=8; observations=5; conservative recent amount=1821.6
* event_58: groceries; interval=7; observations=26; conservative recent amount=964.05
* event_32: apartment rent transfer; monthly=2; observations=6; conservative recent amount=5148
* event_84: transport; interval=7; observations=26; conservative recent amount=549.05
* event_27: household utility payment; monthly=6; observations=5; conservative recent amount=1651.81
* event_31: delivery service plan; monthly=13; observations=5; conservative recent amount=306.9
* event_30: music service subscription; monthly=11; observations=5; conservative recent amount=235.4

### request_02

* amount_safe_to_pay:
  * predicted: `16202550.61`
  * expected: `17229139.2`
* affordability_status:
  * predicted: `not_affordable`
  * expected: `affordable_with_plan`
* recommended_payment_method:
  * predicted: `not_recommended`
  * expected: `installments`
* payment_plan:
  * predicted: `none`
  * expected: `2025-08-08:15952906.67|2025-09-07:15952906.67|2025-10-07:15952906.67`
* earliest_date_for_full_payment:
  * predicted: `2025-10-15`
  * expected: `2025-09-15`
* decision_explanation:
  * predicted: `Safe today before changes: 16202550.61 IDR; protected minimum: 29158400. No safe eligible plan completes by the deadline under the resolved forecast. Baseline full payment first becomes safe on 2025-10-15, after the deadline. Limiting expense: event_142 (1352563.79 on 2025-08-15). Unresolved evidence/forecast assumptions remain; see audit.`
  * expected: `Use 3 installments of IDR 15,952,906.67, starting 8 August 2025. This leaves at least IDR 29,158,400 available.`

Minimum projected balance: 45360950.61

Evidence/issues:
* unresolved_evidence message_01: source unavailable or not cached; no value imputed; blocking=False

Candidate rejections:
* full_payment payment_option_06: payment method excluded by user; minimum balance breached on 2025-08-05: -657049.39
* wait payment_option_06: payment outside request/deadline/forecast bounds; payment method excluded by user
* partial_payment : payment outside request/deadline/forecast bounds; partial payment not permitted or no strictly partial capacity
* installments payment_option_05: minimum balance breached on 2025-09-09: 14646685.92
* installments payment_option_07: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit

Inferred streams:
* event_136: payroll credit; monthly=15; observations=5; conservative recent amount=33345000
* event_184: dining; interval=21; observations=9; conservative recent amount=1204805.34
* event_140: course tuition; monthly=9; observations=5; conservative recent amount=3040000
* event_142: cinema and events; monthly=15; observations=5; conservative recent amount=1352563.79
* event_162: groceries; interval=10; observations=18; conservative recent amount=2365919.6
* event_141: clinic payment; monthly=11; observations=5; conservative recent amount=1641668.72
* event_144: home repair reserve; monthly=4; observations=6; conservative recent amount=3534000
* event_139: household insurance; monthly=8; observations=5; conservative recent amount=1132400
* event_175: transport; interval=14; observations=13; conservative recent amount=1327886.54
* event_138: municipal utilities; monthly=7; observations=5; conservative recent amount=2141849.94
* event_143: shared storage plan; monthly=13; observations=5; conservative recent amount=369550

### request_03

* amount_safe_to_pay:
  * predicted: `872452.6`
  * expected: `873000`
* decision_explanation:
  * predicted: `Safe today before changes: 872452.60 IDR; protected minimum: 2668700. Use wait, total 5491000, completing 2019-11-15. Lowest projected balance: 3541152.60 on 2019-09-14. Earlier full payment would not preserve the reserve under this forecast. Limiting expense: event_216 (180395.29 on 2019-09-14). Projected income includes event_210: 4365000 on 2019-09-15. Unresolved evidence/forecast assumptions remain; see audit.`
  * expected: `Pay IDR 5,491,000 in full on 15 November 2019. Paying earlier would take the balance below the IDR 2,668,700 minimum.`

Minimum projected balance: 3541152.60

Evidence/issues:
* unresolved_evidence image_01: source unavailable or not cached; no value imputed; blocking=False
* unresolved_evidence message_02: source unavailable or not cached; no value imputed; blocking=False
* missing_historical_amount event_253: already in cash snapshot; recurrence/evidence unresolved; blocking=False

Candidate rejections:
* full_payment payment_option_08: minimum balance breached on 2019-09-03: -1949847.40
* partial_payment : partial payment not permitted or no strictly partial capacity
* installments payment_option_09: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit
* installments payment_option_10: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit

Inferred streams:
* event_210: payroll credit; monthly=15; observations=5; conservative recent amount=4365000
* event_252: dining; interval=21; observations=9; conservative recent amount=171303.21
* event_234: groceries; interval=10; observations=18; conservative recent amount=240706.45
* event_212: landlord standing order; monthly=4; observations=5; conservative recent amount=1140000
* event_216: clothing and household items; monthly=14; observations=5; conservative recent amount=180395.29
* event_243: transport; interval=21; observations=9; conservative recent amount=106233.46
* event_213: water and power payment; monthly=8; observations=5; conservative recent amount=303042.45
* event_214: shared storage plan; monthly=14; observations=5; conservative recent amount=20900
* event_215: video streaming plan; monthly=11; observations=5; conservative recent amount=117800

### request_04

* amount_safe_to_pay:
  * predicted: `7757592.36`
  * expected: `8401800`
* affordability_status:
  * predicted: `affordable_with_plan`
  * expected: `affordable_later`
* earliest_date_for_full_payment:
  * predicted: `2024-07-15`
  * expected: `2024-06-15`
* spending_changes_needed:
  * predicted: `reduce_to:event_290:1097339.58`
  * expected: `none`
* decision_explanation:
  * predicted: `Safe today before changes: 7757592.36 IDR; protected minimum: 30686600. Use wait, total 12693000, completing 2024-06-15. Lowest projected balance: 30686600.01 on 2024-07-14. Required changes: reduce_to:event_290:1097339.58. Earlier full payment would not preserve the reserve under this forecast. Limiting expense: event_343 (1016425.58 on 2024-07-14). Projected income includes event_284: 38190000 on 2024-06-15. Unresolved evidence/forecast assumptions remain; see audit.`
  * expected: `Wait until 15 June 2024, then pay IDR 12,693,000 in full. Paying sooner would put the IDR 30,686,600 minimum at risk.`

Minimum projected balance: 30686600.01

Evidence/issues:
* unresolved_evidence message_03: source unavailable or not cached; no value imputed; blocking=False

Candidate rejections:
* full_payment payment_option_11: minimum balance breached on 2024-06-11: 25751192.36
* wait payment_option_11: payment outside request/deadline/forecast bounds
* partial_payment : payment outside request/deadline/forecast bounds; payment method excluded by user
* installments payment_option_12: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit

Inferred streams:
* event_284: payroll credit; monthly=15; observations=5; conservative recent amount=38190000
* event_356: dining; interval=14; observations=13; conservative recent amount=2108488.15
* event_290: local event tickets; monthly=13; observations=5; conservative recent amount=1542620
* event_317: groceries; interval=7; observations=26; conservative recent amount=1809752.54
* event_291: residential rent payment; monthly=1; observations=6; conservative recent amount=12293000
* event_343: transport; interval=7; observations=26; conservative recent amount=1016425.58
* event_286: municipal utilities; monthly=5; observations=5; conservative recent amount=2033868.83
* event_288: food delivery membership; monthly=12; observations=5; conservative recent amount=377150
* event_289: gym membership; monthly=9; observations=5; conservative recent amount=1027900
* event_287: music service subscription; monthly=10; observations=5; conservative recent amount=332500

### request_05

* amount_safe_to_pay:
  * predicted: `0`
  * expected: `737`
* decision_explanation:
  * predicted: `Safe today before changes: 0 ZAR; protected minimum: 13100. No safe eligible plan completes by the deadline under the resolved forecast. Limiting expense: event_437 (388.74 on 2026-02-04). Unresolved evidence/forecast assumptions remain; see audit.`
  * expected: `Do not make this payment by 12 January 2026. None of the available options keeps the ZAR 13,100 minimum protected.`

Minimum projected balance: 8018.40

Evidence/issues:
* stale_recurrence event_382: payroll credit: expected next occurrence 2025-10-15 already overdue; blocking=False

Candidate rejections:
* full_payment payment_option_13: minimum balance breached on 2025-12-16: -7469.60
* installments payment_option_14: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit
* installments payment_option_15: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit

Inferred streams:
* event_393: vehicle loan payment; monthly=11; observations=5; conservative recent amount=968
* event_395: dependent care payment; monthly=13; observations=5; conservative recent amount=840.4
* event_424: groceries; interval=7; observations=26; conservative recent amount=720.51
* event_394: therapy appointment; monthly=10; observations=5; conservative recent amount=722.37
* event_398: apartment rent transfer; monthly=2; observations=6; conservative recent amount=4972
* event_397: personal shopping; monthly=12; observations=5; conservative recent amount=422.67
* event_437: transport; interval=14; observations=13; conservative recent amount=388.74
* event_392: municipal utilities; monthly=6; observations=5; conservative recent amount=750.89
* event_396: cloud storage plan; monthly=12; observations=5; conservative recent amount=113.3

### request_06

* amount_safe_to_pay:
  * predicted: `389.24`
  * expected: `603.3`
* affordability_status:
  * predicted: `not_affordable`
  * expected: `affordable_with_plan`
* recommended_payment_method:
  * predicted: `not_recommended`
  * expected: `full_payment`
* payment_plan:
  * predicted: `none`
  * expected: `2026-01-03:620.40`
* earliest_date_for_full_payment:
  * predicted: `2026-03-15`
  * expected: `2026-01-15`
* spending_changes_needed:
  * predicted: `none`
  * expected: `stop:event_476`
* decision_explanation:
  * predicted: `Safe today before changes: 389.24 EUR; protected minimum: 800. No safe eligible plan completes by the deadline under the resolved forecast. Baseline full payment first becomes safe on 2026-03-15, after the deadline. Limiting expense: event_556 (57.28 on 2026-02-15). Unresolved evidence/forecast assumptions remain; see audit.`
  * expected: `Stop the family streaming plan, then pay EUR 620.40 today. This leaves at least EUR 800 available.`

Minimum projected balance: 1189.24

Evidence/issues:
* unresolved_evidence message_04: source unavailable or not cached; no value imputed; blocking=False

Candidate rejections:
* full_payment payment_option_16: minimum balance breached on 2026-01-10: 568.84
* wait payment_option_16: payment outside request/deadline/forecast bounds
* partial_payment : payment outside request/deadline/forecast bounds; partial payment not permitted or no strictly partial capacity
* installments payment_option_17: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit
* installments payment_option_18: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit

Inferred streams:
* event_471: payroll credit; monthly=15; observations=5; conservative recent amount=1037.52
* event_556: dining; interval=7; observations=25; conservative recent amount=57.28
* event_478: monthly entertainment spend; monthly=15; observations=5; conservative recent amount=38.33
* event_496: groceries; interval=10; observations=18; conservative recent amount=52.76
* event_474: vehicle insurance premium; monthly=8; observations=5; conservative recent amount=26
* event_472: monthly rent; monthly=3; observations=5; conservative recent amount=254.1
* event_477: household shopping; monthly=13; observations=5; conservative recent amount=39.88
* event_531: transport; interval=5; observations=35; conservative recent amount=32.9
* event_473: water and power payment; monthly=7; observations=5; conservative recent amount=58.98
* event_475: shared storage plan; monthly=13; observations=5; conservative recent amount=5
* event_476: family streaming plan; monthly=10; observations=5; conservative recent amount=19

### request_07

* amount_safe_to_pay:
  * predicted: `0`
  * expected: `87170.56`
* affordability_status:
  * predicted: `not_affordable`
  * expected: `affordable_with_plan`
* recommended_payment_method:
  * predicted: `not_recommended`
  * expected: `installments`
* payment_plan:
  * predicted: `none`
  * expected: `2024-09-12:68432|2024-10-10:68432|2024-11-07:68432`
* earliest_date_for_full_payment:
  * predicted: ``
  * expected: `2024-10-23`
* decision_explanation:
  * predicted: `Safe today before changes: 0 INR; protected minimum: 93000. No safe eligible plan completes by the deadline under the resolved forecast. Limiting expense: event_583 (34200 on 2024-12-04). Unresolved evidence/forecast assumptions remain; see audit.`
  * expected: `Use 3 installments of INR 68,432, starting 12 September 2024. This leaves at least INR 93,000 available.`

Minimum projected balance: -45019.81

Evidence/issues:
* unresolved_evidence message_05: source unavailable or not cached; no value imputed; blocking=False
* irregular_history event_578: no supported cadence for payroll credit; blocking=False

Candidate rejections:
* full_payment payment_option_20: payment method excluded by user; minimum balance breached on 2024-09-05: -242419.81
* installments payment_option_19: minimum balance breached on 2024-10-04: -250315.81
* installments payment_option_21: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit

Inferred streams:
* event_581: personal loan payment; monthly=13; observations=5; conservative recent amount=15650
* event_614: dining; interval=21; observations=9; conservative recent amount=6664.9
* event_596: groceries; interval=14; observations=13; conservative recent amount=7913.81
* event_583: monthly rent; monthly=4; observations=6; conservative recent amount=34200
* event_605: transport; interval=21; observations=9; conservative recent amount=3773.92
* event_580: electricity bill; monthly=8; observations=5; conservative recent amount=7387.41
* event_582: music subscription; monthly=13; observations=5; conservative recent amount=1005

### request_08

* amount_safe_to_pay:
  * predicted: `0`
  * expected: `284.57`
* affordability_status:
  * predicted: `not_affordable`
  * expected: `affordable_later`
* recommended_payment_method:
  * predicted: `not_recommended`
  * expected: `wait`
* payment_plan:
  * predicted: `none`
  * expected: `2025-04-15:996.60`
* earliest_date_for_full_payment:
  * predicted: ``
  * expected: `2025-04-15`
* decision_explanation:
  * predicted: `Safe today before changes: 0 EUR; protected minimum: 800. No safe eligible plan completes by the deadline under the resolved forecast. Limiting expense: event_716 (56.05 on 2025-05-08). Unresolved evidence/forecast assumptions remain; see audit.`
  * expected: `Pay EUR 996.60 in full on 15 April 2025. Paying earlier would take the balance below the EUR 800 minimum.`

Minimum projected balance: -714.07

Evidence/issues:
* unresolved_evidence message_06: source unavailable or not cached; no value imputed; blocking=False

Candidate rejections:
* full_payment payment_option_22: minimum balance breached on 2025-02-07: -1710.67
* installments payment_option_23: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit

Inferred streams:
* event_643: payroll credit; monthly=15; observations=5; conservative recent amount=782.57
* event_647: personal loan payment; monthly=10; observations=5; conservative recent amount=177
* event_716: dining; interval=14; observations=13; conservative recent amount=56.05
* event_646: school fee payment; monthly=7; observations=5; conservative recent amount=89
* event_677: groceries; interval=7; observations=26; conservative recent amount=72.38
* event_650: apartment rent transfer; monthly=1; observations=6; conservative recent amount=467.5
* event_703: transport; interval=7; observations=26; conservative recent amount=47.21
* event_651: municipal utilities; monthly=5; observations=6; conservative recent amount=82.61
* event_649: grocery delivery membership; monthly=12; observations=5; conservative recent amount=24
* event_648: music subscription; monthly=10; observations=5; conservative recent amount=14

### request_09

* amount_safe_to_pay:
  * predicted: `0`
  * expected: `166.61`
* affordability_status:
  * predicted: `not_affordable`
  * expected: `affordable_now`
* recommended_payment_method:
  * predicted: `not_recommended`
  * expected: `full_payment`
* payment_plan:
  * predicted: `none`
  * expected: `2026-07-04:166.61`
* earliest_date_for_full_payment:
  * predicted: ``
  * expected: `2026-07-04`
* decision_explanation:
  * predicted: `Safe today before changes: 0 EUR; protected minimum: 600. No safe eligible plan completes by the deadline under the resolved forecast. Limiting expense: event_752 (211.2 on 2026-10-02).`
  * expected: `Pay EUR 166.61 today. This keeps the EUR 600 minimum available over the next 90 days.`

Minimum projected balance: 507.40

Evidence/issues:

Candidate rejections:
* full_payment payment_option_24: minimum balance breached on 2026-09-25: 340.79
* installments payment_option_25: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit
* installments payment_option_26: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit

Inferred streams:
* event_788: dining; interval=21; observations=9; conservative recent amount=35.49
* event_770: groceries; interval=10; observations=18; conservative recent amount=51.3
* event_752: monthly rent; monthly=2; observations=6; conservative recent amount=211.2
* event_751: household shopping; monthly=12; observations=5; conservative recent amount=28.32
* event_779: transport; interval=21; observations=9; conservative recent amount=28.34
* event_748: water and power payment; monthly=6; observations=5; conservative recent amount=71.04
* event_749: cloud storage plan; monthly=12; observations=5; conservative recent amount=5
* event_750: video streaming plan; monthly=9; observations=5; conservative recent amount=20

### request_10

* amount_safe_to_pay:
  * predicted: `0`
  * expected: `12700`
* decision_explanation:
  * predicted: `Safe today before changes: 0 INR; protected minimum: 225400. No safe eligible plan completes by the deadline under the resolved forecast. Limiting expense: event_866 (8755.75 on 2025-03-06). Unresolved evidence/forecast assumptions remain; see audit.`
  * expected: `Do not make this payment by 10 February 2025. None of the available options keeps the INR 225,400 minimum protected.`

Minimum projected balance: 187502.17

Evidence/issues:
* unresolved_evidence message_07: source unavailable or not cached; no value imputed; blocking=False

Candidate rejections:
* full_payment payment_option_27: payment method excluded by user; minimum balance breached on 2025-01-17: -79197.83
* installments payment_option_28: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit

Inferred streams:
* event_904: dining; interval=14; observations=13; conservative recent amount=10370.83
* event_838: cinema and events; monthly=15; observations=5; conservative recent amount=4883.78
* event_866: groceries; interval=7; observations=26; conservative recent amount=8755.75
* event_840: monthly rent; monthly=3; observations=6; conservative recent amount=69100
* event_891: transport; interval=7; observations=25; conservative recent amount=6359.49
* event_834: electricity and water bill; monthly=7; observations=5; conservative recent amount=17771.13
* event_836: delivery service plan; monthly=14; observations=5; conservative recent amount=1895
* event_837: community fitness plan; monthly=11; observations=5; conservative recent amount=4860
* event_835: music subscription; monthly=12; observations=5; conservative recent amount=2800

### request_11

* amount_safe_to_pay:
  * predicted: `10155966.94`
  * expected: `12510645`
* recommended_payment_method:
  * predicted: `wait`
  * expected: `full_payment`
* payment_plan:
  * predicted: `2025-05-15:13110000`
  * expected: `2025-05-03:13110000`
* spending_changes_needed:
  * predicted: `reduce_to:event_948:1089562.41|reduce_to:event_989:665950`
  * expected: `reduce_to:event_989:665950`
* decision_explanation:
  * predicted: `Safe today before changes: 10155966.94 IDR; protected minimum: 34140600. Use wait, total 13110000, completing 2025-05-15. Lowest projected balance: 34140600.00 on 2025-06-14. Required changes: reduce_to:event_948:1089562.41; reduce_to:event_989:665950.00. Earlier full payment would not preserve the reserve under this forecast. Limiting expense: event_949 (168150 on 2025-06-14). Projected income includes event_941: 23256000 on 2025-05-15. Unresolved evidence/forecast assumptions remain; see audit.`
  * expected: `Reduce the weekend food delivery to IDR 665,950, then pay IDR 13,110,000 today. This leaves at least IDR 34,140,600 available.`

Minimum projected balance: 34140600.00

Evidence/issues:
* unresolved_evidence message_08: source unavailable or not cached; no value imputed; blocking=False

Candidate rejections:
* full_payment payment_option_29: minimum balance breached on 2025-05-14: 31186566.94
* wait payment_option_29: payment outside request/deadline/forecast bounds
* partial_payment : payment outside request/deadline/forecast bounds; payment method excluded by user; partial payment not permitted or no strictly partial capacity
* installments payment_option_30: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit
* installments payment_option_31: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit
* installments payment_option_32: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit

Inferred streams:
* event_941: base salary; monthly=15; observations=5; conservative recent amount=23256000
* event_989: dining; interval=21; observations=9; conservative recent amount=1503635.49
* event_946: child education fee; monthly=10; observations=5; conservative recent amount=2544100
* event_948: games and recreation; monthly=16; observations=5; conservative recent amount=1674887.61
* event_967: groceries; interval=10; observations=18; conservative recent amount=1590529.64
* event_947: regular medicine purchase; monthly=12; observations=5; conservative recent amount=3165638.3
* event_943: home association fee; monthly=5; observations=5; conservative recent amount=2954500
* event_945: vehicle insurance premium; monthly=9; observations=5; conservative recent amount=1881000
* event_980: transport; interval=14; observations=13; conservative recent amount=1244835.69
* event_944: municipal utilities; monthly=8; observations=5; conservative recent amount=2796165.18
* event_949: cloud storage plan; monthly=14; observations=5; conservative recent amount=168150

### request_12

* amount_safe_to_pay:
  * predicted: `55861.14`
  * expected: `65164`
* affordability_status:
  * predicted: `not_affordable`
  * expected: `affordable_with_plan`
* recommended_payment_method:
  * predicted: `not_recommended`
  * expected: `installments`
* payment_plan:
  * predicted: `none`
  * expected: `2026-04-19:22590.19|2026-05-20:22590.19|2026-06-20:22590.19`
* earliest_date_for_full_payment:
  * predicted: ``
  * expected: `2026-04-05`
* decision_explanation:
  * predicted: `Safe today before changes: 55861.14 ZAR; protected minimum: 43200. No safe eligible plan completes by the deadline under the resolved forecast. Limiting expense: event_1018 (11792 on 2026-07-01). Unresolved evidence/forecast assumptions remain; see audit.`
  * expected: `Use 3 installments of ZAR 22,590.19, starting 19 April 2026. This leaves at least ZAR 43,200 available.`

Minimum projected balance: 99061.14

Evidence/issues:
* unresolved_evidence message_09: source unavailable or not cached; no value imputed; blocking=False

Candidate rejections:
* full_payment payment_option_34: payment method excluded by user; minimum balance breached on 2026-07-01: 33897.14
* installments payment_option_33: minimum balance breached on 2026-06-26: 31290.57
* installments payment_option_35: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit

Inferred streams:
* event_1054: dining; interval=21; observations=9; conservative recent amount=2089.92
* event_1036: groceries; interval=10; observations=18; conservative recent amount=2469.4
* event_1018: monthly rent; monthly=1; observations=6; conservative recent amount=11792
* event_1017: monthly shopping spend; monthly=11; observations=5; conservative recent amount=1401.99
* event_1045: transport; interval=21; observations=9; conservative recent amount=1684.28
* event_1014: water and power payment; monthly=5; observations=5; conservative recent amount=3755.96
* event_1015: shared storage plan; monthly=11; observations=5; conservative recent amount=447.7
* event_1016: family streaming plan; monthly=8; observations=5; conservative recent amount=1504.8

### request_13

* amount_safe_to_pay:
  * predicted: `202.7`
  * expected: `433.4`
* affordability_status:
  * predicted: `not_affordable`
  * expected: `affordable_later`
* recommended_payment_method:
  * predicted: `not_recommended`
  * expected: `wait`
* payment_plan:
  * predicted: `none`
  * expected: `2024-05-15:941.60`
* earliest_date_for_full_payment:
  * predicted: ``
  * expected: `2024-05-15`
* decision_explanation:
  * predicted: `Safe today before changes: 202.70 EUR; protected minimum: 1300. No safe eligible plan completes by the deadline under the resolved forecast. Limiting expense: event_1147 (50.46 on 2024-05-15).`
  * expected: `Pay EUR 941.60 in full on 15 May 2024. Paying earlier would take the balance below the EUR 1,300 minimum.`

Minimum projected balance: 1502.70

Evidence/issues:

Candidate rejections:
* full_payment payment_option_36: minimum balance breached on 2024-04-10: 561.10
* installments payment_option_37: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit
* installments payment_option_38: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit

Inferred streams:
* event_1087: primary household salary; monthly=15; observations=5; conservative recent amount=1343.54
* event_1160: dining; interval=14; observations=13; conservative recent amount=61.28
* event_1093: local event tickets; monthly=14; observations=5; conservative recent amount=37.9
* event_1121: groceries; interval=7; observations=26; conservative recent amount=118.36
* event_1094: shared housing rent; monthly=2; observations=6; conservative recent amount=622.6
* event_1147: transport; interval=7; observations=26; conservative recent amount=50.46
* event_1095: water and power payment; monthly=6; observations=6; conservative recent amount=143.7
* event_1091: delivery service plan; monthly=13; observations=5; conservative recent amount=21
* event_1092: community fitness plan; monthly=10; observations=5; conservative recent amount=61
* event_1090: music subscription; monthly=11; observations=5; conservative recent amount=29

### request_14

* amount_safe_to_pay:
  * predicted: `0`
  * expected: `597.74`
* decision_explanation:
  * predicted: `Safe today before changes: 0 EUR; protected minimum: 2200. No safe eligible plan completes by the deadline under the resolved forecast. Available methods are excluded by the user. Limiting expense: event_1226 (129.56 on 2025-11-02). Unresolved evidence/forecast assumptions remain; see audit.`
  * expected: `Do not proceed with the EUR 5,414.20 request. Although EUR 597.74 is available today, the full amount cannot be completed safely within 90 days.`

Minimum projected balance: -2441.29

Evidence/issues:
* unresolved_evidence message_10: source unavailable or not cached; no value imputed; blocking=False

Candidate rejections:
* full_payment payment_option_39: payment method excluded by user; minimum balance breached on 2025-08-04: -7855.49
* installments payment_option_40: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit

Inferred streams:
* event_1195: credit card repayment; monthly=12; observations=5; conservative recent amount=350
* event_1197: family support payment; monthly=14; observations=5; conservative recent amount=226
* event_1226: groceries; interval=7; observations=26; conservative recent amount=129.56
* event_1196: family healthcare expense; monthly=11; observations=5; conservative recent amount=95.17
* event_1200: monthly rent; monthly=3; observations=6; conservative recent amount=688.6
* event_1199: online retail purchases; monthly=13; observations=5; conservative recent amount=140.39
* event_1239: transport; interval=14; observations=13; conservative recent amount=62.3
* event_1194: energy provider bill; monthly=7; observations=5; conservative recent amount=153.69
* event_1198: cloud storage plan; monthly=13; observations=5; conservative recent amount=14

### request_15

* amount_safe_to_pay:
  * predicted: `0`
  * expected: `83.05`
* decision_explanation:
  * predicted: `Safe today before changes: 0 EUR; protected minimum: 1200. No safe eligible plan completes by the deadline under the resolved forecast. Available methods are excluded by the user. Limiting expense: event_1272 (435.6 on 2026-04-04). Unresolved evidence/forecast assumptions remain; see audit.`
  * expected: `Do not make this payment by 1 February 2026. None of the available options keeps the EUR 1,200 minimum protected.`

Minimum projected balance: -2313.01

Evidence/issues:
* unresolved_evidence message_11: source unavailable or not cached; no value imputed; blocking=False

Candidate rejections:
* full_payment payment_option_41: payment method excluded by user; minimum balance breached on 2026-01-06: -5998.01
* installments payment_option_42: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit
* installments payment_option_43: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit

Inferred streams:
* event_1269: credit card repayment; monthly=13; observations=5; conservative recent amount=84
* event_1335: dining; interval=14; observations=13; conservative recent amount=49.35
* event_1268: school fee payment; monthly=10; observations=5; conservative recent amount=159
* event_1297: groceries; interval=7; observations=25; conservative recent amount=64.42
* event_1272: landlord standing order; monthly=4; observations=6; conservative recent amount=435.6
* event_1322: transport; interval=7; observations=25; conservative recent amount=36.86
* event_1267: energy provider bill; monthly=8; observations=5; conservative recent amount=90.39
* event_1271: food delivery membership; monthly=15; observations=5; conservative recent amount=27
* event_1270: music subscription; monthly=13; observations=5; conservative recent amount=11

### request_16

* amount_safe_to_pay:
  * predicted: `0`
  * expected: `122500`
* affordability_status:
  * predicted: `not_affordable`
  * expected: `affordable_now`
* recommended_payment_method:
  * predicted: `not_recommended`
  * expected: `full_payment`
* payment_plan:
  * predicted: `none`
  * expected: `2023-08-12:122500`
* earliest_date_for_full_payment:
  * predicted: ``
  * expected: `2023-08-12`
* decision_explanation:
  * predicted: `Safe today before changes: 0 INR; protected minimum: 122400. No safe eligible plan completes by the deadline under the resolved forecast. Limiting expense: event_1441 (6354.26 on 2023-09-15). Unresolved evidence/forecast assumptions remain; see audit. Zero capacity is an uncertified fallback for missing required financial facts.`
  * expected: `Pay INR 122,500 today. This leaves at least INR 122,400 available over the next 90 days.`

Minimum projected balance: 343940.29

Evidence/issues:
* unresolved_evidence image_02: source unavailable or not cached; no value imputed; blocking=False
* unresolved_evidence message_12: source unavailable or not cached; no value imputed; blocking=False
* missing_active_amount event_1442: debit on 2023-08-16; amount requires image interpretation; blocking=True

Candidate rejections:
* full_payment payment_option_44: unresolved active debit prevents safety certification
* installments payment_option_45: unresolved active debit prevents safety certification; payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit
* installments payment_option_46: unresolved active debit prevents safety certification; payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit

Inferred streams:
* event_1364: payroll credit; monthly=15; observations=5; conservative recent amount=173000
* event_1373: vehicle loan payment; monthly=10; observations=6; conservative recent amount=17750
* event_1441: dining; interval=14; observations=13; conservative recent amount=6354.26
* event_1402: groceries; interval=7; observations=26; conservative recent amount=8883.15
* event_1371: monthly rent; monthly=1; observations=6; conservative recent amount=57100
* event_1376: clothing and household items; monthly=11; observations=6; conservative recent amount=10178.56
* event_1428: transport; interval=7; observations=26; conservative recent amount=5368.95
* event_1372: energy provider bill; monthly=5; observations=6; conservative recent amount=11512.87
* event_1375: cloud storage plan; monthly=11; observations=6; conservative recent amount=1055
* event_1374: video streaming plan; monthly=8; observations=6; conservative recent amount=3510

### request_17

* amount_safe_to_pay:
  * predicted: `236925.14`
  * expected: `243849.58`
* earliest_date_for_full_payment:
  * predicted: `2026-05-15`
  * expected: `2026-03-15`
* spending_changes_needed:
  * predicted: `stop:event_1476|reduce_to:event_1542:3506.4`
  * expected: `none`
* decision_explanation:
  * predicted: `Safe today before changes: 236925.14 INR; protected minimum: 166100. Use installments, total 285584.01, completing 2026-04-30. Lowest projected balance: 166100.01 on 2026-05-15. Required changes: stop:event_1476; reduce_to:event_1542:3506.40. Limiting expense: event_1545 (10873.47 on 2026-05-15). Projected income includes event_1546: 206000 on 2026-03-15. Unresolved evidence/forecast assumptions remain; see audit.`
  * expected: `Use 3 installments of INR 95,194.67, starting 1 March 2026. This leaves at least INR 166,100 available.`

Minimum projected balance: 166100.01

Evidence/issues:
* unresolved_evidence image_03: source unavailable or not cached; no value imputed; blocking=False
* missing_historical_amount event_1545: already in cash snapshot; recurrence/evidence unresolved; blocking=False

Candidate rejections:
* full_payment payment_option_48: payment method excluded by user; minimum balance breached on 2026-03-11: 128425.14
* wait payment_option_48: payment outside request/deadline/forecast bounds; payment method excluded by user
* partial_payment : payment outside request/deadline/forecast bounds; payment method excluded by user; partial payment not permitted or no strictly partial capacity
* installments payment_option_47: minimum balance breached on 2026-05-11: 144022.96
* installments payment_option_49: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit

Inferred streams:
* event_1471: payroll credit; monthly=15; observations=5; conservative recent amount=206000
* event_1475: credit card repayment; monthly=11; observations=5; conservative recent amount=30200
* event_1542: dining; interval=14; observations=13; conservative recent amount=6688.81
* event_1474: course tuition; monthly=8; observations=5; conservative recent amount=13660
* event_1545: groceries; interval=7; observations=27; conservative recent amount=10873.47
* event_1472: apartment rent transfer; monthly=2; observations=5; conservative recent amount=49600
* event_1529: transport; interval=7; observations=26; conservative recent amount=5741.08
* event_1473: municipal utilities; monthly=6; observations=5; conservative recent amount=10246.53
* event_1477: food delivery membership; monthly=13; observations=5; conservative recent amount=1675
* event_1476: music subscription; monthly=11; observations=5; conservative recent amount=2055

### request_18

* amount_safe_to_pay:
  * predicted: `399.86`
  * expected: `462`
* decision_explanation:
  * predicted: `Safe today before changes: 399.86 EUR; protected minimum: 1400. Use wait, total 3246.1, completing 2026-09-15. Lowest projected balance: 1799.86 on 2026-07-15. Earlier full payment would not preserve the reserve under this forecast. Limiting expense: event_1621 (101.88 on 2026-07-15). Projected income includes event_1571: 2310 on 2026-07-15. Unresolved evidence/forecast assumptions remain; see audit.`
  * expected: `Pay EUR 3,246.10 in full on 15 September 2026. Paying earlier would take the balance below the EUR 1,400 minimum.`

Minimum projected balance: 1799.86

Evidence/issues:
* unresolved_evidence message_13: source unavailable or not cached; no value imputed; blocking=False

Candidate rejections:
* full_payment payment_option_50: minimum balance breached on 2026-07-07: -1446.24
* partial_payment : partial payment not permitted or no strictly partial capacity
* installments payment_option_51: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit

Inferred streams:
* event_1571: payroll credit; monthly=15; observations=5; conservative recent amount=2310
* event_1621: dining; interval=14; observations=13; conservative recent amount=101.88
* event_1595: groceries; interval=10; observations=18; conservative recent amount=111.41
* event_1575: clinic payment; monthly=11; observations=5; conservative recent amount=162.41
* event_1577: building maintenance payment; monthly=4; observations=6; conservative recent amount=167
* event_1574: household insurance; monthly=8; observations=5; conservative recent amount=68
* event_1608: transport; interval=14; observations=13; conservative recent amount=49.04
* event_1573: energy provider bill; monthly=7; observations=5; conservative recent amount=125.4
* event_1576: family streaming plan; monthly=10; observations=5; conservative recent amount=68

### request_19

* amount_safe_to_pay:
  * predicted: `22139.94`
  * expected: `28820`
* payment_plan:
  * predicted: `2024-09-04:22139.94|2024-09-15:17520.06`
  * expected: `2024-09-04:28820|2024-09-15:10840`
* decision_explanation:
  * predicted: `Safe today before changes: 22139.94 INR; protected minimum: 92800. Use partial_payment, total 39660, completing 2024-09-15. Lowest projected balance: 92800.00 on 2024-09-15. Limiting expense: event_1659 (12650 on 2024-09-15). Projected income includes event_1654: 131000 on 2024-09-15. Unresolved evidence/forecast assumptions remain; see audit.`
  * expected: `Pay INR 28,820 today and the remaining INR 10,840 on 15 September 2024. This completes the full request and keeps the INR 92,800 minimum protected.`

Minimum projected balance: 92800.00

Evidence/issues:
* unresolved_evidence image_04: source unavailable or not cached; no value imputed; blocking=False
* missing_historical_amount event_1700: already in cash snapshot; recurrence/evidence unresolved; blocking=False
* irregular_history event_1700: no supported cadence for groceries; blocking=False

Candidate rejections:
* full_payment payment_option_52: payment method excluded by user; minimum balance breached on 2024-09-14: 75279.94
* wait payment_option_52: payment method excluded by user
* installments payment_option_54: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit

Inferred streams:
* event_1654: payroll credit; monthly=15; observations=5; conservative recent amount=131000
* event_1657: loan repayment; monthly=13; observations=5; conservative recent amount=11850
* event_1659: childcare contribution; monthly=15; observations=5; conservative recent amount=12650
* event_1658: clinic payment; monthly=12; observations=5; conservative recent amount=8645.36
* event_1655: residential rent payment; monthly=4; observations=5; conservative recent amount=36100
* event_1661: clothing and household items; monthly=14; observations=5; conservative recent amount=6069.58
* event_1699: transport; interval=14; observations=13; conservative recent amount=2765.93
* event_1656: municipal utilities; monthly=8; observations=5; conservative recent amount=6129.19
* event_1660: online backup subscription; monthly=14; observations=5; conservative recent amount=395

### request_20

* amount_safe_to_pay:
  * predicted: `0`
  * expected: `5400`
* decision_explanation:
  * predicted: `Safe today before changes: 0 INR; protected minimum: 64500. No safe eligible plan completes by the deadline under the resolved forecast. Limiting expense: event_1739 (2115.92 on 2026-02-13). Unresolved evidence/forecast assumptions remain; see audit. Zero capacity is an uncertified fallback for missing required financial facts.`
  * expected: `Do not make this payment by 22 February 2026. None of the available options keeps the INR 64,500 minimum protected.`

Minimum projected balance: 72300.74

Evidence/issues:
* unresolved_evidence image_05: source unavailable or not cached; no value imputed; blocking=False
* unresolved_evidence message_14: source unavailable or not cached; no value imputed; blocking=False
* missing_active_amount event_1786: debit on 2026-02-07; amount requires image interpretation; blocking=True

Candidate rejections:
* full_payment payment_option_55: unresolved active debit prevents safety certification; minimum balance breached on 2026-02-07: -231399.26
* installments payment_option_56: unresolved active debit prevents safety certification; payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit

Inferred streams:
* event_1733: payroll credit; monthly=15; observations=5; conservative recent amount=108000
* event_1783: dining; interval=21; observations=9; conservative recent amount=3803.95
* event_1737: school fee payment; monthly=7; observations=5; conservative recent amount=8740
* event_1739: cinema and events; monthly=13; observations=5; conservative recent amount=2115.92
* event_1761: groceries; interval=10; observations=18; conservative recent amount=4719.22
* event_1738: family healthcare expense; monthly=9; observations=5; conservative recent amount=6654.33
* event_1741: home association fee; monthly=2; observations=6; conservative recent amount=7950
* event_1743: household insurance; monthly=6; observations=6; conservative recent amount=3290
* event_1774: transport; interval=14; observations=13; conservative recent amount=3243.84
* event_1742: municipal utilities; monthly=5; observations=6; conservative recent amount=7769.87
* event_1740: shared storage plan; monthly=11; observations=5; conservative recent amount=365

### request_21

* amount_safe_to_pay:
  * predicted: `1574.4`
  * expected: `1543.35`
* affordability_status:
  * predicted: `affordable_now`
  * expected: `affordable_with_plan`
* earliest_date_for_full_payment:
  * predicted: `2026-04-03`
  * expected: `2026-04-15`
* spending_changes_needed:
  * predicted: `none`
  * expected: `stop:event_1815|reduce_to:event_1816:23.50`
* decision_explanation:
  * predicted: `Safe today before changes: 1574.40 USD; protected minimum: 1800. Use full_payment, total 1574.4, completing 2026-04-03. Lowest projected balance: 1877.94 on 2026-04-12. Limiting expense: event_1817 (126.38 on 2026-04-12).`
  * expected: `Stop the online backup subscription and reduce the streaming subscription to USD 23.50, then pay USD 1,574.40 today. This leaves at least USD 1,800 available.`

Minimum projected balance: 1877.94

Evidence/issues:

Candidate rejections:
* installments payment_option_58: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit
* installments payment_option_59: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit
* installments payment_option_60: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit

Inferred streams:
* event_1812: payroll credit; monthly=15; observations=5; conservative recent amount=2256
* event_1854: dining; interval=21; observations=9; conservative recent amount=98.39
* event_1836: groceries; interval=10; observations=18; conservative recent amount=97.55
* event_1818: residential rent payment; monthly=2; observations=6; conservative recent amount=718.8
* event_1817: monthly shopping spend; monthly=12; observations=5; conservative recent amount=126.38
* event_1845: transport; interval=21; observations=9; conservative recent amount=51.42
* event_1814: municipal utilities; monthly=6; observations=5; conservative recent amount=124.08
* event_1815: online backup subscription; monthly=12; observations=5; conservative recent amount=11
* event_1816: streaming subscription; monthly=9; observations=5; conservative recent amount=47

### request_22

* amount_safe_to_pay:
  * predicted: `429.68`
  * expected: `475.46`
* affordability_status:
  * predicted: `not_affordable`
  * expected: `affordable_with_plan`
* recommended_payment_method:
  * predicted: `not_recommended`
  * expected: `installments`
* payment_plan:
  * predicted: `none`
  * expected: `2024-12-08:253.59|2025-01-05:253.59|2025-02-02:253.59`
* earliest_date_for_full_payment:
  * predicted: `2025-02-15`
  * expected: `2025-01-15`
* decision_explanation:
  * predicted: `Safe today before changes: 429.68 EUR; protected minimum: 500. No safe eligible plan completes by the deadline under the resolved forecast. Baseline full payment first becomes safe on 2025-02-15, after the deadline. Limiting expense: event_1893 (23.29 on 2024-12-15). Unresolved evidence/forecast assumptions remain; see audit.`
  * expected: `Use 3 installments of EUR 253.59, starting 8 December 2024. This leaves at least EUR 500 available.`

Minimum projected balance: 929.68

Evidence/issues:
* unresolved_evidence message_15: source unavailable or not cached; no value imputed; blocking=False

Candidate rejections:
* full_payment payment_option_62: payment method excluded by user; minimum balance breached on 2024-12-05: 198.18
* wait payment_option_62: payment outside request/deadline/forecast bounds; payment method excluded by user
* partial_payment : payment outside request/deadline/forecast bounds; payment method excluded by user
* installments payment_option_61: minimum balance breached on 2025-02-11: 421.04
* installments payment_option_63: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit

Inferred streams:
* event_1887: payroll credit; monthly=15; observations=5; conservative recent amount=616
* event_1958: dining; interval=14; observations=13; conservative recent amount=18.41
* event_1893: weekend entertainment; monthly=15; observations=5; conservative recent amount=23.29
* event_1920: groceries; interval=7; observations=26; conservative recent amount=26.82
* event_1894: apartment rent transfer; monthly=3; observations=6; conservative recent amount=178.2
* event_1945: transport; interval=7; observations=25; conservative recent amount=15.87
* event_1889: electricity and water bill; monthly=7; observations=5; conservative recent amount=31.52
* event_1891: food delivery membership; monthly=14; observations=5; conservative recent amount=5
* event_1892: gym membership; monthly=11; observations=5; conservative recent amount=17
* event_1890: music service subscription; monthly=12; observations=5; conservative recent amount=6

### request_23

* amount_safe_to_pay:
  * predicted: `2791.91`
  * expected: `9152`
* affordability_status:
  * predicted: `affordable_with_plan`
  * expected: `affordable_later`
* earliest_date_for_full_payment:
  * predicted: ``
  * expected: `2025-07-15`
* spending_changes_needed:
  * predicted: `stop:event_2000`
  * expected: `none`
* decision_explanation:
  * predicted: `Safe today before changes: 2791.91 ZAR; protected minimum: 27000. Use wait, total 38016, completing 2025-07-15. Lowest projected balance: 27754.50 on 2025-08-04. Required changes: stop:event_2000. Earlier full payment would not preserve the reserve under this forecast. Limiting expense: event_2002 (15312 on 2025-08-04). Projected income includes event_1994: 45760 on 2025-05-15. Unresolved evidence/forecast assumptions remain; see audit.`
  * expected: `Pay ZAR 38,016 in full on 15 July 2025. Paying earlier would take the balance below the ZAR 27,000 minimum.`

Minimum projected balance: 27754.50

Evidence/issues:
* unresolved_evidence message_16: source unavailable or not cached; no value imputed; blocking=False

Candidate rejections:
* full_payment payment_option_64: minimum balance breached on 2025-05-07: -8224.09
* installments payment_option_65: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit
* installments payment_option_66: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit

Inferred streams:
* event_1994: payroll credit; monthly=15; observations=5; conservative recent amount=45760
* event_1997: education loan instalment; monthly=13; observations=5; conservative recent amount=5852
* event_1999: childcare contribution; monthly=15; observations=5; conservative recent amount=4270.2
* event_2027: groceries; interval=7; observations=25; conservative recent amount=1678.37
* event_1998: clinic payment; monthly=12; observations=5; conservative recent amount=1439.91
* event_2002: shared housing rent; monthly=4; observations=6; conservative recent amount=15312
* event_2001: personal shopping; monthly=14; observations=5; conservative recent amount=1389.39
* event_2040: transport; interval=14; observations=13; conservative recent amount=1092.98
* event_1996: electricity bill; monthly=8; observations=5; conservative recent amount=2915.67
* event_2000: cloud storage plan; monthly=14; observations=5; conservative recent amount=295.9

### request_24

* amount_safe_to_pay:
  * predicted: `12369.96`
  * expected: `13420`
* decision_explanation:
  * predicted: `Safe today before changes: 12369.96 INR; protected minimum: 51000. No safe eligible plan completes by the deadline under the resolved forecast. Available methods are excluded by the user. Limiting expense: event_2082 (1916.16 on 2026-01-13). Unresolved evidence/forecast assumptions remain; see audit.`
  * expected: `Do not proceed with the INR 109,600 request. Although INR 13,420 is available today, the full amount cannot be completed safely within 90 days.`

Minimum projected balance: 63369.96

Evidence/issues:
* unresolved_evidence message_17: source unavailable or not cached; no value imputed; blocking=False

Candidate rejections:
* full_payment payment_option_67: payment method excluded by user; minimum balance breached on 2026-01-04: -46230.04
* installments payment_option_68: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit

Inferred streams:
* event_2075: payroll credit; monthly=15; observations=5; conservative recent amount=61000
* event_2163: dining; interval=7; observations=26; conservative recent amount=2184.47
* event_2082: local event tickets; monthly=13; observations=5; conservative recent amount=1916.16
* event_2101: groceries; interval=10; observations=18; conservative recent amount=2321.31
* event_2078: insurance policy payment; monthly=6; observations=5; conservative recent amount=2510
* event_2083: landlord standing order; monthly=1; observations=6; conservative recent amount=18600
* event_2081: monthly shopping spend; monthly=11; observations=5; conservative recent amount=2680.78
* event_2137: transport; interval=5; observations=36; conservative recent amount=1593.41
* event_2077: household utility payment; monthly=5; observations=5; conservative recent amount=3490.5
* event_2079: online backup subscription; monthly=11; observations=5; conservative recent amount=355
* event_2080: family streaming plan; monthly=8; observations=5; conservative recent amount=1200

### request_25

* amount_safe_to_pay:
  * predicted: `0`
  * expected: `1425000`
* decision_explanation:
  * predicted: `Safe today before changes: 0 IDR; protected minimum: 23379100. No safe eligible plan completes by the deadline under the resolved forecast. Limiting expense: event_2261 (729004.44 on 2024-03-15).`
  * expected: `Do not make this payment by 17 April 2024. None of the available options keeps the IDR 23,379,100 minimum protected.`

Minimum projected balance: 22245558.61

Evidence/issues:

Candidate rejections:
* full_payment payment_option_69: minimum balance breached on 2024-03-06: -38250441.39
* installments payment_option_70: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit
* installments payment_option_71: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit

Inferred streams:
* event_2199: international employer payroll; monthly=15; observations=5; conservative recent amount=1800
* event_2286: dining; interval=7; observations=25; conservative recent amount=1133036.68
* event_2206: games and recreation; monthly=14; observations=5; conservative recent amount=504697.37
* event_2225: groceries; interval=10; observations=18; conservative recent amount=1472349.1
* event_2202: insurance policy payment; monthly=7; observations=5; conservative recent amount=904400
* event_2207: monthly rent; monthly=2; observations=6; conservative recent amount=6954000
* event_2205: monthly shopping spend; monthly=12; observations=5; conservative recent amount=1170271.29
* event_2261: transport; interval=5; observations=36; conservative recent amount=729004.44
* event_2201: household utility payment; monthly=6; observations=5; conservative recent amount=1341541.39
* event_2203: cloud storage plan; monthly=12; observations=5; conservative recent amount=126350
* event_2204: video streaming plan; monthly=9; observations=5; conservative recent amount=573800


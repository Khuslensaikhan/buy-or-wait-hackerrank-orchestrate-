# Offline agent sample evaluation

Cached evidence only; flexible spending search enabled. Cache misses remain unresolved.
Normalized equality parses decimals and schedules exactly; there is no tolerance.
Explanation accuracy is exact text equality, not semantic grading.

| Field | Normalized correct | Exact text correct |
|---|---:|---:|
| request_id | 25/25 (100%) | 25/25 (100%) |
| amount_safe_to_pay | 2/25 (8%) | 2/25 (8%) |
| affordability_status | 19/25 (76%) | 19/25 (76%) |
| recommended_payment_method | 21/25 (84%) | 21/25 (84%) |
| payment_plan | 21/25 (84%) | 18/25 (72%) |
| earliest_date_for_full_payment | 16/25 (64%) | 16/25 (64%) |
| spending_changes_needed | 20/25 (80%) | 20/25 (80%) |
| decision_explanation | 0/25 (0%) | 0/25 (0%) |

All fields correct: 0/25.
All operational fields excluding explanation: 2/25.
Exact-text full rows: 0/25.

## Mismatch table

| Request | Safe amount: predicted / expected | Method: predicted / expected | Incorrect fields |
|---|---|---|---|
| request_01 | 25256 / 25256 | full_payment / full_payment | E |
| request_02 | 17038593.76 / 17229139.2 | installments / installments | A, E |
| request_03 | 971736.98 / 873000 | wait / wait | A, E |
| request_04 | 9109811.57 / 8401800 | wait / wait | A, E |
| request_05 | 0 / 737 | not_recommended / not_recommended | A, E |
| request_06 | 488.79 / 603.3 | not_recommended / full_payment | A, S, M, P, D, C, E |
| request_07 | 86237.19 / 87170.56 | installments / installments | A, E |
| request_08 | 285.18 / 284.57 | wait / wait | A, S, D, C, E |
| request_09 | 30.66 / 166.61 | not_recommended / full_payment | A, S, M, P, D, E |
| request_10 | 0 / 12700 | not_recommended / not_recommended | A, E |
| request_11 | 12319866.6 / 12510645 | full_payment / full_payment | A, D, C, E |
| request_12 | 60370.2 / 65164 | installments / installments | A, D, C, E |
| request_13 | 445.78 / 433.4 | not_recommended / wait | A, S, M, P, D, E |
| request_14 | 0 / 597.74 | not_recommended / not_recommended | A, E |
| request_15 | 0 / 83.05 | not_recommended / not_recommended | A, E |
| request_16 | 122500 / 122500 | full_payment / full_payment | E |
| request_17 | 243023.67 / 243849.58 | installments / installments | A, D, E |
| request_18 | 460.38 / 462 | wait / wait | A, E |
| request_19 | 12526.12 / 28820 | not_recommended / partial_payment | A, S, M, P, D, E |
| request_20 | 8969.66 / 5400 | not_recommended / not_recommended | A, E |
| request_21 | 1574.4 / 1543.35 | full_payment / full_payment | A, S, D, C, E |
| request_22 | 443.71 / 475.46 | installments / installments | A, E |
| request_23 | 3201.52 / 9152 | wait / wait | A, E |
| request_24 | 13539.25 / 13420 | not_recommended / not_recommended | A, E |
| request_25 | 0 / 1425000 | not_recommended / not_recommended | A, E |

A=safe amount; S=status; M=method; P=plan; D=earliest date; C=spending changes; E=explanation.

## Detailed diagnostics

### request_01

* decision_explanation:
  * predicted: `Safe today before changes: 25256.00 ZAR; protected minimum: 18000. Use full_payment, total 25256, completing 2024-03-03. Lowest projected balance: 22200.13 on 2024-03-15. Limiting expense: event_58 (785.14 on 2024-03-15).`
  * expected: `Pay ZAR 25,256 today. This leaves at least ZAR 18,000 available over the next 90 days.`

Minimum projected balance: 22200.13

Evidence/issues:

Candidate rejections:
* installments payment_option_02: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit
* installments payment_option_03: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit
* installments payment_option_04: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit

Inferred streams:
* event_25: next confirmed salary; monthly=15; observations=1; supported salary rate=23320
* event_29: education loan instalment; monthly=11; observations=5; latest contractual amount=3487
* event_97: dining; interval=14; observations=13; mean historical budget, rounded up=1089.19
* event_28: professional training fee; monthly=8; observations=5; latest contractual amount=1821.6
* event_58: groceries; interval=7; observations=26; mean historical budget, rounded up=785.14
* event_32: apartment rent transfer; monthly=2; observations=6; latest contractual amount=5148
* event_84: transport; interval=7; observations=26; mean historical budget, rounded up=439.20
* event_27: household utility payment; monthly=6; observations=5; mean historical budget, rounded up=1507.80
* event_31: delivery service plan; monthly=13; observations=5; latest contractual amount=306.9
* event_30: music service subscription; monthly=11; observations=5; latest contractual amount=235.4

### request_02

* amount_safe_to_pay:
  * predicted: `17038593.76`
  * expected: `17229139.2`
* decision_explanation:
  * predicted: `Safe today before changes: 17038593.76 IDR; protected minimum: 29158400. Use installments, total 47858720.01, completing 2025-10-07. Lowest projected balance: 30244087.09 on 2025-08-15. Limiting expense: event_142 (1298171.70 on 2025-08-15). Projected income includes event_136: 42750000 on 2025-08-15.`
  * expected: `Use 3 installments of IDR 15,952,906.67, starting 8 August 2025. This leaves at least IDR 29,158,400 available.`

Minimum projected balance: 30244087.09

Evidence/issues:

Candidate rejections:
* full_payment payment_option_06: payment method excluded by user; minimum balance breached on 2025-08-05: 178993.76
* wait payment_option_06: payment method excluded by user
* partial_payment : partial payment not permitted or no strictly partial capacity
* installments payment_option_07: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit

Inferred streams:
* event_136: payroll credit; monthly=15; observations=5; supported salary rate=33345000
* event_184: dining; interval=21; observations=9; mean historical budget, rounded up=1083819.46
* event_140: course tuition; monthly=9; observations=5; latest contractual amount=3040000
* event_142: cinema and events; monthly=15; observations=5; mean historical budget, rounded up=1298171.70
* event_162: groceries; interval=10; observations=18; mean historical budget, rounded up=1908881.31
* event_141: clinic payment; monthly=11; observations=5; mean historical budget, rounded up=1538993.98
* event_144: home repair reserve; monthly=4; observations=6; latest contractual amount=3534000
* event_139: household insurance; monthly=8; observations=5; latest contractual amount=1132400
* event_175: transport; interval=14; observations=13; mean historical budget, rounded up=1211967.95
* event_138: municipal utilities; monthly=7; observations=5; mean historical budget, rounded up=2035830.50
* event_143: shared storage plan; monthly=13; observations=5; latest contractual amount=369550

### request_03

* amount_safe_to_pay:
  * predicted: `971736.98`
  * expected: `873000`
* decision_explanation:
  * predicted: `Safe today before changes: 971736.98 IDR; protected minimum: 2668700. Use wait, total 5491000, completing 2019-11-15. Lowest projected balance: 3640436.98 on 2019-09-14. Earlier full payment would not preserve the reserve under this forecast. Limiting expense: event_216 (168697.75 on 2019-09-14). Projected income includes event_210: 4365000 on 2019-09-15. Unresolved evidence/forecast assumptions remain; see audit.`
  * expected: `Pay IDR 5,491,000 in full on 15 November 2019. Paying earlier would take the balance below the IDR 2,668,700 minimum.`

Minimum projected balance: 3640436.98

Evidence/issues:
* rejected_fact message_02: low confidence; requires review; blocking=False

Candidate rejections:
* full_payment payment_option_08: minimum balance breached on 2019-09-03: -1850563.02
* partial_payment : partial payment not permitted or no strictly partial capacity
* installments payment_option_09: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit
* installments payment_option_10: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit

Inferred streams:
* event_210: payroll credit; monthly=15; observations=5; supported salary rate=4365000
* event_252: dining; interval=21; observations=9; mean historical budget, rounded up=149912.66
* event_234: groceries; interval=10; observations=18; mean historical budget, rounded up=193164.79
* event_212: landlord standing order; monthly=4; observations=5; latest contractual amount=1140000
* event_216: clothing and household items; monthly=14; observations=5; mean historical budget, rounded up=168697.75
* event_243: transport; interval=21; observations=9; mean historical budget, rounded up=91041.07
* event_213: water and power payment; monthly=8; observations=5; mean historical budget, rounded up=284387.82
* event_214: shared storage plan; monthly=14; observations=5; latest contractual amount=20900
* event_215: video streaming plan; monthly=11; observations=5; latest contractual amount=117800

### request_04

* amount_safe_to_pay:
  * predicted: `9109811.57`
  * expected: `8401800`
* decision_explanation:
  * predicted: `Safe today before changes: 9109811.57 IDR; protected minimum: 30686600. Use wait, total 12693000, completing 2024-06-15. Lowest projected balance: 34216559.43 on 2024-07-14. Earlier full payment would not preserve the reserve under this forecast. Limiting expense: event_343 (832507.42 on 2024-07-14). Projected income includes event_284: 38190000 on 2024-06-15. Unresolved evidence/forecast assumptions remain; see audit.`
  * expected: `Wait until 15 June 2024, then pay IDR 12,693,000 in full. Paying sooner would put the IDR 30,686,600 minimum at risk.`

Minimum projected balance: 34216559.43

Evidence/issues:
* incomplete_new_fact message_03: new event requires explicit description/category/direction/type/currency/date/status; blocking=False

Candidate rejections:
* full_payment payment_option_11: minimum balance breached on 2024-06-11: 27103411.57
* partial_payment : payment method excluded by user
* installments payment_option_12: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit

Inferred streams:
* event_284: payroll credit; monthly=15; observations=5; supported salary rate=38190000
* event_356: dining; interval=14; observations=13; mean historical budget, rounded up=1748635.07
* event_290: local event tickets; monthly=13; observations=5; mean historical budget, rounded up=1385201.36
* event_317: groceries; interval=7; observations=26; mean historical budget, rounded up=1499474.48
* event_291: residential rent payment; monthly=1; observations=6; latest contractual amount=12293000
* event_343: transport; interval=7; observations=26; mean historical budget, rounded up=832507.42
* event_286: municipal utilities; monthly=5; observations=5; mean historical budget, rounded up=2003395.62
* event_288: food delivery membership; monthly=12; observations=5; latest contractual amount=377150
* event_289: gym membership; monthly=9; observations=5; latest contractual amount=1027900
* event_287: music service subscription; monthly=10; observations=5; latest contractual amount=332500

### request_05

* amount_safe_to_pay:
  * predicted: `0`
  * expected: `737`
* decision_explanation:
  * predicted: `Safe today before changes: 0 ZAR; protected minimum: 13100. No safe eligible plan completes by the deadline under the resolved forecast. Limiting expense: event_437 (414.35 on 2026-02-04). Unresolved evidence/forecast assumptions remain; see audit.`
  * expected: `Do not make this payment by 12 January 2026. None of the available options keeps the ZAR 13,100 minimum protected.`

Minimum projected balance: 8160.61

Evidence/issues:
* stale_recurrence event_382: payroll credit: expected next occurrence 2025-10-15 already overdue; blocking=False

Candidate rejections:
* full_payment payment_option_13: minimum balance breached on 2025-12-16: -7327.39
* installments payment_option_14: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit
* installments payment_option_15: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit

Inferred streams:
* event_393: vehicle loan payment; monthly=11; observations=5; latest contractual amount=968
* event_395: dependent care payment; monthly=13; observations=5; mean historical budget, rounded up=840.40
* event_424: groceries; interval=7; observations=26; mean historical budget, rounded up=721.71
* event_394: therapy appointment; monthly=10; observations=5; mean historical budget, rounded up=699.01
* event_398: apartment rent transfer; monthly=2; observations=6; latest contractual amount=4972
* event_397: personal shopping; monthly=12; observations=5; mean historical budget, rounded up=397.85
* event_437: transport; interval=14; observations=13; mean historical budget, rounded up=414.35
* event_392: municipal utilities; monthly=6; observations=5; mean historical budget, rounded up=686.71
* event_396: cloud storage plan; monthly=12; observations=5; latest contractual amount=113.3

### request_06

* amount_safe_to_pay:
  * predicted: `488.79`
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
  * predicted: `2026-02-15`
  * expected: `2026-01-15`
* spending_changes_needed:
  * predicted: `none`
  * expected: `stop:event_476`
* decision_explanation:
  * predicted: `Safe today before changes: 488.79 EUR; protected minimum: 800. No safe eligible plan completes by the deadline under the resolved forecast. Baseline full payment first becomes safe on 2026-02-15, after the deadline. Limiting expense: event_478 (35.02 on 2026-01-15). Unresolved evidence/forecast assumptions remain; see audit.`
  * expected: `Stop the family streaming plan, then pay EUR 620.40 today. This leaves at least EUR 800 available.`

Minimum projected balance: 1288.79

Evidence/issues:
* incomplete_new_fact message_04: new event requires explicit description/category/direction/type/currency/date/status; blocking=False

Candidate rejections:
* full_payment payment_option_16: minimum balance breached on 2026-01-11: 668.39
* wait payment_option_16: payment outside request/deadline/forecast bounds
* partial_payment : payment outside request/deadline/forecast bounds; partial payment not permitted or no strictly partial capacity
* installments payment_option_17: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit
* installments payment_option_18: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit

Inferred streams:
* event_471: payroll credit; monthly=15; observations=5; supported salary rate=1037.52
* event_556: dining; interval=7; observations=25; mean historical budget, rounded up=45.88
* event_478: monthly entertainment spend; monthly=15; observations=5; mean historical budget, rounded up=35.02
* event_496: groceries; interval=10; observations=18; mean historical budget, rounded up=45.08
* event_474: vehicle insurance premium; monthly=8; observations=5; latest contractual amount=26
* event_472: monthly rent; monthly=3; observations=5; latest contractual amount=254.1
* event_477: household shopping; monthly=13; observations=5; mean historical budget, rounded up=41.00
* event_531: transport; interval=5; observations=35; mean historical budget, rounded up=26.98
* event_473: water and power payment; monthly=7; observations=5; mean historical budget, rounded up=55.71
* event_475: shared storage plan; monthly=13; observations=5; latest contractual amount=5
* event_476: family streaming plan; monthly=10; observations=5; latest contractual amount=19

### request_07

* amount_safe_to_pay:
  * predicted: `86237.19`
  * expected: `87170.56`
* decision_explanation:
  * predicted: `Safe today before changes: 86237.19 INR; protected minimum: 93000. Use installments, total 205296, completing 2024-11-07. Lowest projected balance: 93627.61 on 2024-11-22. Limiting expense: event_605 (3220.14 on 2024-11-22). Projected income includes event_578_next: 149000 on 2024-09-23.`
  * expected: `Use 3 installments of INR 68,432, starting 12 September 2024. This leaves at least INR 93,000 available.`

Minimum projected balance: 93627.61

Evidence/issues:

Candidate rejections:
* full_payment payment_option_20: payment method excluded by user; minimum balance breached on 2024-09-05: -18162.81
* wait payment_option_20: payment method excluded by user
* partial_payment : payment method excluded by user
* installments payment_option_21: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit

Inferred streams:
* event_578: payroll credit; monthly=23; observations=5; supported salary rate=149000
* event_581: personal loan payment; monthly=13; observations=5; latest contractual amount=15650
* event_614: dining; interval=21; observations=9; mean historical budget, rounded up=5927.32
* event_596: groceries; interval=14; observations=13; mean historical budget, rounded up=7116.46
* event_583: monthly rent; monthly=4; observations=6; latest contractual amount=34200
* event_605: transport; interval=21; observations=9; mean historical budget, rounded up=3220.14
* event_580: electricity bill; monthly=8; observations=5; mean historical budget, rounded up=6789.45
* event_582: music subscription; monthly=13; observations=5; latest contractual amount=1005

### request_08

* amount_safe_to_pay:
  * predicted: `285.18`
  * expected: `284.57`
* affordability_status:
  * predicted: `affordable_with_plan`
  * expected: `affordable_later`
* earliest_date_for_full_payment:
  * predicted: ``
  * expected: `2025-04-15`
* spending_changes_needed:
  * predicted: `stop:event_649|reduce_to:event_716:27.35`
  * expected: `none`
* decision_explanation:
  * predicted: `Safe today before changes: 285.18 EUR; protected minimum: 800. Use wait, total 996.6, completing 2025-04-15. Lowest projected balance: 800.06 on 2025-05-08. Required changes: stop:event_649; reduce_to:event_716:27.35. Earlier full payment would not preserve the reserve under this forecast. Limiting expense: event_716 (50.85 on 2025-05-08). Projected income includes event_643_next: 1422.85 on 2025-02-15.`
  * expected: `Pay EUR 996.60 in full on 15 April 2025. Paying earlier would take the balance below the EUR 800 minimum.`

Minimum projected balance: 800.06

Evidence/issues:

Candidate rejections:
* full_payment payment_option_22: minimum balance breached on 2025-02-07: 88.58
* installments payment_option_23: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit

Inferred streams:
* event_643: payroll credit; monthly=15; observations=5; supported salary rate=1422.85
* event_647: personal loan payment; monthly=10; observations=5; latest contractual amount=177
* event_716: dining; interval=14; observations=13; mean historical budget, rounded up=50.85
* event_646: school fee payment; monthly=7; observations=5; latest contractual amount=89
* event_677: groceries; interval=7; observations=26; mean historical budget, rounded up=59.05
* event_650: apartment rent transfer; monthly=1; observations=6; latest contractual amount=467.5
* event_703: transport; interval=7; observations=26; mean historical budget, rounded up=37.49
* event_651: municipal utilities; monthly=5; observations=6; mean historical budget, rounded up=76.83
* event_649: grocery delivery membership; monthly=12; observations=5; latest contractual amount=24
* event_648: music subscription; monthly=10; observations=5; latest contractual amount=14

### request_09

* amount_safe_to_pay:
  * predicted: `30.66`
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
  * predicted: `Safe today before changes: 30.66 EUR; protected minimum: 600. No safe eligible plan completes by the deadline under the resolved forecast. Limiting expense: event_752 (211.2 on 2026-10-02).`
  * expected: `Pay EUR 166.61 today. This keeps the EUR 600 minimum available over the next 90 days.`

Minimum projected balance: 630.66

Evidence/issues:

Candidate rejections:
* full_payment payment_option_24: minimum balance breached on 2026-10-02: 464.05
* installments payment_option_25: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit
* installments payment_option_26: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit

Inferred streams:
* event_788: dining; interval=21; observations=9; mean historical budget, rounded up=30.30
* event_770: groceries; interval=10; observations=18; mean historical budget, rounded up=44.57
* event_752: monthly rent; monthly=2; observations=6; latest contractual amount=211.2
* event_751: household shopping; monthly=12; observations=5; mean historical budget, rounded up=26.64
* event_779: transport; interval=21; observations=9; mean historical budget, rounded up=24.12
* event_748: water and power payment; monthly=6; observations=5; mean historical budget, rounded up=64.37
* event_749: cloud storage plan; monthly=12; observations=5; latest contractual amount=5
* event_750: video streaming plan; monthly=9; observations=5; latest contractual amount=20

### request_10

* amount_safe_to_pay:
  * predicted: `0`
  * expected: `12700`
* decision_explanation:
  * predicted: `Safe today before changes: 0 INR; protected minimum: 225400. No safe eligible plan completes by the deadline under the resolved forecast. Limiting expense: event_866 (10776.08 on 2025-03-06). Unresolved evidence/forecast assumptions remain; see audit.`
  * expected: `Do not make this payment by 10 February 2025. None of the available options keeps the INR 225,400 minimum protected.`

Minimum projected balance: 178050.49

Evidence/issues:
* incomplete_new_fact message_07: new event requires explicit description/category/direction/type/currency/date/status; blocking=False

Candidate rejections:
* full_payment payment_option_27: payment method excluded by user; minimum balance breached on 2025-01-16: -88649.51
* installments payment_option_28: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit

Inferred streams:
* event_904: dining; interval=14; observations=13; mean historical budget, rounded up=8837.77
* event_838: cinema and events; monthly=15; observations=5; mean historical budget, rounded up=4645.20
* event_866: groceries; interval=7; observations=26; mean historical budget, rounded up=10776.08
* event_840: monthly rent; monthly=3; observations=6; latest contractual amount=69100
* event_891: transport; interval=7; observations=25; mean historical budget, rounded up=5982.80
* event_834: electricity and water bill; monthly=7; observations=5; mean historical budget, rounded up=17103.95
* event_836: delivery service plan; monthly=14; observations=5; latest contractual amount=1895
* event_837: community fitness plan; monthly=11; observations=5; latest contractual amount=4860
* event_835: music subscription; monthly=12; observations=5; latest contractual amount=2800

### request_11

* amount_safe_to_pay:
  * predicted: `12319866.6`
  * expected: `12510645`
* earliest_date_for_full_payment:
  * predicted: `2025-06-15`
  * expected: `2025-07-15`
* spending_changes_needed:
  * predicted: `stop:event_949|reduce_to:event_989:728039.15`
  * expected: `reduce_to:event_989:665950`
* decision_explanation:
  * predicted: `Safe today before changes: 12319866.60 IDR; protected minimum: 34140600. Use full_payment, total 13110000, completing 2025-05-03. Lowest projected balance: 34140600.00 on 2025-05-14. Required changes: stop:event_949; reduce_to:event_989:728039.15. Limiting expense: event_989 (1350022.55 on 2025-05-14). Unresolved evidence/forecast assumptions remain; see audit.`
  * expected: `Reduce the weekend food delivery to IDR 665,950, then pay IDR 13,110,000 today. This leaves at least IDR 34,140,600 available.`

Minimum projected balance: 34140600.00

Evidence/issues:
* rejected_fact message_08: low confidence; requires review; blocking=False

Candidate rejections:
* full_payment payment_option_29: minimum balance breached on 2025-05-14: 33350466.60
* wait payment_option_29: payment outside request/deadline/forecast bounds
* partial_payment : payment outside request/deadline/forecast bounds; payment method excluded by user; partial payment not permitted or no strictly partial capacity
* installments payment_option_30: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit
* installments payment_option_31: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit
* installments payment_option_32: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit

Inferred streams:
* event_941: base salary; monthly=15; observations=5; supported salary rate=23256000
* event_989: dining; interval=21; observations=9; mean historical budget, rounded up=1350022.55
* event_946: child education fee; monthly=10; observations=5; latest contractual amount=2544100
* event_948: games and recreation; monthly=16; observations=5; mean historical budget, rounded up=1600926.76
* event_967: groceries; interval=10; observations=18; mean historical budget, rounded up=1421333.17
* event_947: regular medicine purchase; monthly=12; observations=5; mean historical budget, rounded up=2943993.43
* event_943: home association fee; monthly=5; observations=5; latest contractual amount=2954500
* event_945: vehicle insurance premium; monthly=9; observations=5; latest contractual amount=1881000
* event_980: transport; interval=14; observations=13; mean historical budget, rounded up=1088014.14
* event_944: municipal utilities; monthly=8; observations=5; mean historical budget, rounded up=2720215.11
* event_949: cloud storage plan; monthly=14; observations=5; latest contractual amount=168150

### request_12

* amount_safe_to_pay:
  * predicted: `60370.2`
  * expected: `65164`
* earliest_date_for_full_payment:
  * predicted: ``
  * expected: `2026-04-05`
* spending_changes_needed:
  * predicted: `stop:event_1016|reduce_to:event_1054:1536.1`
  * expected: `none`
* decision_explanation:
  * predicted: `Safe today before changes: 60370.20 ZAR; protected minimum: 43200. Use installments, total 67770.57, completing 2026-06-20. Lowest projected balance: 43200.03 on 2026-07-01. Required changes: stop:event_1016; reduce_to:event_1054:1536.10. Limiting expense: event_1018 (11792 on 2026-07-01).`
  * expected: `Use 3 installments of ZAR 22,590.19, starting 19 April 2026. This leaves at least ZAR 43,200 available.`

Minimum projected balance: 43200.03

Evidence/issues:

Candidate rejections:
* full_payment payment_option_34: payment method excluded by user; minimum balance breached on 2026-07-01: 38406.20
* installments payment_option_33: minimum balance breached on 2026-07-01: 35799.63
* installments payment_option_35: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit

Inferred streams:
* event_1054: dining; interval=21; observations=9; mean historical budget, rounded up=2257.60
* event_1036: groceries; interval=10; observations=18; mean historical budget, rounded up=2134.89
* event_1018: monthly rent; monthly=1; observations=6; latest contractual amount=11792
* event_1017: monthly shopping spend; monthly=11; observations=5; mean historical budget, rounded up=1255.89
* event_1045: transport; interval=21; observations=9; mean historical budget, rounded up=1436.23
* event_1014: water and power payment; monthly=5; observations=5; mean historical budget, rounded up=3509.73
* event_1015: shared storage plan; monthly=11; observations=5; latest contractual amount=447.7
* event_1016: family streaming plan; monthly=8; observations=5; latest contractual amount=1504.8

### request_13

* amount_safe_to_pay:
  * predicted: `445.78`
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
  * predicted: `Safe today before changes: 445.78 EUR; protected minimum: 1300. No safe eligible plan completes by the deadline under the resolved forecast. Limiting expense: event_1147 (44.83 on 2024-05-15).`
  * expected: `Pay EUR 941.60 in full on 15 May 2024. Paying earlier would take the balance below the EUR 1,300 minimum.`

Minimum projected balance: 1745.78

Evidence/issues:

Candidate rejections:
* full_payment payment_option_36: minimum balance breached on 2024-04-11: 804.18
* installments payment_option_37: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit
* installments payment_option_38: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit

Inferred streams:
* event_1087: primary household salary; monthly=15; observations=5; supported salary rate=1343.54
* event_1160: dining; interval=14; observations=13; mean historical budget, rounded up=64.28
* event_1093: local event tickets; monthly=14; observations=5; mean historical budget, rounded up=32.96
* event_1121: groceries; interval=7; observations=26; mean historical budget, rounded up=99.67
* event_1094: shared housing rent; monthly=2; observations=6; latest contractual amount=622.6
* event_1147: transport; interval=7; observations=26; mean historical budget, rounded up=44.83
* event_1095: water and power payment; monthly=6; observations=6; mean historical budget, rounded up=143.67
* event_1091: delivery service plan; monthly=13; observations=5; latest contractual amount=21
* event_1092: community fitness plan; monthly=10; observations=5; latest contractual amount=61
* event_1090: music subscription; monthly=11; observations=5; latest contractual amount=29

### request_14

* amount_safe_to_pay:
  * predicted: `0`
  * expected: `597.74`
* decision_explanation:
  * predicted: `Safe today before changes: 0 EUR; protected minimum: 2200. No safe eligible plan completes by the deadline under the resolved forecast. Available methods are excluded by the user. Limiting expense: event_1226 (104.80 on 2025-11-02). Unresolved evidence/forecast assumptions remain; see audit. Zero capacity is an uncertified fallback for missing required financial facts.`
  * expected: `Do not proceed with the EUR 5,414.20 request. Although EUR 597.74 is available today, the full amount cannot be completed safely within 90 days.`

Minimum projected balance: -1993.08

Evidence/issues:
* incomplete_new_fact message_10: new event requires explicit description/category/direction/type/currency/date/status; blocking=True

Candidate rejections:
* full_payment payment_option_39: unresolved active debit prevents safety certification; payment method excluded by user; minimum balance breached on 2025-08-04: -7407.28
* installments payment_option_40: unresolved active debit prevents safety certification; payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit

Inferred streams:
* event_1195: credit card repayment; monthly=12; observations=5; latest contractual amount=350
* event_1197: family support payment; monthly=14; observations=5; mean historical budget, rounded up=226.00
* event_1226: groceries; interval=7; observations=26; mean historical budget, rounded up=104.80
* event_1196: family healthcare expense; monthly=11; observations=5; mean historical budget, rounded up=91.91
* event_1200: monthly rent; monthly=3; observations=6; latest contractual amount=688.6
* event_1199: online retail purchases; monthly=13; observations=5; mean historical budget, rounded up=129.47
* event_1239: transport; interval=14; observations=13; mean historical budget, rounded up=51.07
* event_1194: energy provider bill; monthly=7; observations=5; mean historical budget, rounded up=148.22
* event_1198: cloud storage plan; monthly=13; observations=5; latest contractual amount=14

### request_15

* amount_safe_to_pay:
  * predicted: `0`
  * expected: `83.05`
* decision_explanation:
  * predicted: `Safe today before changes: 0 EUR; protected minimum: 1200. No safe eligible plan completes by the deadline under the resolved forecast. Available methods are excluded by the user. Limiting expense: event_1271 (27 on 2026-01-15).`
  * expected: `Do not make this payment by 1 February 2026. None of the available options keeps the EUR 1,200 minimum protected.`

Minimum projected balance: 1178.07

Evidence/issues:

Candidate rejections:
* full_payment payment_option_41: payment method excluded by user; minimum balance breached on 2026-01-06: -2506.93
* installments payment_option_42: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit
* installments payment_option_43: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit

Inferred streams:
* event_1265: first-job payroll; monthly=15; observations=2; supported salary rate=1661
* event_1269: credit card repayment; monthly=13; observations=5; latest contractual amount=84
* event_1335: dining; interval=14; observations=13; mean historical budget, rounded up=40.84
* event_1268: school fee payment; monthly=10; observations=5; latest contractual amount=159
* event_1297: groceries; interval=7; observations=25; mean historical budget, rounded up=60.11
* event_1272: landlord standing order; monthly=4; observations=6; latest contractual amount=435.6
* event_1322: transport; interval=7; observations=25; mean historical budget, rounded up=31.76
* event_1267: energy provider bill; monthly=8; observations=5; mean historical budget, rounded up=86.40
* event_1271: food delivery membership; monthly=15; observations=5; latest contractual amount=27
* event_1270: music subscription; monthly=13; observations=5; latest contractual amount=11

### request_16

* decision_explanation:
  * predicted: `Safe today before changes: 122500.00 INR; protected minimum: 122400. Use full_payment, total 122500, completing 2023-08-12. Lowest projected balance: 133708.45 on 2023-09-15. Limiting expense: event_1441 (5302.32 on 2023-09-15).`
  * expected: `Pay INR 122,500 today. This leaves at least INR 122,400 available over the next 90 days.`

Minimum projected balance: 133708.45

Evidence/issues:

Candidate rejections:
* installments payment_option_45: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit
* installments payment_option_46: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit

Inferred streams:
* event_1364: payroll credit; monthly=15; observations=5; supported salary rate=173000
* event_1373: vehicle loan payment; monthly=10; observations=6; latest contractual amount=17750
* event_1441: dining; interval=14; observations=13; mean historical budget, rounded up=5302.32
* event_1402: groceries; interval=7; observations=26; mean historical budget, rounded up=7060.64
* event_1371: monthly rent; monthly=1; observations=6; latest contractual amount=57100
* event_1376: clothing and household items; monthly=11; observations=6; mean historical budget, rounded up=9179.85
* event_1428: transport; interval=7; observations=26; mean historical budget, rounded up=4419.42
* event_1372: energy provider bill; monthly=5; observations=6; mean historical budget, rounded up=10407.44
* event_1375: cloud storage plan; monthly=11; observations=6; latest contractual amount=1055
* event_1374: video streaming plan; monthly=8; observations=6; latest contractual amount=3510

### request_17

* amount_safe_to_pay:
  * predicted: `243023.67`
  * expected: `243849.58`
* earliest_date_for_full_payment:
  * predicted: `2026-04-15`
  * expected: `2026-03-15`
* decision_explanation:
  * predicted: `Safe today before changes: 243023.67 INR; protected minimum: 166100. Use installments, total 285584.01, completing 2026-04-30. Lowest projected balance: 174876.82 on 2026-05-15. Limiting expense: event_1503 (9096.70 on 2026-05-15). Projected income includes event_1546: 206000 on 2026-03-15.`
  * expected: `Use 3 installments of INR 95,194.67, starting 1 March 2026. This leaves at least INR 166,100 available.`

Minimum projected balance: 174876.82

Evidence/issues:

Candidate rejections:
* full_payment payment_option_48: payment method excluded by user; minimum balance breached on 2026-03-11: 134523.67
* wait payment_option_48: payment method excluded by user
* partial_payment : payment method excluded by user; partial payment not permitted or no strictly partial capacity
* installments payment_option_49: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit

Inferred streams:
* event_1471: payroll credit; monthly=15; observations=5; supported salary rate=206000
* event_1475: credit card repayment; monthly=11; observations=5; latest contractual amount=30200
* event_1542: dining; interval=14; observations=13; mean historical budget, rounded up=5777.68
* event_1474: course tuition; monthly=8; observations=5; latest contractual amount=13660
* event_1503: groceries; interval=7; observations=26; mean historical budget, rounded up=9096.70
* event_1472: apartment rent transfer; monthly=2; observations=5; latest contractual amount=49600
* event_1529: transport; interval=7; observations=26; mean historical budget, rounded up=5278.04
* event_1473: municipal utilities; monthly=6; observations=5; mean historical budget, rounded up=9538.75
* event_1477: food delivery membership; monthly=13; observations=5; latest contractual amount=1675
* event_1476: music subscription; monthly=11; observations=5; latest contractual amount=2055

### request_18

* amount_safe_to_pay:
  * predicted: `460.38`
  * expected: `462`
* decision_explanation:
  * predicted: `Safe today before changes: 460.38 EUR; protected minimum: 1400. Use wait, total 3246.1, completing 2026-09-15. Lowest projected balance: 1860.38 on 2026-07-15. Earlier full payment would not preserve the reserve under this forecast. Limiting expense: event_1621 (85.64 on 2026-07-15). Projected income includes event_1571: 2310 on 2026-07-15.`
  * expected: `Pay EUR 3,246.10 in full on 15 September 2026. Paying earlier would take the balance below the EUR 1,400 minimum.`

Minimum projected balance: 1860.38

Evidence/issues:

Candidate rejections:
* full_payment payment_option_50: minimum balance breached on 2026-07-07: -1385.72
* partial_payment : partial payment not permitted or no strictly partial capacity
* installments payment_option_51: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit

Inferred streams:
* event_1571: payroll credit; monthly=15; observations=5; supported salary rate=2310
* event_1621: dining; interval=14; observations=13; mean historical budget, rounded up=85.64
* event_1595: groceries; interval=10; observations=18; mean historical budget, rounded up=93.43
* event_1575: clinic payment; monthly=11; observations=5; mean historical budget, rounded up=155.42
* event_1577: building maintenance payment; monthly=4; observations=6; latest contractual amount=167
* event_1574: household insurance; monthly=8; observations=5; latest contractual amount=68
* event_1608: transport; interval=14; observations=13; mean historical budget, rounded up=43.86
* event_1573: energy provider bill; monthly=7; observations=5; mean historical budget, rounded up=111.27
* event_1576: family streaming plan; monthly=10; observations=5; latest contractual amount=68

### request_19

* amount_safe_to_pay:
  * predicted: `12526.12`
  * expected: `28820`
* affordability_status:
  * predicted: `not_affordable`
  * expected: `affordable_with_plan`
* recommended_payment_method:
  * predicted: `not_recommended`
  * expected: `partial_payment`
* payment_plan:
  * predicted: `none`
  * expected: `2024-09-04:28820|2024-09-15:10840`
* earliest_date_for_full_payment:
  * predicted: `2024-10-15`
  * expected: `2024-09-15`
* decision_explanation:
  * predicted: `Safe today before changes: 12526.12 INR; protected minimum: 92800. No safe eligible plan completes by the deadline under the resolved forecast. Baseline full payment first becomes safe on 2024-10-15, after the deadline. Limiting expense: event_1659 (12650.00 on 2024-09-15).`
  * expected: `Pay INR 28,820 today and the remaining INR 10,840 on 15 September 2024. This completes the full request and keeps the INR 92,800 minimum protected.`

Minimum projected balance: 105326.12

Evidence/issues:

Candidate rejections:
* full_payment payment_option_52: payment method excluded by user; minimum balance breached on 2024-09-13: 65666.12
* wait payment_option_52: payment outside request/deadline/forecast bounds; payment method excluded by user
* partial_payment : payment outside request/deadline/forecast bounds
* installments payment_option_53: minimum balance breached on 2024-09-15: 84702.92
* installments payment_option_54: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit

Inferred streams:
* event_1654: payroll credit; monthly=15; observations=5; supported salary rate=131000
* event_1657: loan repayment; monthly=13; observations=5; latest contractual amount=11850
* event_1659: childcare contribution; monthly=15; observations=5; mean historical budget, rounded up=12650.00
* event_1686: groceries; interval=7; observations=25; mean historical budget, rounded up=4772.83
* event_1658: clinic payment; monthly=12; observations=5; mean historical budget, rounded up=8808.58
* event_1655: residential rent payment; monthly=4; observations=5; latest contractual amount=36100
* event_1661: clothing and household items; monthly=14; observations=5; mean historical budget, rounded up=5833.87
* event_1699: transport; interval=14; observations=13; mean historical budget, rounded up=3080.13
* event_1656: municipal utilities; monthly=8; observations=5; mean historical budget, rounded up=5955.64
* event_1660: online backup subscription; monthly=14; observations=5; latest contractual amount=395

### request_20

* amount_safe_to_pay:
  * predicted: `8969.66`
  * expected: `5400`
* decision_explanation:
  * predicted: `Safe today before changes: 8969.66 INR; protected minimum: 64500. No safe eligible plan completes by the deadline under the resolved forecast. Limiting expense: event_1739 (2148.28 on 2026-02-13).`
  * expected: `Do not make this payment by 22 February 2026. None of the available options keeps the INR 64,500 minimum protected.`

Minimum projected balance: 73469.66

Evidence/issues:

Candidate rejections:
* full_payment payment_option_55: minimum balance breached on 2026-02-07: -230230.34
* installments payment_option_56: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit

Inferred streams:
* event_1733: payroll credit; monthly=15; observations=5; supported salary rate=108000
* event_1783: dining; interval=21; observations=9; mean historical budget, rounded up=3423.80
* event_1737: school fee payment; monthly=7; observations=5; latest contractual amount=8740
* event_1739: cinema and events; monthly=13; observations=5; mean historical budget, rounded up=2148.28
* event_1761: groceries; interval=10; observations=18; mean historical budget, rounded up=3700.53
* event_1738: family healthcare expense; monthly=9; observations=5; mean historical budget, rounded up=6336.85
* event_1741: home association fee; monthly=2; observations=6; latest contractual amount=7950
* event_1743: household insurance; monthly=6; observations=6; latest contractual amount=3290
* event_1774: transport; interval=14; observations=13; mean historical budget, rounded up=2674.68
* event_1742: municipal utilities; monthly=5; observations=6; mean historical budget, rounded up=7665.16
* event_1740: shared storage plan; monthly=11; observations=5; latest contractual amount=365

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
  * predicted: `Safe today before changes: 1574.40 USD; protected minimum: 1800. Use full_payment, total 1574.4, completing 2026-04-03. Lowest projected balance: 1898.72 on 2026-04-12. Limiting expense: event_1817 (122.42 on 2026-04-12).`
  * expected: `Stop the online backup subscription and reduce the streaming subscription to USD 23.50, then pay USD 1,574.40 today. This leaves at least USD 1,800 available.`

Minimum projected balance: 1898.72

Evidence/issues:

Candidate rejections:
* installments payment_option_58: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit
* installments payment_option_59: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit
* installments payment_option_60: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit

Inferred streams:
* event_1812: payroll credit; monthly=15; observations=5; supported salary rate=2256
* event_1854: dining; interval=21; observations=9; mean historical budget, rounded up=83.44
* event_1836: groceries; interval=10; observations=18; mean historical budget, rounded up=83.63
* event_1818: residential rent payment; monthly=2; observations=6; latest contractual amount=718.8
* event_1817: monthly shopping spend; monthly=12; observations=5; mean historical budget, rounded up=122.42
* event_1845: transport; interval=21; observations=9; mean historical budget, rounded up=41.21
* event_1814: municipal utilities; monthly=6; observations=5; mean historical budget, rounded up=121.18
* event_1815: online backup subscription; monthly=12; observations=5; latest contractual amount=11
* event_1816: streaming subscription; monthly=9; observations=5; latest contractual amount=47

### request_22

* amount_safe_to_pay:
  * predicted: `443.71`
  * expected: `475.46`
* decision_explanation:
  * predicted: `Safe today before changes: 443.71 EUR; protected minimum: 500. Use installments, total 760.77, completing 2025-02-02. Lowest projected balance: 501.46 on 2025-02-15. Limiting expense: event_1893 (20.87 on 2025-02-15). Projected income includes event_1887: 616 on 2024-12-15.`
  * expected: `Use 3 installments of EUR 253.59, starting 8 December 2024. This leaves at least EUR 500 available.`

Minimum projected balance: 501.46

Evidence/issues:

Candidate rejections:
* full_payment payment_option_62: payment method excluded by user; minimum balance breached on 2024-12-05: 212.21
* wait payment_option_62: payment method excluded by user
* partial_payment : payment method excluded by user
* installments payment_option_63: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit

Inferred streams:
* event_1887: payroll credit; monthly=15; observations=5; supported salary rate=616
* event_1958: dining; interval=14; observations=13; mean historical budget, rounded up=16.08
* event_1893: weekend entertainment; monthly=15; observations=5; mean historical budget, rounded up=20.87
* event_1920: groceries; interval=7; observations=26; mean historical budget, rounded up=23.96
* event_1894: apartment rent transfer; monthly=3; observations=6; latest contractual amount=178.2
* event_1945: transport; interval=7; observations=25; mean historical budget, rounded up=13.14
* event_1889: electricity and water bill; monthly=7; observations=5; mean historical budget, rounded up=30.56
* event_1891: food delivery membership; monthly=14; observations=5; latest contractual amount=5
* event_1892: gym membership; monthly=11; observations=5; latest contractual amount=17
* event_1890: music service subscription; monthly=12; observations=5; latest contractual amount=6

### request_23

* amount_safe_to_pay:
  * predicted: `3201.52`
  * expected: `9152`
* decision_explanation:
  * predicted: `Safe today before changes: 3201.52 ZAR; protected minimum: 27000. Use wait, total 38016, completing 2025-07-15. Lowest projected balance: 28330.48 on 2025-08-04. Earlier full payment would not preserve the reserve under this forecast. Limiting expense: event_2002 (15312 on 2025-08-04). Projected income includes event_1994: 45760 on 2025-05-15. Unresolved evidence/forecast assumptions remain; see audit.`
  * expected: `Pay ZAR 38,016 in full on 15 July 2025. Paying earlier would take the balance below the ZAR 27,000 minimum.`

Minimum projected balance: 28330.48

Evidence/issues:
* incomplete_new_fact message_16: new event requires explicit description/category/direction/type/currency/date/status; blocking=False

Candidate rejections:
* full_payment payment_option_64: minimum balance breached on 2025-05-07: -7814.48
* partial_payment : partial payment not permitted or no strictly partial capacity
* installments payment_option_65: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit
* installments payment_option_66: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit

Inferred streams:
* event_1994: payroll credit; monthly=15; observations=5; supported salary rate=45760
* event_1997: education loan instalment; monthly=13; observations=5; latest contractual amount=5852
* event_1999: childcare contribution; monthly=15; observations=5; mean historical budget, rounded up=4270.20
* event_2027: groceries; interval=7; observations=25; mean historical budget, rounded up=1732.48
* event_1998: clinic payment; monthly=12; observations=5; mean historical budget, rounded up=1361.55
* event_2002: shared housing rent; monthly=4; observations=6; latest contractual amount=15312
* event_2001: personal shopping; monthly=14; observations=5; mean historical budget, rounded up=1315.74
* event_2040: transport; interval=14; observations=13; mean historical budget, rounded up=888.44
* event_1996: electricity bill; monthly=8; observations=5; mean historical budget, rounded up=2754.39
* event_2000: cloud storage plan; monthly=14; observations=5; latest contractual amount=295.9

### request_24

* amount_safe_to_pay:
  * predicted: `13539.25`
  * expected: `13420`
* decision_explanation:
  * predicted: `Safe today before changes: 13539.25 INR; protected minimum: 51000. No safe eligible plan completes by the deadline under the resolved forecast. Available methods are excluded by the user. Limiting expense: event_2082 (1930.70 on 2026-01-13).`
  * expected: `Do not proceed with the INR 109,600 request. Although INR 13,420 is available today, the full amount cannot be completed safely within 90 days.`

Minimum projected balance: 64539.25

Evidence/issues:

Candidate rejections:
* full_payment payment_option_67: payment method excluded by user; minimum balance breached on 2026-01-04: -45060.75
* installments payment_option_68: payment outside request/deadline/forecast bounds; payment method excluded by user; installment duration/count exceeds user limit

Inferred streams:
* event_2075: payroll credit; monthly=15; observations=5; supported salary rate=61000
* event_2163: dining; interval=7; observations=26; mean historical budget, rounded up=1854.04
* event_2082: local event tickets; monthly=13; observations=5; mean historical budget, rounded up=1930.70
* event_2101: groceries; interval=10; observations=18; mean historical budget, rounded up=2290.44
* event_2078: insurance policy payment; monthly=6; observations=5; latest contractual amount=2510
* event_2083: landlord standing order; monthly=1; observations=6; latest contractual amount=18600
* event_2081: monthly shopping spend; monthly=11; observations=5; mean historical budget, rounded up=2513.66
* event_2137: transport; interval=5; observations=36; mean historical budget, rounded up=1359.00
* event_2077: household utility payment; monthly=5; observations=5; mean historical budget, rounded up=3303.91
* event_2079: online backup subscription; monthly=11; observations=5; latest contractual amount=355
* event_2080: family streaming plan; monthly=8; observations=5; latest contractual amount=1200

### request_25

* amount_safe_to_pay:
  * predicted: `0`
  * expected: `1425000`
* decision_explanation:
  * predicted: `Safe today before changes: 0 IDR; protected minimum: 23379100. No safe eligible plan completes by the deadline under the resolved forecast. Limiting expense: event_2261 (592511.15 on 2024-03-15).`
  * expected: `Do not make this payment by 17 April 2024. None of the available options keeps the IDR 23,379,100 minimum protected.`

Minimum projected balance: 23162672.23

Evidence/issues:

Candidate rejections:
* full_payment payment_option_69: minimum balance breached on 2024-03-06: -37333327.77
* installments payment_option_70: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit
* installments payment_option_71: payment outside request/deadline/forecast bounds; installment duration/count exceeds user limit

Inferred streams:
* event_2199: international employer payroll; monthly=15; observations=5; supported salary rate=1800
* event_2286: dining; interval=7; observations=25; mean historical budget, rounded up=1034677.39
* event_2206: games and recreation; monthly=14; observations=5; mean historical budget, rounded up=459592.42
* event_2225: groceries; interval=10; observations=18; mean historical budget, rounded up=1199174.80
* event_2202: insurance policy payment; monthly=7; observations=5; latest contractual amount=904400
* event_2207: monthly rent; monthly=2; observations=6; latest contractual amount=6954000
* event_2205: monthly shopping spend; monthly=12; observations=5; mean historical budget, rounded up=1059028.75
* event_2261: transport; interval=5; observations=36; mean historical budget, rounded up=592511.15
* event_2201: household utility payment; monthly=6; observations=5; mean historical budget, rounded up=1323654.72
* event_2203: cloud storage plan; monthly=12; observations=5; latest contractual amount=126350
* event_2204: video streaming plan; monthly=9; observations=5; latest contractual amount=573800


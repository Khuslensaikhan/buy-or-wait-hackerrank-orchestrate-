# Trace: request_259

## Retrieved context

{"events": 58, "messages": 1, "images": 0, "options": 2, "exchange_rates": 25}

## Evidence

* Used: {"source_id": "message_201", "event_id": "event_23855", "action": "confirm"}

## Resolved events

| Event | Date | Amount | Currency | Status | Evidence |
|---|---|---:|---|---|---|
| event_23799 | 2024-04-15 | 792 | EUR | settled |  |
| event_23800 | 2024-04-04 | 240.9 | EUR | settled |  |
| event_23801 | 2024-04-08 | 41.94 | EUR | settled |  |
| event_23802 | 2024-04-13 | 91 | EUR | settled |  |
| event_23803 | 2024-04-13 | 7 | EUR | settled |  |
| event_23804 | 2024-05-15 | 792 | EUR | settled |  |
| event_23805 | 2024-05-04 | 240.9 | EUR | settled |  |
| event_23806 | 2024-05-08 | 39.93 | EUR | settled |  |
| event_23807 | 2024-05-13 | 91 | EUR | settled |  |
| event_23808 | 2024-05-13 | 7 | EUR | settled |  |
| event_23809 | 2024-06-15 | 792 | EUR | settled |  |
| event_23810 | 2024-06-04 | 240.9 | EUR | settled |  |
| event_23811 | 2024-06-08 | 37.95 | EUR | settled |  |
| event_23812 | 2024-06-13 | 91 | EUR | settled |  |
| event_23813 | 2024-06-13 | 7 | EUR | settled |  |
| event_23814 | 2024-07-15 | 792 | EUR | settled |  |
| event_23815 | 2024-07-04 | 240.9 | EUR | settled |  |
| event_23816 | 2024-07-08 | 46.4 | EUR | settled |  |
| event_23817 | 2024-07-13 | 91 | EUR | settled |  |
| event_23818 | 2024-07-13 | 7 | EUR | settled |  |
| event_23819 | 2024-08-15 | 792 | EUR | settled |  |
| event_23820 | 2024-08-04 | 240.9 | EUR | settled |  |
| event_23821 | 2024-08-08 | 39.44 | EUR | settled |  |
| event_23822 | 2024-08-13 | 91 | EUR | settled |  |
| event_23823 | 2024-08-13 | 7 | EUR | settled |  |
| event_23824 | 2024-03-13 | 28.58 | EUR | settled |  |
| event_23825 | 2024-03-27 | 30.04 | EUR | settled |  |
| event_23826 | 2024-04-10 | 29.31 | EUR | settled |  |
| event_23827 | 2024-04-24 | 37.87 | EUR | settled |  |
| event_23828 | 2024-05-08 | 39.16 | EUR | settled |  |
| event_23829 | 2024-05-22 | 42.96 | EUR | settled |  |
| event_23830 | 2024-06-05 | 34.49 | EUR | settled |  |
| event_23831 | 2024-06-19 | 32.1 | EUR | settled |  |
| event_23832 | 2024-07-03 | 33.19 | EUR | settled |  |
| event_23833 | 2024-07-17 | 31.11 | EUR | settled |  |
| event_23834 | 2024-07-31 | 42.39 | EUR | settled |  |
| event_23835 | 2024-08-14 | 41.98 | EUR | settled |  |
| event_23836 | 2024-08-28 | 36.86 | EUR | settled |  |
| event_23837 | 2024-03-14 | 15.09 | EUR | settled |  |
| event_23838 | 2024-04-04 | 22.37 | EUR | settled |  |
| event_23839 | 2024-04-25 | 23.83 | EUR | settled |  |
| event_23840 | 2024-05-16 | 22.96 | EUR | settled |  |
| event_23841 | 2024-06-06 | 22.39 | EUR | settled |  |
| event_23842 | 2024-06-27 | 21.93 | EUR | settled |  |
| event_23843 | 2024-07-18 | 19.6 | EUR | settled |  |
| event_23844 | 2024-08-08 | 18.98 | EUR | settled |  |
| event_23845 | 2024-08-29 | 22.66 | EUR | settled |  |
| event_23846 | 2024-03-10 | 34.6 | EUR | settled |  |
| event_23847 | 2024-03-31 | 36.52 | EUR | settled |  |
| event_23848 | 2024-04-21 | 25.65 | EUR | settled |  |
| event_23849 | 2024-05-12 | 41.15 | EUR | settled |  |
| event_23850 | 2024-06-02 | 43.49 | EUR | settled |  |
| event_23851 | 2024-06-23 | 28.41 | EUR | settled |  |
| event_23852 | 2024-07-14 | 42.65 | EUR | settled |  |
| event_23853 | 2024-08-04 | 40.48 | EUR | settled |  |
| event_23854 | 2024-08-25 | 31.82 | EUR | settled |  |
| event_23855 | 2024-09-02 | 42 | EUR | failed | message_201 |
| event_23856 | 2024-09-08 | 42 | EUR | scheduled |  |

## Projected recurrence

* event_23819: payroll credit; monthly=15; observations=5; supported salary rate=792
* event_23822: personal loan payment; monthly=13; observations=5; latest contractual amount=91
* event_23854: dining; interval=21; observations=9; mean historical budget, rounded up=36.09
* event_23836: groceries; interval=14; observations=13; mean historical budget, rounded up=35.39
* event_23820: monthly rent; monthly=4; observations=5; latest contractual amount=240.9
* event_23845: transport; interval=21; observations=9; mean historical budget, rounded up=21.09
* event_23821: municipal utilities; monthly=8; observations=5; mean historical budget, rounded up=41.14
* event_23823: audio streaming plan; monthly=13; observations=5; latest contractual amount=7

## Capacity

Baseline minimum: 775.78 on 2024-09-15.
{"amount": "175.78", "verified_by_simulation": true, "blocked": false, "algorithm": "maximum cent amount via monotone binary search"}

## Earliest full-payment tests

* {"date": "2024-09-04", "safe": false, "minimum_balance": "-159.22", "breach_date": "2024-09-04"}
* {"date": "2024-09-05", "safe": false, "minimum_balance": "-159.22", "breach_date": "2024-09-05"}
* {"date": "2024-09-06", "safe": false, "minimum_balance": "-159.22", "breach_date": "2024-09-06"}
* {"date": "2024-09-07", "safe": false, "minimum_balance": "-159.22", "breach_date": "2024-09-07"}
* {"date": "2024-09-08", "safe": false, "minimum_balance": "-159.22", "breach_date": "2024-09-08"}
* {"date": "2024-09-09", "safe": false, "minimum_balance": "-159.22", "breach_date": "2024-09-09"}
* {"date": "2024-09-10", "safe": false, "minimum_balance": "-159.22", "breach_date": "2024-09-10"}
* {"date": "2024-09-11", "safe": false, "minimum_balance": "-159.22", "breach_date": "2024-09-11"}
* {"date": "2024-09-12", "safe": false, "minimum_balance": "-159.22", "breach_date": "2024-09-12"}
* {"date": "2024-09-13", "safe": false, "minimum_balance": "-159.22", "breach_date": "2024-09-13"}
* {"date": "2024-09-14", "safe": false, "minimum_balance": "-159.22", "breach_date": "2024-09-14"}
* {"date": "2024-09-15", "safe": false, "minimum_balance": "103.69", "breach_date": "2024-09-25"}
* {"date": "2024-09-16", "safe": false, "minimum_balance": "103.69", "breach_date": "2024-09-25"}
* {"date": "2024-09-17", "safe": false, "minimum_balance": "103.69", "breach_date": "2024-09-25"}
* {"date": "2024-09-18", "safe": false, "minimum_balance": "103.69", "breach_date": "2024-09-25"}
* {"date": "2024-09-19", "safe": false, "minimum_balance": "103.69", "breach_date": "2024-09-25"}
* {"date": "2024-09-20", "safe": false, "minimum_balance": "103.69", "breach_date": "2024-09-25"}
* {"date": "2024-09-21", "safe": false, "minimum_balance": "103.69", "breach_date": "2024-09-25"}
* {"date": "2024-09-22", "safe": false, "minimum_balance": "103.69", "breach_date": "2024-09-25"}
* {"date": "2024-09-23", "safe": false, "minimum_balance": "103.69", "breach_date": "2024-09-25"}
* {"date": "2024-09-24", "safe": false, "minimum_balance": "103.69", "breach_date": "2024-09-25"}
* {"date": "2024-09-25", "safe": false, "minimum_balance": "103.69", "breach_date": "2024-09-25"}
* {"date": "2024-09-26", "safe": false, "minimum_balance": "103.69", "breach_date": "2024-09-26"}
* {"date": "2024-09-27", "safe": false, "minimum_balance": "103.69", "breach_date": "2024-09-27"}
* {"date": "2024-09-28", "safe": false, "minimum_balance": "103.69", "breach_date": "2024-09-28"}
* {"date": "2024-09-29", "safe": false, "minimum_balance": "103.69", "breach_date": "2024-09-29"}
* {"date": "2024-09-30", "safe": false, "minimum_balance": "103.69", "breach_date": "2024-09-30"}
* {"date": "2024-10-01", "safe": false, "minimum_balance": "103.69", "breach_date": "2024-10-01"}
* {"date": "2024-10-02", "safe": false, "minimum_balance": "103.69", "breach_date": "2024-10-02"}
* {"date": "2024-10-03", "safe": false, "minimum_balance": "103.69", "breach_date": "2024-10-03"}
* {"date": "2024-10-04", "safe": false, "minimum_balance": "103.69", "breach_date": "2024-10-04"}
* {"date": "2024-10-05", "safe": false, "minimum_balance": "103.69", "breach_date": "2024-10-05"}
* {"date": "2024-10-06", "safe": false, "minimum_balance": "103.69", "breach_date": "2024-10-06"}
* {"date": "2024-10-07", "safe": false, "minimum_balance": "103.69", "breach_date": "2024-10-07"}
* {"date": "2024-10-08", "safe": false, "minimum_balance": "103.69", "breach_date": "2024-10-08"}
* {"date": "2024-10-09", "safe": false, "minimum_balance": "103.69", "breach_date": "2024-10-09"}
* {"date": "2024-10-10", "safe": false, "minimum_balance": "103.69", "breach_date": "2024-10-10"}
* {"date": "2024-10-11", "safe": false, "minimum_balance": "103.69", "breach_date": "2024-10-11"}
* {"date": "2024-10-12", "safe": false, "minimum_balance": "103.69", "breach_date": "2024-10-12"}
* {"date": "2024-10-13", "safe": false, "minimum_balance": "103.69", "breach_date": "2024-10-13"}
* {"date": "2024-10-14", "safe": false, "minimum_balance": "103.69", "breach_date": "2024-10-14"}
* {"date": "2024-10-15", "safe": false, "minimum_balance": "387.69", "breach_date": "2024-11-04"}
* {"date": "2024-10-16", "safe": false, "minimum_balance": "387.69", "breach_date": "2024-11-04"}
* {"date": "2024-10-17", "safe": false, "minimum_balance": "387.69", "breach_date": "2024-11-04"}
* {"date": "2024-10-18", "safe": false, "minimum_balance": "387.69", "breach_date": "2024-11-04"}
* {"date": "2024-10-19", "safe": false, "minimum_balance": "387.69", "breach_date": "2024-11-04"}
* {"date": "2024-10-20", "safe": false, "minimum_balance": "387.69", "breach_date": "2024-11-04"}
* {"date": "2024-10-21", "safe": false, "minimum_balance": "387.69", "breach_date": "2024-11-04"}
* {"date": "2024-10-22", "safe": false, "minimum_balance": "387.69", "breach_date": "2024-11-04"}
* {"date": "2024-10-23", "safe": false, "minimum_balance": "387.69", "breach_date": "2024-11-04"}
* {"date": "2024-10-24", "safe": false, "minimum_balance": "387.69", "breach_date": "2024-11-04"}
* {"date": "2024-10-25", "safe": false, "minimum_balance": "387.69", "breach_date": "2024-11-04"}
* {"date": "2024-10-26", "safe": false, "minimum_balance": "387.69", "breach_date": "2024-11-04"}
* {"date": "2024-10-27", "safe": false, "minimum_balance": "387.69", "breach_date": "2024-11-04"}
* {"date": "2024-10-28", "safe": false, "minimum_balance": "387.69", "breach_date": "2024-11-04"}
* {"date": "2024-10-29", "safe": false, "minimum_balance": "387.69", "breach_date": "2024-11-04"}
* {"date": "2024-10-30", "safe": false, "minimum_balance": "387.69", "breach_date": "2024-11-04"}
* {"date": "2024-10-31", "safe": false, "minimum_balance": "387.69", "breach_date": "2024-11-04"}
* {"date": "2024-11-01", "safe": false, "minimum_balance": "387.69", "breach_date": "2024-11-04"}
* {"date": "2024-11-02", "safe": false, "minimum_balance": "387.69", "breach_date": "2024-11-04"}
* {"date": "2024-11-03", "safe": false, "minimum_balance": "387.69", "breach_date": "2024-11-04"}
* {"date": "2024-11-04", "safe": false, "minimum_balance": "387.69", "breach_date": "2024-11-04"}
* {"date": "2024-11-05", "safe": false, "minimum_balance": "387.69", "breach_date": "2024-11-05"}
* {"date": "2024-11-06", "safe": false, "minimum_balance": "387.69", "breach_date": "2024-11-06"}
* {"date": "2024-11-07", "safe": false, "minimum_balance": "387.69", "breach_date": "2024-11-07"}
* {"date": "2024-11-08", "safe": false, "minimum_balance": "387.69", "breach_date": "2024-11-08"}
* {"date": "2024-11-09", "safe": false, "minimum_balance": "387.69", "breach_date": "2024-11-09"}
* {"date": "2024-11-10", "safe": false, "minimum_balance": "387.69", "breach_date": "2024-11-10"}
* {"date": "2024-11-11", "safe": false, "minimum_balance": "387.69", "breach_date": "2024-11-11"}
* {"date": "2024-11-12", "safe": false, "minimum_balance": "387.69", "breach_date": "2024-11-12"}
* {"date": "2024-11-13", "safe": false, "minimum_balance": "387.69", "breach_date": "2024-11-13"}
* {"date": "2024-11-14", "safe": false, "minimum_balance": "387.69", "breach_date": "2024-11-14"}
* {"date": "2024-11-15", "safe": true, "minimum_balance": "775.78", "breach_date": null}

## Every candidate

### Candidate 1

```json
{
  "candidate": {
    "method": "full_payment",
    "payments": [
      {
        "day": "2024-09-04",
        "amount": "935"
      }
    ],
    "total_cost": "935",
    "option_id": "payment_option_746",
    "changes": [],
    "change_reasons": []
  },
  "checks": {
    "method_accepted": true,
    "every_payment_possible": false,
    "full_commitment_completed": true,
    "deadline_met": true,
    "minimum_maintained": false,
    "plan_format_valid": true,
    "installment_option_matches": true,
    "spending_changes_valid": true
  },
  "errors": [
    "minimum balance breached on 2024-09-04: -159.22"
  ],
  "valid": false,
  "minimum_balance": "-159.22",
  "ranking_key": null
}
```

### Candidate 2

```json
{
  "candidate": {
    "method": "wait",
    "payments": [
      {
        "day": "2024-11-15",
        "amount": "935"
      }
    ],
    "total_cost": "935",
    "option_id": "payment_option_746",
    "changes": [],
    "change_reasons": []
  },
  "checks": {
    "method_accepted": true,
    "every_payment_possible": true,
    "full_commitment_completed": true,
    "deadline_met": true,
    "minimum_maintained": true,
    "plan_format_valid": true,
    "installment_option_matches": true,
    "spending_changes_valid": true
  },
  "errors": [],
  "valid": true,
  "minimum_balance": "775.78",
  "ranking_key": [
    false,
    0,
    "935",
    "2024-11-15",
    1,
    "payment_option_746"
  ]
}
```

### Candidate 3

```json
{
  "candidate": {
    "method": "partial_payment",
    "payments": [
      {
        "day": "2024-09-04",
        "amount": "175.78"
      },
      {
        "day": "2024-11-15",
        "amount": "759.22"
      }
    ],
    "total_cost": "935",
    "option_id": "",
    "changes": [],
    "change_reasons": []
  },
  "checks": {
    "method_accepted": false,
    "every_payment_possible": true,
    "full_commitment_completed": true,
    "deadline_met": true,
    "minimum_maintained": true,
    "plan_format_valid": true,
    "installment_option_matches": true,
    "spending_changes_valid": true
  },
  "errors": [
    "payment method excluded by user",
    "partial payment not permitted or no strictly partial capacity"
  ],
  "valid": false,
  "minimum_balance": "600.00",
  "ranking_key": null
}
```

### Candidate 4

```json
{
  "candidate": {
    "method": "installments",
    "payments": [
      {
        "day": "2024-09-11",
        "amount": "52.54"
      },
      {
        "day": "2024-10-09",
        "amount": "52.54"
      },
      {
        "day": "2024-11-06",
        "amount": "52.54"
      },
      {
        "day": "2024-12-04",
        "amount": "52.54"
      },
      {
        "day": "2025-01-01",
        "amount": "52.54"
      },
      {
        "day": "2025-01-29",
        "amount": "52.54"
      },
      {
        "day": "2025-02-26",
        "amount": "52.54"
      },
      {
        "day": "2025-03-26",
        "amount": "52.54"
      },
      {
        "day": "2025-04-23",
        "amount": "52.54"
      },
      {
        "day": "2025-05-21",
        "amount": "52.54"
      },
      {
        "day": "2025-06-18",
        "amount": "52.54"
      },
      {
        "day": "2025-07-16",
        "amount": "52.54"
      },
      {
        "day": "2025-08-13",
        "amount": "52.54"
      },
      {
        "day": "2025-09-10",
        "amount": "52.54"
      },
      {
        "day": "2025-10-08",
        "amount": "52.54"
      },
      {
        "day": "2025-11-05",
        "amount": "52.54"
      },
      {
        "day": "2025-12-03",
        "amount": "52.54"
      },
      {
        "day": "2025-12-31",
        "amount": "52.54"
      },
      {
        "day": "2026-01-28",
        "amount": "52.54"
      },
      {
        "day": "2026-02-25",
        "amount": "52.54"
      },
      {
        "day": "2026-03-25",
        "amount": "52.54"
      }
    ],
    "total_cost": "1103.34",
    "option_id": "payment_option_747",
    "changes": [],
    "change_reasons": []
  },
  "checks": {
    "method_accepted": false,
    "every_payment_possible": false,
    "full_commitment_completed": true,
    "deadline_met": false,
    "minimum_maintained": false,
    "plan_format_valid": false,
    "installment_option_matches": false,
    "spending_changes_valid": true
  },
  "errors": [
    "payment outside request/deadline/forecast bounds",
    "payment method excluded by user",
    "installment duration/count exceeds user limit"
  ],
  "valid": false,
  "minimum_balance": null,
  "ranking_key": null
}
```

## Selected recommendation

```json
{
  "request_id": "request_259",
  "amount_safe_to_pay": "175.78",
  "affordability_status": "affordable_later",
  "recommended_payment_method": "wait",
  "payment_plan": "2024-11-15:935",
  "earliest_date_for_full_payment": "2024-11-15",
  "spending_changes_needed": "none",
  "decision_explanation": "Safe today before changes: 175.78 EUR; protected minimum: 600. Use wait, total 935, completing 2024-11-15. Lowest projected balance: 775.78 on 2024-09-15. Earlier full payment would not preserve the reserve under this forecast. Limiting expense: event_23854 (36.09 on 2024-09-15). Projected income includes event_23819: 792 on 2024-09-15."
}
```

## Daily selected forecast

| Date | Opening | Credits | Essential/protected debits | Other debits | Request payments | Closing | Required | Surplus | Lowest |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2024-09-04 | 1269.3 | 0 | 240.9 | 0 | 0 | 1028.4 | 600 | 428.4 | 1028.4 |
| 2024-09-05 | 1028.4 | 0 | 0 | 0 | 0 | 1028.4 | 600 | 428.4 | 1028.4 |
| 2024-09-06 | 1028.4 | 0 | 0 | 0 | 0 | 1028.4 | 600 | 428.4 | 1028.4 |
| 2024-09-07 | 1028.4 | 0 | 0 | 0 | 0 | 1028.4 | 600 | 428.4 | 1028.4 |
| 2024-09-08 | 1028.4 | 0 | 83.14 | 0 | 0 | 945.26 | 600 | 345.26 | 945.26 |
| 2024-09-09 | 945.26 | 0 | 0 | 0 | 0 | 945.26 | 600 | 345.26 | 945.26 |
| 2024-09-10 | 945.26 | 0 | 0 | 0 | 0 | 945.26 | 600 | 345.26 | 945.26 |
| 2024-09-11 | 945.26 | 0 | 35.39 | 0 | 0 | 909.87 | 600 | 309.87 | 909.87 |
| 2024-09-12 | 909.87 | 0 | 0 | 0 | 0 | 909.87 | 600 | 309.87 | 909.87 |
| 2024-09-13 | 909.87 | 0 | 91 | 7 | 0 | 811.87 | 600 | 211.87 | 811.87 |
| 2024-09-14 | 811.87 | 0 | 0 | 0 | 0 | 811.87 | 600 | 211.87 | 811.87 |
| 2024-09-15 | 811.87 | 792 | 0 | 36.09 | 0 | 1567.78 | 600 | 967.78 | 775.78 |
| 2024-09-16 | 1567.78 | 0 | 0 | 0 | 0 | 1567.78 | 600 | 967.78 | 1567.78 |
| 2024-09-17 | 1567.78 | 0 | 0 | 0 | 0 | 1567.78 | 600 | 967.78 | 1567.78 |
| 2024-09-18 | 1567.78 | 0 | 0 | 0 | 0 | 1567.78 | 600 | 967.78 | 1567.78 |
| 2024-09-19 | 1567.78 | 0 | 21.09 | 0 | 0 | 1546.69 | 600 | 946.69 | 1546.69 |
| 2024-09-20 | 1546.69 | 0 | 0 | 0 | 0 | 1546.69 | 600 | 946.69 | 1546.69 |
| 2024-09-21 | 1546.69 | 0 | 0 | 0 | 0 | 1546.69 | 600 | 946.69 | 1546.69 |
| 2024-09-22 | 1546.69 | 0 | 0 | 0 | 0 | 1546.69 | 600 | 946.69 | 1546.69 |
| 2024-09-23 | 1546.69 | 0 | 0 | 0 | 0 | 1546.69 | 600 | 946.69 | 1546.69 |
| 2024-09-24 | 1546.69 | 0 | 0 | 0 | 0 | 1546.69 | 600 | 946.69 | 1546.69 |
| 2024-09-25 | 1546.69 | 0 | 35.39 | 0 | 0 | 1511.30 | 600 | 911.30 | 1511.30 |
| 2024-09-26 | 1511.30 | 0 | 0 | 0 | 0 | 1511.30 | 600 | 911.30 | 1511.30 |
| 2024-09-27 | 1511.30 | 0 | 0 | 0 | 0 | 1511.30 | 600 | 911.30 | 1511.30 |
| 2024-09-28 | 1511.30 | 0 | 0 | 0 | 0 | 1511.30 | 600 | 911.30 | 1511.30 |
| 2024-09-29 | 1511.30 | 0 | 0 | 0 | 0 | 1511.30 | 600 | 911.30 | 1511.30 |
| 2024-09-30 | 1511.30 | 0 | 0 | 0 | 0 | 1511.30 | 600 | 911.30 | 1511.30 |
| 2024-10-01 | 1511.30 | 0 | 0 | 0 | 0 | 1511.30 | 600 | 911.30 | 1511.30 |
| 2024-10-02 | 1511.30 | 0 | 0 | 0 | 0 | 1511.30 | 600 | 911.30 | 1511.30 |
| 2024-10-03 | 1511.30 | 0 | 0 | 0 | 0 | 1511.30 | 600 | 911.30 | 1511.30 |
| 2024-10-04 | 1511.30 | 0 | 240.9 | 0 | 0 | 1270.40 | 600 | 670.40 | 1270.40 |
| 2024-10-05 | 1270.40 | 0 | 0 | 0 | 0 | 1270.40 | 600 | 670.40 | 1270.40 |
| 2024-10-06 | 1270.40 | 0 | 0 | 36.09 | 0 | 1234.31 | 600 | 634.31 | 1234.31 |
| 2024-10-07 | 1234.31 | 0 | 0 | 0 | 0 | 1234.31 | 600 | 634.31 | 1234.31 |
| 2024-10-08 | 1234.31 | 0 | 41.14 | 0 | 0 | 1193.17 | 600 | 593.17 | 1193.17 |
| 2024-10-09 | 1193.17 | 0 | 35.39 | 0 | 0 | 1157.78 | 600 | 557.78 | 1157.78 |
| 2024-10-10 | 1157.78 | 0 | 21.09 | 0 | 0 | 1136.69 | 600 | 536.69 | 1136.69 |
| 2024-10-11 | 1136.69 | 0 | 0 | 0 | 0 | 1136.69 | 600 | 536.69 | 1136.69 |
| 2024-10-12 | 1136.69 | 0 | 0 | 0 | 0 | 1136.69 | 600 | 536.69 | 1136.69 |
| 2024-10-13 | 1136.69 | 0 | 91 | 7 | 0 | 1038.69 | 600 | 438.69 | 1038.69 |
| 2024-10-14 | 1038.69 | 0 | 0 | 0 | 0 | 1038.69 | 600 | 438.69 | 1038.69 |
| 2024-10-15 | 1038.69 | 792 | 0 | 0 | 0 | 1830.69 | 600 | 1230.69 | 1038.69 |
| 2024-10-16 | 1830.69 | 0 | 0 | 0 | 0 | 1830.69 | 600 | 1230.69 | 1830.69 |
| 2024-10-17 | 1830.69 | 0 | 0 | 0 | 0 | 1830.69 | 600 | 1230.69 | 1830.69 |
| 2024-10-18 | 1830.69 | 0 | 0 | 0 | 0 | 1830.69 | 600 | 1230.69 | 1830.69 |
| 2024-10-19 | 1830.69 | 0 | 0 | 0 | 0 | 1830.69 | 600 | 1230.69 | 1830.69 |
| 2024-10-20 | 1830.69 | 0 | 0 | 0 | 0 | 1830.69 | 600 | 1230.69 | 1830.69 |
| 2024-10-21 | 1830.69 | 0 | 0 | 0 | 0 | 1830.69 | 600 | 1230.69 | 1830.69 |
| 2024-10-22 | 1830.69 | 0 | 0 | 0 | 0 | 1830.69 | 600 | 1230.69 | 1830.69 |
| 2024-10-23 | 1830.69 | 0 | 35.39 | 0 | 0 | 1795.30 | 600 | 1195.30 | 1795.30 |
| 2024-10-24 | 1795.30 | 0 | 0 | 0 | 0 | 1795.30 | 600 | 1195.30 | 1795.30 |
| 2024-10-25 | 1795.30 | 0 | 0 | 0 | 0 | 1795.30 | 600 | 1195.30 | 1795.30 |
| 2024-10-26 | 1795.30 | 0 | 0 | 0 | 0 | 1795.30 | 600 | 1195.30 | 1795.30 |
| 2024-10-27 | 1795.30 | 0 | 0 | 36.09 | 0 | 1759.21 | 600 | 1159.21 | 1759.21 |
| 2024-10-28 | 1759.21 | 0 | 0 | 0 | 0 | 1759.21 | 600 | 1159.21 | 1759.21 |
| 2024-10-29 | 1759.21 | 0 | 0 | 0 | 0 | 1759.21 | 600 | 1159.21 | 1759.21 |
| 2024-10-30 | 1759.21 | 0 | 0 | 0 | 0 | 1759.21 | 600 | 1159.21 | 1759.21 |
| 2024-10-31 | 1759.21 | 0 | 21.09 | 0 | 0 | 1738.12 | 600 | 1138.12 | 1738.12 |
| 2024-11-01 | 1738.12 | 0 | 0 | 0 | 0 | 1738.12 | 600 | 1138.12 | 1738.12 |
| 2024-11-02 | 1738.12 | 0 | 0 | 0 | 0 | 1738.12 | 600 | 1138.12 | 1738.12 |
| 2024-11-03 | 1738.12 | 0 | 0 | 0 | 0 | 1738.12 | 600 | 1138.12 | 1738.12 |
| 2024-11-04 | 1738.12 | 0 | 240.9 | 0 | 0 | 1497.22 | 600 | 897.22 | 1497.22 |
| 2024-11-05 | 1497.22 | 0 | 0 | 0 | 0 | 1497.22 | 600 | 897.22 | 1497.22 |
| 2024-11-06 | 1497.22 | 0 | 35.39 | 0 | 0 | 1461.83 | 600 | 861.83 | 1461.83 |
| 2024-11-07 | 1461.83 | 0 | 0 | 0 | 0 | 1461.83 | 600 | 861.83 | 1461.83 |
| 2024-11-08 | 1461.83 | 0 | 41.14 | 0 | 0 | 1420.69 | 600 | 820.69 | 1420.69 |
| 2024-11-09 | 1420.69 | 0 | 0 | 0 | 0 | 1420.69 | 600 | 820.69 | 1420.69 |
| 2024-11-10 | 1420.69 | 0 | 0 | 0 | 0 | 1420.69 | 600 | 820.69 | 1420.69 |
| 2024-11-11 | 1420.69 | 0 | 0 | 0 | 0 | 1420.69 | 600 | 820.69 | 1420.69 |
| 2024-11-12 | 1420.69 | 0 | 0 | 0 | 0 | 1420.69 | 600 | 820.69 | 1420.69 |
| 2024-11-13 | 1420.69 | 0 | 91 | 7 | 0 | 1322.69 | 600 | 722.69 | 1322.69 |
| 2024-11-14 | 1322.69 | 0 | 0 | 0 | 0 | 1322.69 | 600 | 722.69 | 1322.69 |
| 2024-11-15 | 1322.69 | 792 | 0 | 0 | 935 | 1179.69 | 600 | 579.69 | 1179.69 |
| 2024-11-16 | 1179.69 | 0 | 0 | 0 | 0 | 1179.69 | 600 | 579.69 | 1179.69 |
| 2024-11-17 | 1179.69 | 0 | 0 | 36.09 | 0 | 1143.60 | 600 | 543.60 | 1143.60 |
| 2024-11-18 | 1143.60 | 0 | 0 | 0 | 0 | 1143.60 | 600 | 543.60 | 1143.60 |
| 2024-11-19 | 1143.60 | 0 | 0 | 0 | 0 | 1143.60 | 600 | 543.60 | 1143.60 |
| 2024-11-20 | 1143.60 | 0 | 35.39 | 0 | 0 | 1108.21 | 600 | 508.21 | 1108.21 |
| 2024-11-21 | 1108.21 | 0 | 21.09 | 0 | 0 | 1087.12 | 600 | 487.12 | 1087.12 |
| 2024-11-22 | 1087.12 | 0 | 0 | 0 | 0 | 1087.12 | 600 | 487.12 | 1087.12 |
| 2024-11-23 | 1087.12 | 0 | 0 | 0 | 0 | 1087.12 | 600 | 487.12 | 1087.12 |
| 2024-11-24 | 1087.12 | 0 | 0 | 0 | 0 | 1087.12 | 600 | 487.12 | 1087.12 |
| 2024-11-25 | 1087.12 | 0 | 0 | 0 | 0 | 1087.12 | 600 | 487.12 | 1087.12 |
| 2024-11-26 | 1087.12 | 0 | 0 | 0 | 0 | 1087.12 | 600 | 487.12 | 1087.12 |
| 2024-11-27 | 1087.12 | 0 | 0 | 0 | 0 | 1087.12 | 600 | 487.12 | 1087.12 |
| 2024-11-28 | 1087.12 | 0 | 0 | 0 | 0 | 1087.12 | 600 | 487.12 | 1087.12 |
| 2024-11-29 | 1087.12 | 0 | 0 | 0 | 0 | 1087.12 | 600 | 487.12 | 1087.12 |
| 2024-11-30 | 1087.12 | 0 | 0 | 0 | 0 | 1087.12 | 600 | 487.12 | 1087.12 |
| 2024-12-01 | 1087.12 | 0 | 0 | 0 | 0 | 1087.12 | 600 | 487.12 | 1087.12 |
| 2024-12-02 | 1087.12 | 0 | 0 | 0 | 0 | 1087.12 | 600 | 487.12 | 1087.12 |
| 2024-12-03 | 1087.12 | 0 | 0 | 0 | 0 | 1087.12 | 600 | 487.12 | 1087.12 |

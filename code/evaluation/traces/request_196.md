# Trace: request_196

## Retrieved context

{"events": 58, "messages": 0, "images": 0, "options": 4, "exchange_rates": 25}

## Evidence

* Issue: {"code": "stale_recurrence", "source_id": "event_18053", "detail": "previous employer payroll: expected next occurrence 2024-05-15 already overdue", "blocking": false}

## Resolved events

| Event | Date | Amount | Currency | Status | Evidence |
|---|---|---:|---|---|---|
| event_18038 | 2024-01-15 | 814 | EUR | settled |  |
| event_18039 | 2024-01-01 | 248.6 | EUR | settled |  |
| event_18040 | 2024-01-05 | 48.54 | EUR | settled |  |
| event_18041 | 2024-01-10 | 55 | EUR | settled |  |
| event_18042 | 2024-01-10 | 8 | EUR | settled |  |
| event_18043 | 2024-02-15 | 814 | EUR | settled |  |
| event_18044 | 2024-02-01 | 248.6 | EUR | settled |  |
| event_18045 | 2024-02-05 | 57.87 | EUR | settled |  |
| event_18046 | 2024-02-10 | 55 | EUR | settled |  |
| event_18047 | 2024-02-10 | 8 | EUR | settled |  |
| event_18048 | 2024-03-15 | 814 | EUR | settled |  |
| event_18049 | 2024-03-01 | 248.6 | EUR | settled |  |
| event_18050 | 2024-03-05 | 56.49 | EUR | settled |  |
| event_18051 | 2024-03-10 | 55 | EUR | settled |  |
| event_18052 | 2024-03-10 | 8 | EUR | settled |  |
| event_18053 | 2024-04-15 | 814 | EUR | settled |  |
| event_18054 | 2024-04-01 | 248.6 | EUR | settled |  |
| event_18055 | 2024-04-05 | 52.38 | EUR | settled |  |
| event_18056 | 2024-04-10 | 55 | EUR | settled |  |
| event_18057 | 2024-04-10 | 8 | EUR | settled |  |
| event_18058 | 2024-05-15 | 814 | EUR | settled |  |
| event_18059 | 2024-05-01 | 248.6 | EUR | settled |  |
| event_18060 | 2024-05-05 | 54.01 | EUR | settled |  |
| event_18061 | 2024-05-10 | 55 | EUR | settled |  |
| event_18062 | 2024-05-10 | 8 | EUR | settled |  |
| event_18063 | 2024-06-01 | 248.6 | EUR | settled |  |
| event_18064 | 2023-12-08 | 27.19 | EUR | settled |  |
| event_18065 | 2023-12-22 | 39.64 | EUR | settled |  |
| event_18066 | 2024-01-05 | 29.94 | EUR | settled |  |
| event_18067 | 2024-01-19 | 25.93 | EUR | settled |  |
| event_18068 | 2024-02-02 | 27.37 | EUR | settled |  |
| event_18069 | 2024-02-16 | 25.56 | EUR | settled |  |
| event_18070 | 2024-03-01 | 39.09 | EUR | settled |  |
| event_18071 | 2024-03-15 | 33.56 | EUR | settled |  |
| event_18072 | 2024-03-29 | 25.24 | EUR | settled |  |
| event_18073 | 2024-04-12 | 37.58 | EUR | settled |  |
| event_18074 | 2024-04-26 | 37.24 | EUR | settled |  |
| event_18075 | 2024-05-10 | 29 | EUR | settled |  |
| event_18076 | 2024-05-24 | 35.06 | EUR | settled |  |
| event_18077 | 2023-12-09 | 17.93 | EUR | settled |  |
| event_18078 | 2023-12-30 | 18.85 | EUR | settled |  |
| event_18079 | 2024-01-20 | 16.22 | EUR | settled |  |
| event_18080 | 2024-02-10 | 15.05 | EUR | settled |  |
| event_18081 | 2024-03-02 | 20.18 | EUR | settled |  |
| event_18082 | 2024-03-23 | 12.83 | EUR | settled |  |
| event_18083 | 2024-04-13 | 13.71 | EUR | settled |  |
| event_18084 | 2024-05-04 | 15.91 | EUR | settled |  |
| event_18085 | 2024-05-25 | 15.83 | EUR | settled |  |
| event_18086 | 2023-12-10 | 31.73 | EUR | settled |  |
| event_18087 | 2023-12-31 | 28.62 | EUR | settled |  |
| event_18088 | 2024-01-21 | 25.83 | EUR | settled |  |
| event_18089 | 2024-02-11 | 38.07 | EUR | settled |  |
| event_18090 | 2024-03-03 | 33.64 | EUR | settled |  |
| event_18091 | 2024-03-24 | 38.17 | EUR | settled |  |
| event_18092 | 2024-04-14 | 30.63 | EUR | settled |  |
| event_18093 | 2024-05-05 | 41.8 | EUR | settled |  |
| event_18094 | 2024-05-26 | 42.09 | EUR | settled |  |
| event_18095 | 2024-06-15 | 814 | EUR | scheduled |  |

## Projected recurrence

* event_18061: vehicle loan payment; monthly=10; observations=5; latest contractual amount=55
* event_18094: dining; interval=21; observations=9; mean historical budget, rounded up=34.51
* event_18076: groceries; interval=14; observations=13; mean historical budget, rounded up=31.73
* event_18063: residential rent payment; monthly=1; observations=6; latest contractual amount=248.6
* event_18085: transport; interval=21; observations=9; mean historical budget, rounded up=16.28
* event_18060: water and power payment; monthly=5; observations=5; mean historical budget, rounded up=53.86
* event_18062: audio streaming plan; monthly=10; observations=5; latest contractual amount=8

## Capacity

Baseline minimum: 868.00 on 2024-09-01.
{"amount": "368.00", "verified_by_simulation": true, "blocked": false, "algorithm": "maximum cent amount via monotone binary search"}

## Earliest full-payment tests

* {"date": "2024-06-03", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-06-04", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-06-05", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-06-06", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-06-07", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-06-08", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-06-09", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-06-10", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-06-11", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-06-12", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-06-13", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-06-14", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-06-15", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-06-16", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-06-17", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-06-18", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-06-19", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-06-20", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-06-21", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-06-22", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-06-23", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-06-24", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-06-25", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-06-26", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-06-27", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-06-28", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-06-29", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-06-30", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-07-01", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-07-02", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-07-03", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-07-04", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-07-05", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-07-06", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-07-07", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-07-08", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-07-09", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-07-10", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-07-11", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-07-12", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-07-13", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-07-14", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-07-15", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-07-16", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-07-17", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-07-18", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-07-19", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-07-20", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-07-21", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-07-22", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-07-23", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-07-24", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-07-25", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-07-26", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-07-27", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-07-28", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-07-29", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-07-30", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-07-31", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-08-01", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-08-02", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-08-03", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-08-04", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-08-05", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-08-06", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-08-07", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-08-08", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-08-09", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-08-10", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-10"}
* {"date": "2024-08-11", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-11"}
* {"date": "2024-08-12", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-12"}
* {"date": "2024-08-13", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-13"}
* {"date": "2024-08-14", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-14"}
* {"date": "2024-08-15", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-15"}
* {"date": "2024-08-16", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-16"}
* {"date": "2024-08-17", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-17"}
* {"date": "2024-08-18", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-18"}
* {"date": "2024-08-19", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-19"}
* {"date": "2024-08-20", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-20"}
* {"date": "2024-08-21", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-21"}
* {"date": "2024-08-22", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-22"}
* {"date": "2024-08-23", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-23"}
* {"date": "2024-08-24", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-24"}
* {"date": "2024-08-25", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-25"}
* {"date": "2024-08-26", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-26"}
* {"date": "2024-08-27", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-27"}
* {"date": "2024-08-28", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-28"}
* {"date": "2024-08-29", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-29"}
* {"date": "2024-08-30", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-30"}
* {"date": "2024-08-31", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-08-31"}
* {"date": "2024-09-01", "safe": false, "minimum_balance": "105.70", "breach_date": "2024-09-01"}

## Every candidate

### Candidate 1

```json
{
  "candidate": {
    "method": "full_payment",
    "payments": [
      {
        "day": "2024-06-03",
        "amount": "762.3"
      }
    ],
    "total_cost": "762.3",
    "option_id": "payment_option_558",
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
    "minimum balance breached on 2024-08-10: 105.70"
  ],
  "valid": false,
  "minimum_balance": "105.70",
  "ranking_key": null
}
```

### Candidate 2

```json
{
  "candidate": {
    "method": "installments",
    "payments": [
      {
        "day": "2024-06-17",
        "amount": "42.83"
      },
      {
        "day": "2024-07-15",
        "amount": "42.83"
      },
      {
        "day": "2024-08-12",
        "amount": "42.83"
      },
      {
        "day": "2024-09-09",
        "amount": "42.83"
      },
      {
        "day": "2024-10-07",
        "amount": "42.83"
      },
      {
        "day": "2024-11-04",
        "amount": "42.83"
      },
      {
        "day": "2024-12-02",
        "amount": "42.83"
      },
      {
        "day": "2024-12-30",
        "amount": "42.83"
      },
      {
        "day": "2025-01-27",
        "amount": "42.83"
      },
      {
        "day": "2025-02-24",
        "amount": "42.83"
      },
      {
        "day": "2025-03-24",
        "amount": "42.83"
      },
      {
        "day": "2025-04-21",
        "amount": "42.83"
      },
      {
        "day": "2025-05-19",
        "amount": "42.83"
      },
      {
        "day": "2025-06-16",
        "amount": "42.83"
      },
      {
        "day": "2025-07-14",
        "amount": "42.83"
      },
      {
        "day": "2025-08-11",
        "amount": "42.83"
      },
      {
        "day": "2025-09-08",
        "amount": "42.83"
      },
      {
        "day": "2025-10-06",
        "amount": "42.83"
      },
      {
        "day": "2025-11-03",
        "amount": "42.83"
      },
      {
        "day": "2025-12-01",
        "amount": "42.83"
      },
      {
        "day": "2025-12-29",
        "amount": "42.83"
      }
    ],
    "total_cost": "899.43",
    "option_id": "payment_option_559",
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

### Candidate 3

```json
{
  "candidate": {
    "method": "installments",
    "payments": [
      {
        "day": "2024-06-03",
        "amount": "137.21"
      },
      {
        "day": "2024-07-03",
        "amount": "137.21"
      },
      {
        "day": "2024-08-02",
        "amount": "137.21"
      },
      {
        "day": "2024-09-01",
        "amount": "137.21"
      },
      {
        "day": "2024-10-01",
        "amount": "137.21"
      },
      {
        "day": "2024-10-31",
        "amount": "137.21"
      }
    ],
    "total_cost": "823.26",
    "option_id": "payment_option_560",
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

### Candidate 4

```json
{
  "candidate": {
    "method": "installments",
    "payments": [
      {
        "day": "2024-06-06",
        "amount": "38.75"
      },
      {
        "day": "2024-07-07",
        "amount": "38.75"
      },
      {
        "day": "2024-08-07",
        "amount": "38.75"
      },
      {
        "day": "2024-09-07",
        "amount": "38.75"
      },
      {
        "day": "2024-10-08",
        "amount": "38.75"
      },
      {
        "day": "2024-11-08",
        "amount": "38.75"
      },
      {
        "day": "2024-12-09",
        "amount": "38.75"
      },
      {
        "day": "2025-01-09",
        "amount": "38.75"
      },
      {
        "day": "2025-02-09",
        "amount": "38.75"
      },
      {
        "day": "2025-03-12",
        "amount": "38.75"
      },
      {
        "day": "2025-04-12",
        "amount": "38.75"
      },
      {
        "day": "2025-05-13",
        "amount": "38.75"
      },
      {
        "day": "2025-06-13",
        "amount": "38.75"
      },
      {
        "day": "2025-07-14",
        "amount": "38.75"
      },
      {
        "day": "2025-08-14",
        "amount": "38.75"
      },
      {
        "day": "2025-09-14",
        "amount": "38.75"
      },
      {
        "day": "2025-10-15",
        "amount": "38.75"
      },
      {
        "day": "2025-11-15",
        "amount": "38.75"
      },
      {
        "day": "2025-12-16",
        "amount": "38.75"
      },
      {
        "day": "2026-01-16",
        "amount": "38.75"
      },
      {
        "day": "2026-02-16",
        "amount": "38.75"
      },
      {
        "day": "2026-03-19",
        "amount": "38.75"
      },
      {
        "day": "2026-04-19",
        "amount": "38.75"
      },
      {
        "day": "2026-05-20",
        "amount": "38.75"
      }
    ],
    "total_cost": "930",
    "option_id": "payment_option_561",
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
  "request_id": "request_196",
  "amount_safe_to_pay": "368",
  "affordability_status": "not_affordable",
  "recommended_payment_method": "not_recommended",
  "payment_plan": "none",
  "earliest_date_for_full_payment": "",
  "spending_changes_needed": "none",
  "decision_explanation": "Safe today before changes: 368.00 EUR; protected minimum: 500. No safe eligible plan completes by the deadline under the resolved forecast. Limiting expense: event_18063 (248.6 on 2024-09-01). Unresolved evidence/forecast assumptions remain; see audit."
}
```

## Daily selected forecast

| Date | Opening | Credits | Essential/protected debits | Other debits | Request payments | Closing | Required | Surplus | Lowest |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2024-06-03 | 1575.65 | 0 | 0 | 0 | 0 | 1575.65 | 500 | 1075.65 | 1575.65 |
| 2024-06-04 | 1575.65 | 0 | 0 | 0 | 0 | 1575.65 | 500 | 1075.65 | 1575.65 |
| 2024-06-05 | 1575.65 | 0 | 53.86 | 0 | 0 | 1521.79 | 500 | 1021.79 | 1521.79 |
| 2024-06-06 | 1521.79 | 0 | 0 | 0 | 0 | 1521.79 | 500 | 1021.79 | 1521.79 |
| 2024-06-07 | 1521.79 | 0 | 31.73 | 0 | 0 | 1490.06 | 500 | 990.06 | 1490.06 |
| 2024-06-08 | 1490.06 | 0 | 0 | 0 | 0 | 1490.06 | 500 | 990.06 | 1490.06 |
| 2024-06-09 | 1490.06 | 0 | 0 | 0 | 0 | 1490.06 | 500 | 990.06 | 1490.06 |
| 2024-06-10 | 1490.06 | 0 | 55 | 8 | 0 | 1427.06 | 500 | 927.06 | 1427.06 |
| 2024-06-11 | 1427.06 | 0 | 0 | 0 | 0 | 1427.06 | 500 | 927.06 | 1427.06 |
| 2024-06-12 | 1427.06 | 0 | 0 | 0 | 0 | 1427.06 | 500 | 927.06 | 1427.06 |
| 2024-06-13 | 1427.06 | 0 | 0 | 0 | 0 | 1427.06 | 500 | 927.06 | 1427.06 |
| 2024-06-14 | 1427.06 | 0 | 0 | 0 | 0 | 1427.06 | 500 | 927.06 | 1427.06 |
| 2024-06-15 | 1427.06 | 814 | 16.28 | 0 | 0 | 2224.78 | 500 | 1724.78 | 1410.78 |
| 2024-06-16 | 2224.78 | 0 | 0 | 34.51 | 0 | 2190.27 | 500 | 1690.27 | 2190.27 |
| 2024-06-17 | 2190.27 | 0 | 0 | 0 | 0 | 2190.27 | 500 | 1690.27 | 2190.27 |
| 2024-06-18 | 2190.27 | 0 | 0 | 0 | 0 | 2190.27 | 500 | 1690.27 | 2190.27 |
| 2024-06-19 | 2190.27 | 0 | 0 | 0 | 0 | 2190.27 | 500 | 1690.27 | 2190.27 |
| 2024-06-20 | 2190.27 | 0 | 0 | 0 | 0 | 2190.27 | 500 | 1690.27 | 2190.27 |
| 2024-06-21 | 2190.27 | 0 | 31.73 | 0 | 0 | 2158.54 | 500 | 1658.54 | 2158.54 |
| 2024-06-22 | 2158.54 | 0 | 0 | 0 | 0 | 2158.54 | 500 | 1658.54 | 2158.54 |
| 2024-06-23 | 2158.54 | 0 | 0 | 0 | 0 | 2158.54 | 500 | 1658.54 | 2158.54 |
| 2024-06-24 | 2158.54 | 0 | 0 | 0 | 0 | 2158.54 | 500 | 1658.54 | 2158.54 |
| 2024-06-25 | 2158.54 | 0 | 0 | 0 | 0 | 2158.54 | 500 | 1658.54 | 2158.54 |
| 2024-06-26 | 2158.54 | 0 | 0 | 0 | 0 | 2158.54 | 500 | 1658.54 | 2158.54 |
| 2024-06-27 | 2158.54 | 0 | 0 | 0 | 0 | 2158.54 | 500 | 1658.54 | 2158.54 |
| 2024-06-28 | 2158.54 | 0 | 0 | 0 | 0 | 2158.54 | 500 | 1658.54 | 2158.54 |
| 2024-06-29 | 2158.54 | 0 | 0 | 0 | 0 | 2158.54 | 500 | 1658.54 | 2158.54 |
| 2024-06-30 | 2158.54 | 0 | 0 | 0 | 0 | 2158.54 | 500 | 1658.54 | 2158.54 |
| 2024-07-01 | 2158.54 | 0 | 248.6 | 0 | 0 | 1909.94 | 500 | 1409.94 | 1909.94 |
| 2024-07-02 | 1909.94 | 0 | 0 | 0 | 0 | 1909.94 | 500 | 1409.94 | 1909.94 |
| 2024-07-03 | 1909.94 | 0 | 0 | 0 | 0 | 1909.94 | 500 | 1409.94 | 1909.94 |
| 2024-07-04 | 1909.94 | 0 | 0 | 0 | 0 | 1909.94 | 500 | 1409.94 | 1909.94 |
| 2024-07-05 | 1909.94 | 0 | 85.59 | 0 | 0 | 1824.35 | 500 | 1324.35 | 1824.35 |
| 2024-07-06 | 1824.35 | 0 | 16.28 | 0 | 0 | 1808.07 | 500 | 1308.07 | 1808.07 |
| 2024-07-07 | 1808.07 | 0 | 0 | 34.51 | 0 | 1773.56 | 500 | 1273.56 | 1773.56 |
| 2024-07-08 | 1773.56 | 0 | 0 | 0 | 0 | 1773.56 | 500 | 1273.56 | 1773.56 |
| 2024-07-09 | 1773.56 | 0 | 0 | 0 | 0 | 1773.56 | 500 | 1273.56 | 1773.56 |
| 2024-07-10 | 1773.56 | 0 | 55 | 8 | 0 | 1710.56 | 500 | 1210.56 | 1710.56 |
| 2024-07-11 | 1710.56 | 0 | 0 | 0 | 0 | 1710.56 | 500 | 1210.56 | 1710.56 |
| 2024-07-12 | 1710.56 | 0 | 0 | 0 | 0 | 1710.56 | 500 | 1210.56 | 1710.56 |
| 2024-07-13 | 1710.56 | 0 | 0 | 0 | 0 | 1710.56 | 500 | 1210.56 | 1710.56 |
| 2024-07-14 | 1710.56 | 0 | 0 | 0 | 0 | 1710.56 | 500 | 1210.56 | 1710.56 |
| 2024-07-15 | 1710.56 | 0 | 0 | 0 | 0 | 1710.56 | 500 | 1210.56 | 1710.56 |
| 2024-07-16 | 1710.56 | 0 | 0 | 0 | 0 | 1710.56 | 500 | 1210.56 | 1710.56 |
| 2024-07-17 | 1710.56 | 0 | 0 | 0 | 0 | 1710.56 | 500 | 1210.56 | 1710.56 |
| 2024-07-18 | 1710.56 | 0 | 0 | 0 | 0 | 1710.56 | 500 | 1210.56 | 1710.56 |
| 2024-07-19 | 1710.56 | 0 | 31.73 | 0 | 0 | 1678.83 | 500 | 1178.83 | 1678.83 |
| 2024-07-20 | 1678.83 | 0 | 0 | 0 | 0 | 1678.83 | 500 | 1178.83 | 1678.83 |
| 2024-07-21 | 1678.83 | 0 | 0 | 0 | 0 | 1678.83 | 500 | 1178.83 | 1678.83 |
| 2024-07-22 | 1678.83 | 0 | 0 | 0 | 0 | 1678.83 | 500 | 1178.83 | 1678.83 |
| 2024-07-23 | 1678.83 | 0 | 0 | 0 | 0 | 1678.83 | 500 | 1178.83 | 1678.83 |
| 2024-07-24 | 1678.83 | 0 | 0 | 0 | 0 | 1678.83 | 500 | 1178.83 | 1678.83 |
| 2024-07-25 | 1678.83 | 0 | 0 | 0 | 0 | 1678.83 | 500 | 1178.83 | 1678.83 |
| 2024-07-26 | 1678.83 | 0 | 0 | 0 | 0 | 1678.83 | 500 | 1178.83 | 1678.83 |
| 2024-07-27 | 1678.83 | 0 | 16.28 | 0 | 0 | 1662.55 | 500 | 1162.55 | 1662.55 |
| 2024-07-28 | 1662.55 | 0 | 0 | 34.51 | 0 | 1628.04 | 500 | 1128.04 | 1628.04 |
| 2024-07-29 | 1628.04 | 0 | 0 | 0 | 0 | 1628.04 | 500 | 1128.04 | 1628.04 |
| 2024-07-30 | 1628.04 | 0 | 0 | 0 | 0 | 1628.04 | 500 | 1128.04 | 1628.04 |
| 2024-07-31 | 1628.04 | 0 | 0 | 0 | 0 | 1628.04 | 500 | 1128.04 | 1628.04 |
| 2024-08-01 | 1628.04 | 0 | 248.6 | 0 | 0 | 1379.44 | 500 | 879.44 | 1379.44 |
| 2024-08-02 | 1379.44 | 0 | 31.73 | 0 | 0 | 1347.71 | 500 | 847.71 | 1347.71 |
| 2024-08-03 | 1347.71 | 0 | 0 | 0 | 0 | 1347.71 | 500 | 847.71 | 1347.71 |
| 2024-08-04 | 1347.71 | 0 | 0 | 0 | 0 | 1347.71 | 500 | 847.71 | 1347.71 |
| 2024-08-05 | 1347.71 | 0 | 53.86 | 0 | 0 | 1293.85 | 500 | 793.85 | 1293.85 |
| 2024-08-06 | 1293.85 | 0 | 0 | 0 | 0 | 1293.85 | 500 | 793.85 | 1293.85 |
| 2024-08-07 | 1293.85 | 0 | 0 | 0 | 0 | 1293.85 | 500 | 793.85 | 1293.85 |
| 2024-08-08 | 1293.85 | 0 | 0 | 0 | 0 | 1293.85 | 500 | 793.85 | 1293.85 |
| 2024-08-09 | 1293.85 | 0 | 0 | 0 | 0 | 1293.85 | 500 | 793.85 | 1293.85 |
| 2024-08-10 | 1293.85 | 0 | 55 | 8 | 0 | 1230.85 | 500 | 730.85 | 1230.85 |
| 2024-08-11 | 1230.85 | 0 | 0 | 0 | 0 | 1230.85 | 500 | 730.85 | 1230.85 |
| 2024-08-12 | 1230.85 | 0 | 0 | 0 | 0 | 1230.85 | 500 | 730.85 | 1230.85 |
| 2024-08-13 | 1230.85 | 0 | 0 | 0 | 0 | 1230.85 | 500 | 730.85 | 1230.85 |
| 2024-08-14 | 1230.85 | 0 | 0 | 0 | 0 | 1230.85 | 500 | 730.85 | 1230.85 |
| 2024-08-15 | 1230.85 | 0 | 0 | 0 | 0 | 1230.85 | 500 | 730.85 | 1230.85 |
| 2024-08-16 | 1230.85 | 0 | 31.73 | 0 | 0 | 1199.12 | 500 | 699.12 | 1199.12 |
| 2024-08-17 | 1199.12 | 0 | 16.28 | 0 | 0 | 1182.84 | 500 | 682.84 | 1182.84 |
| 2024-08-18 | 1182.84 | 0 | 0 | 34.51 | 0 | 1148.33 | 500 | 648.33 | 1148.33 |
| 2024-08-19 | 1148.33 | 0 | 0 | 0 | 0 | 1148.33 | 500 | 648.33 | 1148.33 |
| 2024-08-20 | 1148.33 | 0 | 0 | 0 | 0 | 1148.33 | 500 | 648.33 | 1148.33 |
| 2024-08-21 | 1148.33 | 0 | 0 | 0 | 0 | 1148.33 | 500 | 648.33 | 1148.33 |
| 2024-08-22 | 1148.33 | 0 | 0 | 0 | 0 | 1148.33 | 500 | 648.33 | 1148.33 |
| 2024-08-23 | 1148.33 | 0 | 0 | 0 | 0 | 1148.33 | 500 | 648.33 | 1148.33 |
| 2024-08-24 | 1148.33 | 0 | 0 | 0 | 0 | 1148.33 | 500 | 648.33 | 1148.33 |
| 2024-08-25 | 1148.33 | 0 | 0 | 0 | 0 | 1148.33 | 500 | 648.33 | 1148.33 |
| 2024-08-26 | 1148.33 | 0 | 0 | 0 | 0 | 1148.33 | 500 | 648.33 | 1148.33 |
| 2024-08-27 | 1148.33 | 0 | 0 | 0 | 0 | 1148.33 | 500 | 648.33 | 1148.33 |
| 2024-08-28 | 1148.33 | 0 | 0 | 0 | 0 | 1148.33 | 500 | 648.33 | 1148.33 |
| 2024-08-29 | 1148.33 | 0 | 0 | 0 | 0 | 1148.33 | 500 | 648.33 | 1148.33 |
| 2024-08-30 | 1148.33 | 0 | 31.73 | 0 | 0 | 1116.60 | 500 | 616.60 | 1116.60 |
| 2024-08-31 | 1116.60 | 0 | 0 | 0 | 0 | 1116.60 | 500 | 616.60 | 1116.60 |
| 2024-09-01 | 1116.60 | 0 | 248.6 | 0 | 0 | 868.00 | 500 | 368.00 | 868.00 |

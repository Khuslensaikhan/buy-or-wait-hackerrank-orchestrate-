# Trace: request_106

## Retrieved context

{"events": 57, "messages": 1, "images": 0, "options": 3, "exchange_rates": 25}

## Evidence

* Issue: {"code": "incomplete_new_fact", "source_id": "message_80", "detail": "new event requires explicit description/category/direction/type/currency/date/status", "blocking": false}
* Issue: {"code": "stale_recurrence", "source_id": "event_9823", "detail": "previous employer payroll: expected next occurrence 2024-11-15 already overdue", "blocking": false}

## Resolved events

| Event | Date | Amount | Currency | Status | Evidence |
|---|---|---:|---|---|---|
| event_9808 | 2024-07-15 | 1815 | EUR | settled |  |
| event_9809 | 2024-07-03 | 524.7 | EUR | settled |  |
| event_9810 | 2024-07-07 | 99.3 | EUR | settled |  |
| event_9811 | 2024-07-12 | 215 | EUR | settled |  |
| event_9812 | 2024-07-12 | 23 | EUR | settled |  |
| event_9813 | 2024-08-15 | 1815 | EUR | settled |  |
| event_9814 | 2024-08-03 | 524.7 | EUR | settled |  |
| event_9815 | 2024-08-07 | 83.44 | EUR | settled |  |
| event_9816 | 2024-08-12 | 215 | EUR | settled |  |
| event_9817 | 2024-08-12 | 23 | EUR | settled |  |
| event_9818 | 2024-09-15 | 1815 | EUR | settled |  |
| event_9819 | 2024-09-03 | 524.7 | EUR | settled |  |
| event_9820 | 2024-09-07 | 100.56 | EUR | settled |  |
| event_9821 | 2024-09-12 | 215 | EUR | settled |  |
| event_9822 | 2024-09-12 | 23 | EUR | settled |  |
| event_9823 | 2024-10-15 | 1815 | EUR | settled |  |
| event_9824 | 2024-10-03 | 524.7 | EUR | settled |  |
| event_9825 | 2024-10-07 | 93.63 | EUR | settled |  |
| event_9826 | 2024-10-12 | 215 | EUR | settled |  |
| event_9827 | 2024-10-12 | 23 | EUR | settled |  |
| event_9828 | 2024-11-15 | 1815 | EUR | settled |  |
| event_9829 | 2024-11-03 | 524.7 | EUR | settled |  |
| event_9830 | 2024-11-07 | 99.16 | EUR | settled |  |
| event_9831 | 2024-11-12 | 215 | EUR | settled |  |
| event_9832 | 2024-11-12 | 23 | EUR | settled |  |
| event_9833 | 2024-06-10 | 66.69 | EUR | settled |  |
| event_9834 | 2024-06-24 | 60.22 | EUR | settled |  |
| event_9835 | 2024-07-08 | 100.42 | EUR | settled |  |
| event_9836 | 2024-07-22 | 64.63 | EUR | settled |  |
| event_9837 | 2024-08-05 | 93.6 | EUR | settled |  |
| event_9838 | 2024-08-19 | 102.91 | EUR | settled |  |
| event_9839 | 2024-09-02 | 79.63 | EUR | settled |  |
| event_9840 | 2024-09-16 | 60.32 | EUR | settled |  |
| event_9841 | 2024-09-30 | 86.98 | EUR | settled |  |
| event_9842 | 2024-10-14 | 70.51 | EUR | settled |  |
| event_9843 | 2024-10-28 | 79.96 | EUR | settled |  |
| event_9844 | 2024-11-11 | 81.7 | EUR | settled |  |
| event_9845 | 2024-11-25 | 99.72 | EUR | settled |  |
| event_9846 | 2024-06-11 | 40.22 | EUR | settled |  |
| event_9847 | 2024-07-02 | 54.33 | EUR | settled |  |
| event_9848 | 2024-07-23 | 43.89 | EUR | settled |  |
| event_9849 | 2024-08-13 | 36.33 | EUR | settled |  |
| event_9850 | 2024-09-03 | 47.38 | EUR | settled |  |
| event_9851 | 2024-09-24 | 35.89 | EUR | settled |  |
| event_9852 | 2024-10-15 | 40.48 | EUR | settled |  |
| event_9853 | 2024-11-05 | 38.2 | EUR | settled |  |
| event_9854 | 2024-11-26 | 40.13 | EUR | settled |  |
| event_9855 | 2024-06-12 | 65.93 | EUR | settled |  |
| event_9856 | 2024-07-03 | 58.05 | EUR | settled |  |
| event_9857 | 2024-07-24 | 48.64 | EUR | settled |  |
| event_9858 | 2024-08-14 | 42.58 | EUR | settled |  |
| event_9859 | 2024-09-04 | 60.51 | EUR | settled |  |
| event_9860 | 2024-09-25 | 66.98 | EUR | settled |  |
| event_9861 | 2024-10-16 | 62.64 | EUR | settled |  |
| event_9862 | 2024-11-06 | 46.88 | EUR | settled |  |
| event_9863 | 2024-11-27 | 72.01 | EUR | settled |  |
| event_9864 | 2024-11-30 | 67 | EUR | cancelled |  |

## Projected recurrence

* event_9831: credit card repayment; monthly=12; observations=5; latest contractual amount=215
* event_9863: dining; interval=21; observations=9; mean historical budget, rounded up=58.25
* event_9845: groceries; interval=14; observations=13; mean historical budget, rounded up=80.57
* event_9829: landlord standing order; monthly=3; observations=5; latest contractual amount=524.7
* event_9854: transport; interval=21; observations=9; mean historical budget, rounded up=41.88
* event_9830: household utility payment; monthly=7; observations=5; mean historical budget, rounded up=95.22
* event_9832: audio streaming plan; monthly=12; observations=5; latest contractual amount=23

## Capacity

Baseline minimum: -1461.27 on 2025-03-03.
{"amount": "0", "verified_by_simulation": false, "blocked": false, "algorithm": "maximum cent amount via monotone binary search"}

## Earliest full-payment tests

* {"reason": "baseline already breaches minimum; no payment date is safe"}

## Every candidate

### Candidate 1

```json
{
  "candidate": {
    "method": "full_payment",
    "payments": [
      {
        "day": "2024-12-03",
        "amount": "2207.7"
      }
    ],
    "total_cost": "2207.7",
    "option_id": "payment_option_298",
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
    "minimum balance breached on 2024-12-03: -3668.97"
  ],
  "valid": false,
  "minimum_balance": "-3668.97",
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
        "day": "2024-12-06",
        "amount": "124.05"
      },
      {
        "day": "2025-01-03",
        "amount": "124.05"
      },
      {
        "day": "2025-01-31",
        "amount": "124.05"
      },
      {
        "day": "2025-02-28",
        "amount": "124.05"
      },
      {
        "day": "2025-03-28",
        "amount": "124.05"
      },
      {
        "day": "2025-04-25",
        "amount": "124.05"
      },
      {
        "day": "2025-05-23",
        "amount": "124.05"
      },
      {
        "day": "2025-06-20",
        "amount": "124.05"
      },
      {
        "day": "2025-07-18",
        "amount": "124.05"
      },
      {
        "day": "2025-08-15",
        "amount": "124.05"
      },
      {
        "day": "2025-09-12",
        "amount": "124.05"
      },
      {
        "day": "2025-10-10",
        "amount": "124.05"
      },
      {
        "day": "2025-11-07",
        "amount": "124.05"
      },
      {
        "day": "2025-12-05",
        "amount": "124.05"
      },
      {
        "day": "2026-01-02",
        "amount": "124.05"
      },
      {
        "day": "2026-01-30",
        "amount": "124.05"
      },
      {
        "day": "2026-02-27",
        "amount": "124.05"
      },
      {
        "day": "2026-03-27",
        "amount": "124.05"
      },
      {
        "day": "2026-04-24",
        "amount": "124.05"
      },
      {
        "day": "2026-05-22",
        "amount": "124.05"
      },
      {
        "day": "2026-06-19",
        "amount": "124.05"
      }
    ],
    "total_cost": "2605.05",
    "option_id": "payment_option_299",
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
        "day": "2024-12-17",
        "amount": "112.22"
      },
      {
        "day": "2025-01-17",
        "amount": "112.22"
      },
      {
        "day": "2025-02-17",
        "amount": "112.22"
      },
      {
        "day": "2025-03-20",
        "amount": "112.22"
      },
      {
        "day": "2025-04-20",
        "amount": "112.22"
      },
      {
        "day": "2025-05-21",
        "amount": "112.22"
      },
      {
        "day": "2025-06-21",
        "amount": "112.22"
      },
      {
        "day": "2025-07-22",
        "amount": "112.22"
      },
      {
        "day": "2025-08-22",
        "amount": "112.22"
      },
      {
        "day": "2025-09-22",
        "amount": "112.22"
      },
      {
        "day": "2025-10-23",
        "amount": "112.22"
      },
      {
        "day": "2025-11-23",
        "amount": "112.22"
      },
      {
        "day": "2025-12-24",
        "amount": "112.22"
      },
      {
        "day": "2026-01-24",
        "amount": "112.22"
      },
      {
        "day": "2026-02-24",
        "amount": "112.22"
      },
      {
        "day": "2026-03-27",
        "amount": "112.22"
      },
      {
        "day": "2026-04-27",
        "amount": "112.22"
      },
      {
        "day": "2026-05-28",
        "amount": "112.22"
      },
      {
        "day": "2026-06-28",
        "amount": "112.22"
      },
      {
        "day": "2026-07-29",
        "amount": "112.22"
      },
      {
        "day": "2026-08-29",
        "amount": "112.22"
      },
      {
        "day": "2026-09-29",
        "amount": "112.22"
      },
      {
        "day": "2026-10-30",
        "amount": "112.22"
      },
      {
        "day": "2026-11-30",
        "amount": "112.22"
      }
    ],
    "total_cost": "2693.28",
    "option_id": "payment_option_300",
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
  "request_id": "request_106",
  "amount_safe_to_pay": "0",
  "affordability_status": "not_affordable",
  "recommended_payment_method": "not_recommended",
  "payment_plan": "none",
  "earliest_date_for_full_payment": "",
  "spending_changes_needed": "none",
  "decision_explanation": "Safe today before changes: 0 EUR; protected minimum: 1200. No safe eligible plan completes by the deadline under the resolved forecast. Limiting expense: event_9829 (524.7 on 2025-03-03). Unresolved evidence/forecast assumptions remain; see audit."
}
```

## Daily selected forecast

| Date | Opening | Credits | Essential/protected debits | Other debits | Request payments | Closing | Required | Surplus | Lowest |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2024-12-03 | 2601.7 | 0 | 524.7 | 0 | 0 | 2077.0 | 1200 | 877.0 | 2077.0 |
| 2024-12-04 | 2077.0 | 0 | 0 | 0 | 0 | 2077.0 | 1200 | 877.0 | 2077.0 |
| 2024-12-05 | 2077.0 | 0 | 0 | 0 | 0 | 2077.0 | 1200 | 877.0 | 2077.0 |
| 2024-12-06 | 2077.0 | 0 | 0 | 0 | 0 | 2077.0 | 1200 | 877.0 | 2077.0 |
| 2024-12-07 | 2077.0 | 0 | 95.22 | 0 | 0 | 1981.78 | 1200 | 781.78 | 1981.78 |
| 2024-12-08 | 1981.78 | 0 | 0 | 0 | 0 | 1981.78 | 1200 | 781.78 | 1981.78 |
| 2024-12-09 | 1981.78 | 0 | 80.57 | 0 | 0 | 1901.21 | 1200 | 701.21 | 1901.21 |
| 2024-12-10 | 1901.21 | 0 | 0 | 0 | 0 | 1901.21 | 1200 | 701.21 | 1901.21 |
| 2024-12-11 | 1901.21 | 0 | 0 | 0 | 0 | 1901.21 | 1200 | 701.21 | 1901.21 |
| 2024-12-12 | 1901.21 | 0 | 215 | 23 | 0 | 1663.21 | 1200 | 463.21 | 1663.21 |
| 2024-12-13 | 1663.21 | 0 | 0 | 0 | 0 | 1663.21 | 1200 | 463.21 | 1663.21 |
| 2024-12-14 | 1663.21 | 0 | 0 | 0 | 0 | 1663.21 | 1200 | 463.21 | 1663.21 |
| 2024-12-15 | 1663.21 | 0 | 0 | 0 | 0 | 1663.21 | 1200 | 463.21 | 1663.21 |
| 2024-12-16 | 1663.21 | 0 | 0 | 0 | 0 | 1663.21 | 1200 | 463.21 | 1663.21 |
| 2024-12-17 | 1663.21 | 0 | 41.88 | 0 | 0 | 1621.33 | 1200 | 421.33 | 1621.33 |
| 2024-12-18 | 1621.33 | 0 | 0 | 58.25 | 0 | 1563.08 | 1200 | 363.08 | 1563.08 |
| 2024-12-19 | 1563.08 | 0 | 0 | 0 | 0 | 1563.08 | 1200 | 363.08 | 1563.08 |
| 2024-12-20 | 1563.08 | 0 | 0 | 0 | 0 | 1563.08 | 1200 | 363.08 | 1563.08 |
| 2024-12-21 | 1563.08 | 0 | 0 | 0 | 0 | 1563.08 | 1200 | 363.08 | 1563.08 |
| 2024-12-22 | 1563.08 | 0 | 0 | 0 | 0 | 1563.08 | 1200 | 363.08 | 1563.08 |
| 2024-12-23 | 1563.08 | 0 | 80.57 | 0 | 0 | 1482.51 | 1200 | 282.51 | 1482.51 |
| 2024-12-24 | 1482.51 | 0 | 0 | 0 | 0 | 1482.51 | 1200 | 282.51 | 1482.51 |
| 2024-12-25 | 1482.51 | 0 | 0 | 0 | 0 | 1482.51 | 1200 | 282.51 | 1482.51 |
| 2024-12-26 | 1482.51 | 0 | 0 | 0 | 0 | 1482.51 | 1200 | 282.51 | 1482.51 |
| 2024-12-27 | 1482.51 | 0 | 0 | 0 | 0 | 1482.51 | 1200 | 282.51 | 1482.51 |
| 2024-12-28 | 1482.51 | 0 | 0 | 0 | 0 | 1482.51 | 1200 | 282.51 | 1482.51 |
| 2024-12-29 | 1482.51 | 0 | 0 | 0 | 0 | 1482.51 | 1200 | 282.51 | 1482.51 |
| 2024-12-30 | 1482.51 | 0 | 0 | 0 | 0 | 1482.51 | 1200 | 282.51 | 1482.51 |
| 2024-12-31 | 1482.51 | 0 | 0 | 0 | 0 | 1482.51 | 1200 | 282.51 | 1482.51 |
| 2025-01-01 | 1482.51 | 0 | 0 | 0 | 0 | 1482.51 | 1200 | 282.51 | 1482.51 |
| 2025-01-02 | 1482.51 | 0 | 0 | 0 | 0 | 1482.51 | 1200 | 282.51 | 1482.51 |
| 2025-01-03 | 1482.51 | 0 | 524.7 | 0 | 0 | 957.81 | 1200 | -242.19 | 957.81 |
| 2025-01-04 | 957.81 | 0 | 0 | 0 | 0 | 957.81 | 1200 | -242.19 | 957.81 |
| 2025-01-05 | 957.81 | 0 | 0 | 0 | 0 | 957.81 | 1200 | -242.19 | 957.81 |
| 2025-01-06 | 957.81 | 0 | 80.57 | 0 | 0 | 877.24 | 1200 | -322.76 | 877.24 |
| 2025-01-07 | 877.24 | 0 | 137.10 | 0 | 0 | 740.14 | 1200 | -459.86 | 740.14 |
| 2025-01-08 | 740.14 | 0 | 0 | 58.25 | 0 | 681.89 | 1200 | -518.11 | 681.89 |
| 2025-01-09 | 681.89 | 0 | 0 | 0 | 0 | 681.89 | 1200 | -518.11 | 681.89 |
| 2025-01-10 | 681.89 | 0 | 0 | 0 | 0 | 681.89 | 1200 | -518.11 | 681.89 |
| 2025-01-11 | 681.89 | 0 | 0 | 0 | 0 | 681.89 | 1200 | -518.11 | 681.89 |
| 2025-01-12 | 681.89 | 0 | 215 | 23 | 0 | 443.89 | 1200 | -756.11 | 443.89 |
| 2025-01-13 | 443.89 | 0 | 0 | 0 | 0 | 443.89 | 1200 | -756.11 | 443.89 |
| 2025-01-14 | 443.89 | 0 | 0 | 0 | 0 | 443.89 | 1200 | -756.11 | 443.89 |
| 2025-01-15 | 443.89 | 0 | 0 | 0 | 0 | 443.89 | 1200 | -756.11 | 443.89 |
| 2025-01-16 | 443.89 | 0 | 0 | 0 | 0 | 443.89 | 1200 | -756.11 | 443.89 |
| 2025-01-17 | 443.89 | 0 | 0 | 0 | 0 | 443.89 | 1200 | -756.11 | 443.89 |
| 2025-01-18 | 443.89 | 0 | 0 | 0 | 0 | 443.89 | 1200 | -756.11 | 443.89 |
| 2025-01-19 | 443.89 | 0 | 0 | 0 | 0 | 443.89 | 1200 | -756.11 | 443.89 |
| 2025-01-20 | 443.89 | 0 | 80.57 | 0 | 0 | 363.32 | 1200 | -836.68 | 363.32 |
| 2025-01-21 | 363.32 | 0 | 0 | 0 | 0 | 363.32 | 1200 | -836.68 | 363.32 |
| 2025-01-22 | 363.32 | 0 | 0 | 0 | 0 | 363.32 | 1200 | -836.68 | 363.32 |
| 2025-01-23 | 363.32 | 0 | 0 | 0 | 0 | 363.32 | 1200 | -836.68 | 363.32 |
| 2025-01-24 | 363.32 | 0 | 0 | 0 | 0 | 363.32 | 1200 | -836.68 | 363.32 |
| 2025-01-25 | 363.32 | 0 | 0 | 0 | 0 | 363.32 | 1200 | -836.68 | 363.32 |
| 2025-01-26 | 363.32 | 0 | 0 | 0 | 0 | 363.32 | 1200 | -836.68 | 363.32 |
| 2025-01-27 | 363.32 | 0 | 0 | 0 | 0 | 363.32 | 1200 | -836.68 | 363.32 |
| 2025-01-28 | 363.32 | 0 | 41.88 | 0 | 0 | 321.44 | 1200 | -878.56 | 321.44 |
| 2025-01-29 | 321.44 | 0 | 0 | 58.25 | 0 | 263.19 | 1200 | -936.81 | 263.19 |
| 2025-01-30 | 263.19 | 0 | 0 | 0 | 0 | 263.19 | 1200 | -936.81 | 263.19 |
| 2025-01-31 | 263.19 | 0 | 0 | 0 | 0 | 263.19 | 1200 | -936.81 | 263.19 |
| 2025-02-01 | 263.19 | 0 | 0 | 0 | 0 | 263.19 | 1200 | -936.81 | 263.19 |
| 2025-02-02 | 263.19 | 0 | 0 | 0 | 0 | 263.19 | 1200 | -936.81 | 263.19 |
| 2025-02-03 | 263.19 | 0 | 605.27 | 0 | 0 | -342.08 | 1200 | -1542.08 | -342.08 |
| 2025-02-04 | -342.08 | 0 | 0 | 0 | 0 | -342.08 | 1200 | -1542.08 | -342.08 |
| 2025-02-05 | -342.08 | 0 | 0 | 0 | 0 | -342.08 | 1200 | -1542.08 | -342.08 |
| 2025-02-06 | -342.08 | 0 | 0 | 0 | 0 | -342.08 | 1200 | -1542.08 | -342.08 |
| 2025-02-07 | -342.08 | 0 | 95.22 | 0 | 0 | -437.30 | 1200 | -1637.30 | -437.30 |
| 2025-02-08 | -437.30 | 0 | 0 | 0 | 0 | -437.30 | 1200 | -1637.30 | -437.30 |
| 2025-02-09 | -437.30 | 0 | 0 | 0 | 0 | -437.30 | 1200 | -1637.30 | -437.30 |
| 2025-02-10 | -437.30 | 0 | 0 | 0 | 0 | -437.30 | 1200 | -1637.30 | -437.30 |
| 2025-02-11 | -437.30 | 0 | 0 | 0 | 0 | -437.30 | 1200 | -1637.30 | -437.30 |
| 2025-02-12 | -437.30 | 0 | 215 | 23 | 0 | -675.30 | 1200 | -1875.30 | -675.30 |
| 2025-02-13 | -675.30 | 0 | 0 | 0 | 0 | -675.30 | 1200 | -1875.30 | -675.30 |
| 2025-02-14 | -675.30 | 0 | 0 | 0 | 0 | -675.30 | 1200 | -1875.30 | -675.30 |
| 2025-02-15 | -675.30 | 0 | 0 | 0 | 0 | -675.30 | 1200 | -1875.30 | -675.30 |
| 2025-02-16 | -675.30 | 0 | 0 | 0 | 0 | -675.30 | 1200 | -1875.30 | -675.30 |
| 2025-02-17 | -675.30 | 0 | 80.57 | 0 | 0 | -755.87 | 1200 | -1955.87 | -755.87 |
| 2025-02-18 | -755.87 | 0 | 41.88 | 0 | 0 | -797.75 | 1200 | -1997.75 | -797.75 |
| 2025-02-19 | -797.75 | 0 | 0 | 58.25 | 0 | -856.00 | 1200 | -2056.00 | -856.00 |
| 2025-02-20 | -856.00 | 0 | 0 | 0 | 0 | -856.00 | 1200 | -2056.00 | -856.00 |
| 2025-02-21 | -856.00 | 0 | 0 | 0 | 0 | -856.00 | 1200 | -2056.00 | -856.00 |
| 2025-02-22 | -856.00 | 0 | 0 | 0 | 0 | -856.00 | 1200 | -2056.00 | -856.00 |
| 2025-02-23 | -856.00 | 0 | 0 | 0 | 0 | -856.00 | 1200 | -2056.00 | -856.00 |
| 2025-02-24 | -856.00 | 0 | 0 | 0 | 0 | -856.00 | 1200 | -2056.00 | -856.00 |
| 2025-02-25 | -856.00 | 0 | 0 | 0 | 0 | -856.00 | 1200 | -2056.00 | -856.00 |
| 2025-02-26 | -856.00 | 0 | 0 | 0 | 0 | -856.00 | 1200 | -2056.00 | -856.00 |
| 2025-02-27 | -856.00 | 0 | 0 | 0 | 0 | -856.00 | 1200 | -2056.00 | -856.00 |
| 2025-02-28 | -856.00 | 0 | 0 | 0 | 0 | -856.00 | 1200 | -2056.00 | -856.00 |
| 2025-03-01 | -856.00 | 0 | 0 | 0 | 0 | -856.00 | 1200 | -2056.00 | -856.00 |
| 2025-03-02 | -856.00 | 0 | 0 | 0 | 0 | -856.00 | 1200 | -2056.00 | -856.00 |
| 2025-03-03 | -856.00 | 0 | 605.27 | 0 | 0 | -1461.27 | 1200 | -2661.27 | -1461.27 |

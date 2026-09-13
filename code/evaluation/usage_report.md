# Run usage

```json
{
  "provider": "cache",
  "model": "gpt-5.6-terra",
  "prompt_version": "evidence-v2",
  "live_calls": 0,
  "cached_resolutions": 203,
  "input_tokens": 0,
  "output_tokens": 0,
  "unmetered_calls": 0,
  "input_rate_per_million": null,
  "output_rate_per_million": null,
  "estimated_cost": "0",
  "cost_status": "estimated",
  "requests": 250,
  "run_kind": "full-dataset prediction",
  "total_tokens": 0,
  "average_tokens_per_request": "0",
  "estimated_cost_per_request": "0"
}
```

These token and cost totals cover new model calls during the named run. Cached resolutions use previously extracted facts from the listed model; zero new tokens does not mean their original extraction was free. Historical cache usage is cumulative and is not summed as per-source billing. Separate extraction attempts and failures are recorded in evidence_extraction.json.

# Interrupted extraction diagnosis

The reported traceback stopped while waiting for OpenAI response headers after Ctrl-C.
The previous command printed only once all request contexts had finished, so an in-flight
call was invisible. The client had no command-specific timeout. The traceback alone
cannot establish why the response was delayed.

Read-only inspection found **23 complete, schema-valid JSON cache entries**, with no
partial JSON or temporary files. Every existing cache file was verified unchanged by
SHA-256 after implementation and offline tests. Completed responses were already saved
per response before this change; the interrupted in-flight response has no recoverable
local result or usage record. Its source ID cannot be established from the reported
traceback alone.

The command now deduplicates evidence globally, prints flushed progress and per-source
failures, supports filtering and limits, and uses configurable SDK timeout/retries
(default 60 seconds/1 retry) and reasoning effort none. Each response commits through
a unique temporary file, fsync and atomic rename. Ctrl-C preserves completed entries,
prints a summary and writes JSON/Markdown extraction audits. Errors never become zero
amounts. SDK retries can make one logical source call exceed 60 seconds.

Offline dry run: **215 unique messages, 16 unique images, 23 cached, 208 requiring
calls**. Estimated logical calls: 208; maximum HTTP attempts at one retry: 416.
The accompanying JSON lists evidence IDs in deterministic processing order.

Validation: **74/74 offline tests passed**. No OpenAI calls were made, dataset files
were unchanged, and root output.csv was not generated.

```sh
source .venv/bin/activate
python3.12 -m unittest discover -s code/tests -v
python3.12 code/main.py extract-evidence --all --dry-run
```

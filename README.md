# Calendar agent — Exercise 1

Python 3.11+ calendar assistant using an OpenAI-compatible Chat Completions API.

## Setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and enter your API key. The example selects Groq and
`openai/gpt-oss-20b`. All four settings (`OPENAI_BASE_URL`, `MODEL`,
`OPENAI_API_KEY`, `DATA_BASE_URL`) are required. Existing environment variables
have precedence over `.env`; endpoint, model and data URL are not hard-coded
in the agent. `.env`, `.venv/` and `logs/` are excluded from Git.

## Run

From the repository root, with the virtual environment activated:

```bash
python -m agent "Was steht am 29.10.2026 im Kalender?"
python -m agent "Welche Termine habe ich am 08.11.2026?"
python -m agent "What is scheduled on 2026-12-01?"
```

Successful runs print the answer to stdout and exit with code 0. Errors are
reported on stderr with exit code 1. Mock calendar data covers 26 October to
8 November 2026. An HTTP 404 is a normal `no_data` tool result, distinct from
an existing day whose `events` list is empty.

## How it works

1. Read configuration and create a unique run log.
2. Send the user's question and the `get_calendar_day` JSON schema to the model.
   `tool_choice="required"` requires a tool call; the model chooses its date argument.
3. Validate the date and retrieve `{DATA_BASE_URL}/calendar/{date}.json` over HTTP.
4. Append the assistant's tool call and the matching `tool_call_id` result.
5. Ask the model to produce a concise answer grounded in that result.

The program uses the `openai` library, not the provider-specific Groq library.
It performs one model → tool → model round trip and does not copy calendar data
into source files. Tool results are recorded in ignored local run logs.

## Logs

Each invocation writes `logs/<run_id>.jsonl`. Each line contains `ts` (UTC ISO
8601), `run_id`, `event`, `tool`, `args`, `ok`, `model`, and `duration_ms`.
Event types are `user_task`, `tool_call`, `tool_result`, `final`, and `error`.
Additional fields record the task, tool result, final answer or sanitized error.
Non-tool events use `null` for `tool` and `args`. Durations are milliseconds;
`tool_call` measures the first model request, `tool_result` the HTTP tool step,
and `final` the second model request. No API key is logged.

## Offline tests

```bash
python -m unittest discover -s tests -v
```

Tests mock HTTP and the model; they do not consume API quota. Live model behavior
must additionally be checked with the run commands above.

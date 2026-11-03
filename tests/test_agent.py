import io
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch
from urllib.error import HTTPError

from agent import __main__ as agent


class CalendarTests(unittest.TestCase):
    def test_calendar_and_empty_day(self):
        for events in [[], [{"title": "Lecture", "start": "09:00"}]]:
            response = io.BytesIO(json.dumps({"events": events}).encode())
            with patch.object(agent, "urlopen", return_value=response) as fetch:
                result = agent.get_calendar_day("https://example.test/v1/", "2026-10-29")
            self.assertEqual(result["data"]["events"], events)
            fetch.assert_called_once_with(
                "https://example.test/v1/calendar/2026-10-29.json", timeout=20)

    def test_404_is_missing_data(self):
        error = HTTPError("https://example.test", 404, "Not found", {}, None)
        with patch.object(agent, "urlopen", side_effect=error):
            result = agent.get_calendar_day("https://example.test", "2026-12-01")
        self.assertEqual(result["status"], "no_data")

    def test_invalid_date_cannot_make_http_request(self):
        with patch.object(agent, "urlopen") as fetch:
            for value in ["../../secret", "2026-02-30", "20261029"]:
                with self.assertRaises(ValueError):
                    agent.get_calendar_day("https://example.test", value)
            fetch.assert_not_called()

    def test_model_tool_model_and_log(self):
        call = SimpleNamespace(id="call_1", function=SimpleNamespace(
            name="get_calendar_day", arguments='{"date":"2026-10-29"}'))
        message = Mock(tool_calls=[call])
        message.model_dump.return_value = {
            "role": "assistant", "tool_calls": [{"id": "call_1", "type": "function",
            "function": {"name": "get_calendar_day", "arguments": call.function.arguments}}]}
        client = Mock()
        client.chat.completions.create.side_effect = [
            SimpleNamespace(choices=[SimpleNamespace(message=message)]),
            SimpleNamespace(choices=[SimpleNamespace(finish_reason="stop",
                message=SimpleNamespace(content="No appointments."))]),
        ]
        with tempfile.TemporaryDirectory() as directory, patch.object(agent, "ROOT", Path(directory)):
            log = agent.RunLog("test-model")
            log.write("user_task", task="Calendar?")
            with patch.object(agent, "get_calendar_day", return_value={
                    "status": "ok", "data": {"events": []}}) as tool:
                answer = agent.answer(client, "test-model", "https://example.test", "Calendar?", log)
            tool.assert_called_once_with("https://example.test", "2026-10-29")
            self.assertEqual(answer, "No appointments.")
            self.assertEqual(client.chat.completions.create.call_count, 2)
            sent = client.chat.completions.create.call_args.kwargs["messages"]
            self.assertEqual(sent[-1]["tool_call_id"], "call_1")
            self.assertEqual(json.loads(sent[-1]["content"])["data"]["events"], [])
            rows = [json.loads(line) for line in log.path.read_text().splitlines()]
            self.assertEqual([r["event"] for r in rows],
                             ["user_task", "tool_call", "tool_result", "final"])
            fields = {"ts", "run_id", "event", "tool", "args", "ok", "model", "duration_ms"}
            for row in rows:
                self.assertTrue(fields <= row.keys())
            self.assertEqual(len({r["run_id"] for r in rows}), 1)
            self.assertNotEqual(agent.RunLog("test-model").path, log.path)


if __name__ == "__main__":
    unittest.main()

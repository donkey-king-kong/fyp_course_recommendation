import json
import tempfile
import unittest
from pathlib import Path

from adapter import (
    Store,
    complete_agent,
    prune_events,
    run_demo,
    sanitize_label,
    start_agent,
    tool_event,
    update_status,
)


class AdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "runtime"
        self.store = Store(self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def events(self) -> list[dict]:
        return [
            json.loads(line)
            for line in self.store.events.read_text(encoding="utf-8").splitlines()
            if line
        ]

    def test_lifecycle_writes_agent_flow_events_and_heartbeat(self) -> None:
        self.store.initialize("session-1", "Coordinate checks")
        start_agent(self.store, "checker", "orchestrator", "Check metadata")
        update_status(self.store, "checker", "working", "Reviewing event types")
        tool_event(self.store, "checker", "read", end=False)
        tool_event(self.store, "checker", "read", end=True)
        complete_agent(
            self.store,
            "checker",
            parent="orchestrator",
            summary="Checks complete",
            failed=False,
        )

        types = [event["type"] for event in self.events()]
        self.assertEqual(
            types,
            [
                "agent_spawn",
                "subagent_dispatch",
                "agent_spawn",
                "message",
                "tool_call_start",
                "tool_call_end",
                "subagent_return",
                "agent_complete",
            ],
        )
        child = json.loads(
            (self.store.heartbeats / "checker.json").read_text(encoding="utf-8")
        )
        self.assertEqual(child["parent_id"], "orchestrator")
        self.assertEqual(child["status"], "completed")

    def test_sensitive_labels_are_redacted(self) -> None:
        raw = (
            "Read /Users/example/private.txt for person@example.com "
            "token=abc123 password=hunter2 Bearer xyz123"
        )
        cleaned = sanitize_label(raw)
        self.assertNotIn("/Users/example", cleaned)
        self.assertNotIn("person@example.com", cleaned)
        self.assertNotIn("abc123", cleaned)
        self.assertNotIn("hunter2", cleaned)
        self.assertNotIn("xyz123", cleaned)

    def test_demo_contains_parent_two_children_waiting_and_failure(self) -> None:
        run_demo(self.store)
        events = self.events()
        spawns = [event for event in events if event["type"] == "agent_spawn"]
        self.assertEqual(
            {event["payload"]["name"] for event in spawns},
            {"orchestrator", "researcher", "verifier"},
        )
        self.assertTrue(any(event["type"] == "permission_requested" for event in events))
        self.assertTrue(any(event["type"] == "error" for event in events))
        verifier = json.loads(
            (self.store.heartbeats / "verifier.json").read_text(encoding="utf-8")
        )
        self.assertEqual(verifier["status"], "failed")

    def test_prune_keeps_newest_events(self) -> None:
        run_demo(self.store)
        before = self.events()
        removed = prune_events(self.store, 3)
        after = self.events()
        self.assertEqual(removed, len(before) - 3)
        self.assertEqual(after, before[-3:])


if __name__ == "__main__":
    unittest.main()

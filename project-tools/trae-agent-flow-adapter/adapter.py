#!/usr/bin/env python3
"""Publish metadata-only cooperative agent events for Agent Flow."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import tempfile
import time
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
DEFAULT_ROOT = WORKSPACE / "project-records" / "agent-observability" / "runtime"
STATES = {"starting", "working", "waiting", "blocked", "completed", "failed"}
TOOL_CATEGORIES = {
    "browser": "Browser",
    "edit": "Edit",
    "read": "Read",
    "search": "Search",
    "shell": "Shell",
    "test": "Test",
}


def sanitize_label(value: str, *, limit: int = 160) -> str:
    """Redact common sensitive values from a short display label."""
    text = " ".join(value.replace("\x00", "").split())
    text = re.sub(r"(?i)\bBearer\s+\S+", "<redacted-token>", text)
    text = re.sub(
        r"(?i)\b(?:api[_-]?key|token|password|secret)\s*[:=]\s*\S+",
        "<redacted-secret>",
        text,
    )
    text = re.sub(r"\bsk-[A-Za-z0-9_-]{8,}\b", "<redacted-token>", text)
    text = re.sub(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "<redacted-email>",
        text,
    )
    text = re.sub(r"(?<!\w)(?:/Users|/home|/tmp)/\S+", "<redacted-path>", text)
    return text[:limit] or "unspecified"


def safe_id(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "-", value.strip()).strip("-")
    if not slug:
        raise ValueError("agent and session identifiers must contain a safe character")
    return slug[:80]


class Store:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.heartbeats = self.root / "heartbeats"
        self.events = self.root / "agent-flow-events.jsonl"
        self.session = self.root / "session.json"

    def ensure(self) -> None:
        self.heartbeats.mkdir(parents=True, exist_ok=True)
        self.events.touch(exist_ok=True)

    def elapsed(self) -> float:
        if not self.session.exists():
            raise RuntimeError("session is not initialized; run the init command first")
        data = json.loads(self.session.read_text(encoding="utf-8"))
        return round(max(0.0, time.time() - float(data["started_at"])), 3)

    def write_json_atomic(self, path: Path, data: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(data, handle, indent=2, sort_keys=True)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_name, path)
        finally:
            if os.path.exists(temp_name):
                os.unlink(temp_name)

    def append_event(
        self,
        event_type: str,
        payload: dict[str, Any],
        *,
        event_time: float | None = None,
    ) -> None:
        self.ensure()
        event = {
            "time": self.elapsed() if event_time is None else event_time,
            "type": event_type,
            "payload": payload,
        }
        if self.session.exists():
            session = json.loads(self.session.read_text(encoding="utf-8"))
            event["sessionId"] = session["session_id"]
        encoded = (json.dumps(event, separators=(",", ":")) + "\n").encode("utf-8")
        fd = os.open(self.events, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
        try:
            os.write(fd, encoded)
            os.fsync(fd)
        finally:
            os.close(fd)

    def heartbeat_path(self, agent: str) -> Path:
        return self.heartbeats / f"{safe_id(agent)}.json"

    def update_heartbeat(
        self,
        agent: str,
        *,
        parent: str | None = None,
        task: str | None = None,
        state: str,
        activity: str,
        outputs: list[str] | None = None,
        blocker: str | None = None,
    ) -> None:
        if state not in STATES:
            raise ValueError(f"unsupported state: {state}")
        path = self.heartbeat_path(agent)
        current: dict[str, Any] = {}
        if path.exists():
            current = json.loads(path.read_text(encoding="utf-8"))
        data = {
            **current,
            "agent_id": safe_id(agent),
            "parent_id": safe_id(parent) if parent else current.get("parent_id"),
            "task": sanitize_label(task) if task else current.get("task", "unspecified"),
            "status": state,
            "activity": sanitize_label(activity),
            "outputs": [sanitize_label(item) for item in (outputs or current.get("outputs", []))],
            "blocker": sanitize_label(blocker) if blocker else None,
            "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        self.write_json_atomic(path, data)

    def initialize(self, session_id: str, task: str, *, replace: bool = False) -> None:
        if replace and self.root.exists():
            shutil.rmtree(self.root)
        self.ensure()
        session = {
            "session_id": safe_id(session_id),
            "started_at": time.time(),
            "task": sanitize_label(task),
        }
        self.write_json_atomic(self.session, session)
        self.update_heartbeat(
            "orchestrator",
            task=task,
            state="starting",
            activity="Starting cooperative session",
        )
        self.append_event(
            "agent_spawn",
            {"name": "orchestrator", "isMain": True, "task": sanitize_label(task)},
            event_time=0.0,
        )


def start_agent(store: Store, agent: str, parent: str, task: str) -> None:
    agent_id, parent_id = safe_id(agent), safe_id(parent)
    clean_task = sanitize_label(task)
    store.update_heartbeat(
        agent_id,
        parent=parent_id,
        task=clean_task,
        state="starting",
        activity="Starting assigned task",
    )
    store.append_event(
        "subagent_dispatch",
        {"parent": parent_id, "child": agent_id, "task": clean_task},
    )
    store.append_event(
        "agent_spawn",
        {"name": agent_id, "parent": parent_id, "task": clean_task},
    )


def update_status(
    store: Store,
    agent: str,
    state: str,
    activity: str,
    blocker: str | None = None,
) -> None:
    agent_id = safe_id(agent)
    store.update_heartbeat(
        agent_id,
        state=state,
        activity=activity,
        blocker=blocker,
    )
    clean_activity = sanitize_label(activity)
    if state == "waiting":
        store.append_event(
            "permission_requested",
            {
                "agent": agent_id,
                "title": "Waiting",
                "message": clean_activity,
            },
        )
    elif state in {"blocked", "failed"}:
        store.append_event(
            "error",
            {
                "agent": agent_id,
                "message": sanitize_label(blocker or clean_activity),
                "status": state,
            },
        )
    elif state in {"starting", "working"}:
        store.append_event(
            "message",
            {"agent": agent_id, "content": clean_activity},
        )


def tool_event(
    store: Store,
    agent: str,
    category: str,
    *,
    end: bool,
    outcome: str = "succeeded",
) -> None:
    agent_id = safe_id(agent)
    tool = TOOL_CATEGORIES.get(category.lower(), "Other")
    if end:
        store.append_event(
            "tool_call_end",
            {
                "agent": agent_id,
                "tool": tool,
                "result": f"{tool} activity {sanitize_label(outcome, limit=40)}",
                "tokenCost": 0,
            },
        )
    else:
        store.append_event(
            "tool_call_start",
            {
                "agent": agent_id,
                "tool": tool,
                "args": "metadata withheld",
                "preview": f"{tool} activity",
            },
        )


def complete_agent(
    store: Store,
    agent: str,
    *,
    parent: str | None,
    summary: str,
    failed: bool,
) -> None:
    agent_id = safe_id(agent)
    clean_summary = sanitize_label(summary)
    final_state = "failed" if failed else "completed"
    store.update_heartbeat(
        agent_id,
        state=final_state,
        activity=clean_summary,
        blocker=clean_summary if failed else None,
    )
    if parent:
        store.append_event(
            "subagent_return",
            {
                "child": agent_id,
                "parent": safe_id(parent),
                "summary": clean_summary,
                "status": final_state,
            },
        )
    if failed:
        store.append_event(
            "error",
            {"agent": agent_id, "message": clean_summary, "status": "failed"},
        )
    store.append_event("agent_complete", {"name": agent_id, "status": final_state})


def prune_events(store: Store, max_events: int) -> int:
    if max_events < 1:
        raise ValueError("max-events must be at least 1")
    if not store.events.exists():
        return 0
    lines = [line for line in store.events.read_text(encoding="utf-8").splitlines() if line]
    kept = lines[-max_events:]
    store.events.write_text("\n".join(kept) + ("\n" if kept else ""), encoding="utf-8")
    return len(lines) - len(kept)


def run_demo(store: Store) -> None:
    store.initialize(
        "trae-local-demo",
        "Demonstrate cooperative TRAE subagent visualization",
        replace=True,
    )
    update_status(store, "orchestrator", "working", "Coordinating two local demo agents")
    start_agent(store, "researcher", "orchestrator", "Inspect public event schema")
    update_status(store, "researcher", "working", "Reviewing metadata contract")
    tool_event(store, "researcher", "Read", end=False)
    tool_event(store, "researcher", "Read", end=True)
    complete_agent(
        store,
        "researcher",
        parent="orchestrator",
        summary="Schema review completed",
        failed=False,
    )
    start_agent(store, "verifier", "orchestrator", "Check privacy boundaries")
    update_status(store, "verifier", "waiting", "Waiting for a verification input")
    update_status(
        store,
        "verifier",
        "blocked",
        "Verification cannot continue",
        blocker="Required test fixture unavailable",
    )
    complete_agent(
        store,
        "verifier",
        parent="orchestrator",
        summary="Verification fixture unavailable",
        failed=True,
    )
    complete_agent(
        store,
        "orchestrator",
        parent=None,
        summary="Local visualization demo completed",
        failed=False,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="initialize a cooperative session")
    init.add_argument("--session-id", required=True)
    init.add_argument("--task", required=True)
    init.add_argument("--replace", action="store_true")

    start = sub.add_parser("start", help="register a child agent")
    start.add_argument("--agent", required=True)
    start.add_argument("--parent", default="orchestrator")
    start.add_argument("--task", required=True)

    status = sub.add_parser("status", help="update an agent heartbeat")
    status.add_argument("--agent", required=True)
    status.add_argument("--state", choices=sorted(STATES), required=True)
    status.add_argument("--activity", required=True)
    status.add_argument("--blocker")

    tool_start = sub.add_parser("tool-start", help="record a sanitized tool start")
    tool_start.add_argument("--agent", required=True)
    tool_start.add_argument("--category", required=True)

    tool_end = sub.add_parser("tool-end", help="record a sanitized tool result")
    tool_end.add_argument("--agent", required=True)
    tool_end.add_argument("--category", required=True)
    tool_end.add_argument("--outcome", choices=("succeeded", "failed"), default="succeeded")

    complete = sub.add_parser("complete", help="finish an agent")
    complete.add_argument("--agent", required=True)
    complete.add_argument("--parent")
    complete.add_argument("--summary", required=True)
    complete.add_argument("--failed", action="store_true")

    sub.add_parser("demo", help="write a parent and two-subagent demonstration")

    prune = sub.add_parser("prune", help="retain only the newest events")
    prune.add_argument("--max-events", type=int, default=1000)

    clear = sub.add_parser("clear", help="delete this adapter's runtime telemetry")
    clear.add_argument("--yes", action="store_true", required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    store = Store(args.root)
    try:
        if args.command == "init":
            store.initialize(args.session_id, args.task, replace=args.replace)
        elif args.command == "start":
            start_agent(store, args.agent, args.parent, args.task)
        elif args.command == "status":
            update_status(store, args.agent, args.state, args.activity, args.blocker)
        elif args.command == "tool-start":
            tool_event(store, args.agent, args.category, end=False)
        elif args.command == "tool-end":
            tool_event(
                store,
                args.agent,
                args.category,
                end=True,
                outcome=args.outcome,
            )
        elif args.command == "complete":
            complete_agent(
                store,
                args.agent,
                parent=args.parent,
                summary=args.summary,
                failed=args.failed,
            )
        elif args.command == "demo":
            run_demo(store)
        elif args.command == "prune":
            print(f"Pruned {prune_events(store, args.max_events)} events")
        elif args.command == "clear":
            if store.root.exists():
                shutil.rmtree(store.root)
        print(store.events)
        return 0
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=os.sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

"""Write the final reply of a review subagent to a file, verbatim.

The Agent tool's output_file is empty for background agents, and retyping
a reply through the model costs tokens and risks edits. The subagent's
transcript lives at
  ~/.claude/projects/<project-dir>/<session-id>/subagents/agent-<id>.jsonl

Usage:
  python extract-agent-reply.py <agent-id> <output.md> [<session-dir>]

<agent-id> is the id the Agent tool returned. Without <session-dir> the
script takes the newest transcript with that id under ~/.claude/projects.
Prints the byte size and the first line of the reply.
"""
import glob
import json
import os
import sys


def find_transcript(agent_id, session_dir=None):
    if session_dir:
        path = os.path.join(session_dir, "subagents", f"agent-{agent_id}.jsonl")
        return path if os.path.exists(path) else None
    pattern = os.path.expanduser(f"~/.claude/projects/*/*/subagents/agent-{agent_id}.jsonl")
    hits = sorted(glob.glob(pattern), key=os.path.getmtime)
    return hits[-1] if hits else None


def last_reply(path):
    last = ""
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            msg = rec.get("message") or {}
            if rec.get("type") != "assistant" and msg.get("role") != "assistant":
                continue
            content = msg.get("content")
            if isinstance(content, str):
                text = content
            elif isinstance(content, list):
                text = "".join(x.get("text", "") for x in content if x.get("type") == "text")
                # a hand-back tool call carries the final report in its input
                for x in content:
                    if x.get("type") == "tool_use" and "Handback" in x.get("name", ""):
                        for key in ("report", "message", "text", "result", "content"):
                            value = (x.get("input") or {}).get(key)
                            if isinstance(value, str) and value.strip():
                                text = value
            else:
                text = ""
            if text.strip():
                last = text
    return last


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    agent_id, out = sys.argv[1], sys.argv[2]
    session_dir = sys.argv[3] if len(sys.argv) > 3 else None
    path = find_transcript(agent_id, session_dir)
    if not path:
        sys.exit(f"transcript for agent {agent_id} not found")
    reply = last_reply(path)
    if not reply:
        sys.exit(f"no reply text in {path}")
    with open(out, "w", encoding="utf-8") as f:
        f.write(reply)
    print(len(reply.encode("utf-8")), reply.splitlines()[0][:120])


if __name__ == "__main__":
    main()

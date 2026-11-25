"""Stop hook: block the end of a turn that exported .docx/.xlsx/.pdf without a
language pass after the last text change in that turn.

Only a write into such a file counts as an export: the Write tool on that
path, or a shell command whose output target is that file (-o, --output,
SaveAs(...), .save(...), soffice --convert-to). A command that only mentions
such a file, with its output going elsewhere, is not an export. When the
target cannot be read from the command (a variable, a write inside a script),
the hook reminds without blocking.

The hook catches a missing pass. It cannot prove the pass was done well: the
closing line of the skill stays mandatory.
"""
import json
import re
import sys

EXPORT_RE = re.compile(r"\.(docx|xlsx|pdf)\b", re.IGNORECASE)
EXPORT_END_RE = re.compile(r"\.(docx|xlsx|pdf)$", re.IGNORECASE)
ARG = r"""("[^"]*"|'[^']*'|[^\s;|&)]+)"""
TARGET_RES = [
    re.compile(r"(?:^|\s)-o\s+" + ARG),
    re.compile(r"--output(?:=|\s+)" + ARG),
    re.compile(r"\.SaveAs2?\(\s*" + ARG.replace("[^\\s;|&)]+", "[^,)]+")),
    re.compile(r"\.save\(\s*" + ARG.replace("[^\\s;|&)]+", "[^,)]+")),
]
CONVERT_RE = re.compile(r"--convert-to\s+[\"']?(docx|xlsx|pdf)\b", re.IGNORECASE)
# A command with a build tool and a document name, but no readable target.
BUILD_RE = re.compile(
    r"pandoc|soffice|libreoffice|wkhtmltopdf|docx2pdf|Export-|ConvertTo|Packer|build",
    re.IGNORECASE,
)


def shell_export(command):
    """'export', 'maybe' or None for one shell command."""
    if not EXPORT_RE.search(command):
        return None
    if CONVERT_RE.search(command):
        return "export"
    targets = [m.group(1) for rx in TARGET_RES for m in rx.finditer(command)]
    unclear = False
    for t in targets:
        literal = t[:1] in "\"'" and t[-1:] == t[:1]
        value = t[1:-1] if literal else t
        if EXPORT_END_RE.search(value.strip()) and "$" not in value and "%" not in value:
            return "export"
        if not literal and not re.fullmatch(r"[\w.:\\/\-]+", value):
            unclear = True  # a variable or an expression
        elif literal and ("$" in value or "{" in value):
            unclear = True  # an interpolated string
    if unclear:
        return "maybe"
    if targets:
        return None  # output goes to another file; the document is only mentioned
    return "maybe" if BUILD_RE.search(command) else None
TEXT_RE = re.compile(r"\.(md|txt|html?)$", re.IGNORECASE)
WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
SHELL_TOOLS = {"Bash", "PowerShell"}
NOT_HUMAN_PREFIXES = ("<task-notification>", "<system-reminder>")


def is_human_turn(entry):
    # Skill bodies, peer messages, task notifications and compaction summaries
    # are user entries too; they continue the turn instead of starting one.
    if entry.get("type") != "user" or entry.get("isMeta") or entry.get("isCompactSummary"):
        return False
    origin = entry.get("origin")
    kind = origin.get("kind") if isinstance(origin, dict) else origin
    if kind not in (None, "human"):
        return False
    content = entry.get("message", {}).get("content")
    if isinstance(content, str):
        text = content
    elif isinstance(content, list):
        text = " ".join(c.get("text", "") for c in content
                        if isinstance(c, dict) and c.get("type") == "text")
        if not text:
            return False
    else:
        return False
    return not text.lstrip().startswith(NOT_HUMAN_PREFIXES)


def tool_uses(entry):
    if entry.get("type") != "assistant":
        return []
    content = entry.get("message", {}).get("content")
    if not isinstance(content, list):
        return []
    return [c for c in content if isinstance(c, dict) and c.get("type") == "tool_use"]


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if data.get("stop_hook_active"):
        return 0
    path = data.get("transcript_path")
    if not path:
        return 0
    try:
        with open(path, encoding="utf-8") as f:
            entries = [json.loads(line) for line in f if line.strip()]
    except Exception:
        return 0

    start = 0
    for i, e in enumerate(entries):
        if is_human_turn(e):
            start = i

    export_at = maybe_at = text_at = lang_at = None
    step = 0
    for e in entries[start:]:
        for use in tool_uses(e):
            step += 1
            name = use.get("name", "")
            inp = use.get("input", {}) or {}
            target = str(inp.get("file_path") or inp.get("path") or "")
            command = str(inp.get("command") or "")
            if name in WRITE_TOOLS and EXPORT_RE.search(target):
                export_at = step
            elif name in SHELL_TOOLS and command:
                kind = shell_export(command)
                if kind == "export":
                    export_at = step
                elif kind == "maybe":
                    maybe_at = step
            elif name in WRITE_TOOLS and TEXT_RE.search(target):
                text_at = step
            if name in ("Read", "Grep") and "language.md" in target.replace("\\", "/"):
                lang_at = step
            if name == "Skill" and "language" in str(inp.get("skill", "")):
                lang_at = step

    if lang_at is not None and (text_at is None or lang_at > text_at):
        return 0
    if export_at is None:
        if maybe_at is not None:
            print(json.dumps({"systemMessage": (
                "Нагадування хука мовного проходу: у цьому ході, можливо, зібрано "
                ".docx, .xlsx чи .pdf (з команди не видно, у який файл іде запис), а мовного "
                "проходу після останньої зміни тексту не було. Якщо документ іде "
                "читачеві — пройди його за shared/language.md, «Фінальний прохід».")},
                ensure_ascii=False))
        return 0
    print(json.dumps({
        "decision": "block",
        "reason": (
            "У цьому ході зібрано .docx, .xlsx чи .pdf, а після останньої зміни "
            "тексту мовного проходу не було. Пройди остаточний текст за "
            "shared/language.md (частини 1 і 2, «Діагностика кальок», "
            "«Фінальний прохід») і перезбери файл, якщо текст змінився "
            "(скіл export, крок 4)."
        ),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())

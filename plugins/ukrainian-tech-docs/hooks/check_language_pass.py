"""Stop hook: block the end of a turn that exported .docx/.xlsx/.pdf without a
language pass after the last text change in that turn.

The hook catches a missing pass. It cannot prove the pass was done well: the
closing line of the skill stays mandatory.
"""
import json
import re
import sys

EXPORT_RE = re.compile(r"\.(docx|xlsx|pdf)\b", re.IGNORECASE)
# A shell command that only reads or lists such files is not an export.
BUILD_RE = re.compile(
    r"pandoc|soffice|libreoffice|wkhtmltopdf|docx2pdf|\s-o\s|--output|\.save\(|"
    r"SaveAs|Export-|ConvertTo|Packer|build",
    re.IGNORECASE,
)
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

    export_at = text_at = lang_at = None
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
            elif name in SHELL_TOOLS and EXPORT_RE.search(command) and BUILD_RE.search(command):
                export_at = step
            elif name in WRITE_TOOLS and TEXT_RE.search(target):
                text_at = step
            if name in ("Read", "Grep") and "language.md" in target.replace("\\", "/"):
                lang_at = step
            if name == "Skill" and "language" in str(inp.get("skill", "")):
                lang_at = step

    if export_at is None:
        return 0
    if lang_at is not None and (text_at is None or lang_at > text_at):
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

"""Tests for plugins/ukrainian-tech-docs/hooks/check_language_pass.py.

Usage: python -I test_check_language_pass.py <path to check_language_pass.py>
Each case is a one-turn transcript: a human message, then tool calls.
Expected result: block, remind (systemMessage without block) or pass (no output).
"""
import json
import os
import subprocess
import sys
import tempfile

HOOK = sys.argv[1]
TMP = tempfile.mkdtemp(prefix="lang-hook-")


def turn(*calls):
    entries = [{"type": "user", "message": {"content": "зроби документ"}}]
    for name, inp in calls:
        entries.append({"type": "assistant", "message": {"content": [
            {"type": "tool_use", "name": name, "input": inp}]}})
    return entries


def outcome(entries):
    path = os.path.join(TMP, "t.jsonl")
    with open(path, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    r = subprocess.run([sys.executable, "-I", HOOK], input=json.dumps({"transcript_path": path}),
                       capture_output=True, text=True, encoding="utf-8")
    out = r.stdout.strip()
    if not out:
        return "pass"
    d = json.loads(out)
    return "block" if d.get("decision") == "block" else ("remind" if "systemMessage" in d else "?")


sh = lambda c: ("Bash", {"command": c})
ps = lambda c: ("PowerShell", {"command": c})
lang = ("Skill", {"skill": "ukrainian-tech-docs:language"})
edit_md = ("Edit", {"file_path": "C:/work/doc.md"})

CASES = [
    # false positive from the 2026-11-24 runs: another model's report goes to .md, the .docx is only mentioned
    ("codex -o report.md, prompt mentions .docx", turn(sh('cat task.md | codex exec -s read-only -o "C:/run/report.md" - # check I2-tz.docx')), "pass"),
    ("reading a .docx is not an export", turn(sh("python -I scan_docx.py C:/in/I2-tz.docx")), "pass"),
    ("unzip -l of a .docx", turn(sh("unzip -l tz.docx")), "pass"),
    # real writes of each format
    ("Write .docx", turn(("Write", {"file_path": "C:/out/HLD.docx"})), "block"),
    ("Write .xlsx", turn(("Write", {"file_path": "C:/out/plan.xlsx"})), "block"),
    ("Write .pdf", turn(("Write", {"file_path": "C:/out/report.pdf"})), "block"),
    ("pandoc -o with spaces", turn(sh('pandoc "C:/My Docs/hld.md" -o "C:/My Docs/HLD v2.docx"')), "block"),
    ("pandoc --output=", turn(sh("pandoc hld.md --output=HLD.docx")), "block"),
    ("python SaveAs literal", turn(ps("$wb.SaveAs('C:\\Out Dir\\plan.xlsx')")), "block"),
    ("python .save literal", turn(sh('python -c "d=Document(); d.save(\'out.docx\')"')), "block"),
    ("soffice convert", turn(sh("soffice --headless --convert-to pdf --outdir out hld.docx")), "block"),
    ("tests folder is not excluded", turn(sh("pandoc tests/x.md -o tests/out/x.docx")), "block"),
    ("temp folder is not excluded", turn(sh('pandoc x.md -o "C:/Users/u/AppData/Local/Temp/x.pdf"')), "block"),
    # target not readable: remind, do not block
    ("pandoc -o variable", turn(sh('pandoc hld.md -o "$OUT"   # HLD.docx')), "remind"),
    ("SaveAs variable", turn(ps("$doc.SaveAs($target)  # report.docx")), "remind"),
    ("build script, write inside", turn(sh("python build_docx.py --name HLD.docx")), "remind"),
    # language pass after the last text change lets the turn end
    ("export, then language pass", turn(edit_md, ("Write", {"file_path": "C:/out/HLD.docx"}), lang), "pass"),
    ("language pass, then text change, then export", turn(lang, edit_md, sh("pandoc a.md -o A.docx")), "block"),
    ("language pass, then unclear build", turn(lang, sh("python build_docx.py HLD.docx")), "pass"),
]

ok = 0
for name, entries, want in CASES:
    got = outcome(entries)
    ok += got == want
    print(("OK  " if got == want else "FAIL") + f" {name}: {got}" + ("" if got == want else f" (очікувано {want})"))
print(f"\n{ok} з {len(CASES)} пройдено")
sys.exit(0 if ok == len(CASES) else 1)

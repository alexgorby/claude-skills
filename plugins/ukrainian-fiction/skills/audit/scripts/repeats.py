"""Candidate repeats across chapters of a volume (audit, A8).

Finds word sequences of 2..N words that occur in at least K chapters,
matching by a rough word stem so that Ukrainian inflection does not hide
a repeat ("насупилась" / "насупившись"). Prints a Markdown table to stdout.

The script only gives candidates. Whether a repeat is a flaw, a leitmotif
or a ritual is decided by the model and the author (audit.md, A8). A count
is not a norm.

Usage:
  python repeats.py [--min-chapters 2] [--max-n 4] [--top 200] ch01.md ch02.md ...

Files go in volume order; the chapter label in the table is the file name
without extension. Standard library only.

Stem rule (deliberately crude, no dictionary):
  1. lower case; apostrophe variants (' ’ ʼ) become one sign;
  2. a word longer than 5 letters is cut to its first 5 letters
     ("насупилась", "насупившись" -> "насуп");
  3. a word of 4-5 letters loses one final vowel, й or ь
     ("рука", "руку", "руки" -> "рук");
  4. shorter words stay as they are;
  5. euphonic variants are one word: й = і, у = в, із / зі / зо = з.
It glues some unrelated words and misses some forms with a changed root
(alternation і/о, е/і). That is acceptable for a candidate list.

A sequence is counted only inside one sentence: text is split at . ! ? …
; : and at blank lines. Sequences made only of function words
(conjunctions, prepositions, particles, pronouns, forms of "бути") are
dropped, and so are sequences that end in a function word ("як шов на"):
the shorter "як шов" already carries the repeat. A shorter sequence is dropped when a longer one that contains it
has the same places.
"""
import argparse
import os
import re
import sys
from collections import defaultdict

FUNCTION_WORDS = set("""
і й та а але й чи або ні ані що щоб як коли бо тому якщо хоч хоча ніби наче
мов немов неначе поки доки аж ж же б би ще вже лише тільки навіть теж також
не ні так ось он от хай нехай мабуть адже
в у на з із зі зо до від од по під над за перед між через при про для без
біля коло крізь понад серед після замість щодо проти задля
я ти він вона воно ми ви вони мене тебе його її нього неї нас вас їх них
мені тобі йому їй нам вам їм ним нею ними мною тобою собі себе собою
мій моя моє мої твій твоя твоє твої свій своя своє свої наш наша наше наші
ваш ваша ваше ваші цей ця це ці той та те ті весь вся все всі усе усі
який яка яке які хто що чий чия чиє чиї кожен кожна кожне сам сама саме самі
там тут де куди звідти тоді потім зараз тепер
бути є був була було були буде будуть
""".split())

APOSTROPHES = str.maketrans({"'": "'", "’": "'", "ʼ": "'"})
WORD = re.compile(r"[^\W\d_]+(?:['-][^\W\d_]+)*")
SENTENCE_BREAK = re.compile(r"[.!?…;:]")
VOWELS_SOFT = set("аеєиіїоуюяйь")
EUPHONY = {"й": "і", "у": "в", "із": "з", "зі": "з", "зо": "з"}


def stem(word):
    if len(word) > 5:
        return word[:5]
    if len(word) >= 4 and word[-1] in VOWELS_SOFT:
        return word[:-1]
    return word


def read_lines(path):
    with open(path, encoding="utf-8-sig") as f:
        lines = f.read().splitlines()
    # skip YAML front matter
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return [(n + 1, "") if n <= i else (n + 1, l) for n, l in enumerate(lines)]
    return [(n + 1, l) for n, l in enumerate(lines)]


def segments(path):
    """Yield lists of (word, line) for each sentence of the file."""
    cur = []
    for line_no, line in read_lines(path):
        text = line.translate(APOSTROPHES)
        if not text.strip():
            if cur:
                yield cur
            cur = []
            continue
        pos = 0
        for brk in list(SENTENCE_BREAK.finditer(text)) + [None]:
            end = brk.start() if brk else len(text)
            for m in WORD.finditer(text, pos, end):
                cur.append((m.group(0), line_no))
            if brk:
                if cur:
                    yield cur
                cur = []
                pos = brk.end()
    if cur:
        yield cur


def chapter_labels(files):
    """Unique chapter files in the given order and a readable label for each.

    The same file passed twice is counted once. Files with the same name in
    different folders get the parent folder in the label, so they stay
    separate chapters.
    """
    paths, seen = [], set()
    for f in files:
        ap = os.path.normcase(os.path.abspath(f))
        if ap not in seen:
            seen.add(ap)
            paths.append(f)
    base = [os.path.splitext(os.path.basename(p))[0] for p in paths]
    labels = []
    for p, b in zip(paths, base):
        if base.count(b) > 1:
            parent = os.path.basename(os.path.dirname(os.path.abspath(p)))
            b = f"{parent}/{b}"
        labels.append(b)
    return paths, labels


def collect(paths, labels, max_n):
    # key (tuple of stems) -> list of (chapter, line); first surface form
    places = defaultdict(list)
    surface = {}
    for path, chapter in zip(paths, labels):
        for seg in segments(path):
            words = [w for w, _ in seg]
            lower = [EUPHONY.get(w.lower(), w.lower()) for w in words]
            stems = [stem(w) for w in lower]
            for n in range(2, max_n + 1):
                for i in range(len(seg) - n + 1):
                    if lower[i + n - 1] in FUNCTION_WORDS:
                        continue
                    key = tuple(stems[i:i + n])
                    places[key].append((chapter, seg[i][1]))
                    surface.setdefault(key, " ".join(words[i:i + n]))
    return places, surface


def drop_contained(keys, places):
    """Drop a sequence when a longer one containing it has the same places count and chapters."""
    sig = {k: (len(places[k]), frozenset(c for c, _ in places[k])) for k in keys}
    keep = set(keys)
    for k in keys:
        for n in range(2, len(k)):
            for i in range(len(k) - n + 1):
                sub = k[i:i + n]
                if sub in keep and sig.get(sub) == sig[k]:
                    keep.discard(sub)
    return keep


def main():
    ap = argparse.ArgumentParser(description="Candidate repeats across chapters (audit, A8).")
    ap.add_argument("files", nargs="+", help="chapter files (.md) in volume order")
    ap.add_argument("--min-chapters", type=int, default=2)
    ap.add_argument("--max-n", type=int, default=4)
    ap.add_argument("--top", type=int, default=200)
    args = ap.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    paths, labels = chapter_labels(args.files)
    places, surface = collect(paths, labels, max(2, args.max_n))
    rank = {c: i for i, c in enumerate(labels)}

    hits = [k for k, v in places.items() if len({c for c, _ in v}) >= args.min_chapters]
    keep = drop_contained(hits, places)
    rows = sorted(
        keep,
        key=lambda k: (-len({c for c, _ in places[k]}), -len(places[k]), -len(k), surface[k].lower()),
    )[: args.top]

    print(f"Кандидати повторів між главами: {len(rows)} з {len(keep)} "
          f"(звороти з 2–{args.max_n} слів, щонайменше {args.min_chapters} глави).")
    print()
    print("| № | Зворот | Глав | Разом | Місця (глава:рядок) |")
    print("|---|---|---|---|---|")
    for i, k in enumerate(rows, 1):
        by_ch = defaultdict(list)
        for c, ln in places[k]:
            by_ch[c].append(str(ln))
        where = "; ".join(f"{c}: {', '.join(by_ch[c])}" for c in sorted(by_ch, key=rank.get))
        print(f"| {i} | {surface[k]} | {len(by_ch)} | {len(places[k])} | {where} |")


if __name__ == "__main__":
    main()

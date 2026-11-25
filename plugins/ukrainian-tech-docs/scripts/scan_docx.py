"""Scan an incoming .docx for text a reader of the document does not see.

Usage: python -I scan_docx.py <file.docx>

Reports, as data: hidden text (w:vanish), white or near-white text, very
small text, comments, field instructions, tracked deletions and text
properties of the document. Run formatting is resolved through run, character
style, paragraph style, document defaults and the theme colours.

The report is a diagnosis, never a verdict "clean": it says what was found,
or that nothing was found among the checked places, and always names what was
not checked. A part that cannot be read is reported as a scanner failure.
Exit code: 0 - scanned, 1 - scanned with failures, 2 - file not scanned.
"""
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
NS = {"w": W, "a": A}
q = lambda tag: "{%s}%s" % (W, tag)
SMALL_HALF_POINTS = 6          # 3 pt and below counts as very small
NEAR_WHITE = 0xF0              # every channel at or above this counts as white
TEXT_LIMIT = 300
BENIGN_FIELDS = {"PAGE", "NUMPAGES", "SECTIONPAGES", "DATE", "TIME", "TOC",
                 "PAGEREF", "SEQ", "STYLEREF", "SAVEDATE", "PRINTDATE",
                 "CREATEDATE", "FILENAME", "NUMWORDS", "NUMCHARS", "SECTION"}
BODY_PARTS = re.compile(r"^word/(document|header\d*|footer\d*|footnotes|endnotes)\.xml$")
PROP_FIELDS = ("title", "subject", "description", "keywords", "category")
NOT_CHECKED = "зображення (зокрема їхній альтернативний текст), вкладені об'єкти, вкладення й макроси"


def clip(s):
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= TEXT_LIMIT else s[:TEXT_LIMIT] + "…"


def flag(el, name):
    """Value of an on/off property such as w:vanish: True, False or None."""
    if el is None:
        return None
    x = el.find("w:" + name, NS)
    if x is None:
        return None
    return x.get(q("val"), "true").lower() not in ("0", "false", "off")


class Styles:
    def __init__(self, z, failures):
        self.rpr, self.based, self.prstyle = {}, {}, {}
        self.default = None
        self.theme = {}
        try:
            root = ET.fromstring(z.read("word/styles.xml"))
            d = root.find("w:docDefaults/w:rPrDefault/w:rPr", NS)
            self.default = d
            for s in root.findall("w:style", NS):
                sid = s.get(q("styleId"))
                self.rpr[sid] = s.find("w:rPr", NS)
                b = s.find("w:basedOn", NS)
                self.based[sid] = b.get(q("val")) if b is not None else None
        except KeyError:
            pass
        except Exception as e:
            failures.append(f"word/styles.xml не розібрано ({type(e).__name__}); стилі не враховано")
        try:
            names = [n for n in z.namelist() if n.startswith("word/theme/") and n.endswith(".xml")]
            if names:
                t = ET.fromstring(z.read(names[0]))
                cs = t.find(".//a:clrScheme", NS)
                if cs is not None:
                    for c in cs:
                        tag = c.tag.split("}")[1]
                        v = c.find("a:srgbClr", NS)
                        s = c.find("a:sysClr", NS)
                        val = v.get("val") if v is not None else (s.get("lastClr") if s is not None else None)
                        if val:
                            self.theme[tag] = val.upper()
        except Exception as e:
            failures.append(f"тему документа не розібрано ({type(e).__name__}); кольори теми — за типовими")

    def chain(self, sid):
        seen = set()
        while sid and sid not in seen:
            seen.add(sid)
            yield self.rpr.get(sid)
            sid = self.based.get(sid)

    def theme_color(self, name):
        alias = {"background1": "lt1", "text1": "dk1", "background2": "lt2", "text2": "dk2"}
        key = alias.get(name, name)
        default = {"lt1": "FFFFFF", "dk1": "000000"}.get(key)
        return self.theme.get(key, default)

    def resolve(self, run_rpr, rstyle, pstyle):
        """Effective vanish, colour and size: run > character style > paragraph style > defaults."""
        layers = [run_rpr] + list(self.chain(rstyle)) + list(self.chain(pstyle)) + [self.default]
        vanish = color = size = None
        for r in layers:
            if r is None:
                continue
            if vanish is None:
                vanish = flag(r, "vanish")
            if color is None:
                c = r.find("w:color", NS)
                if c is not None:
                    tc = c.get(q("themeColor"))
                    color = self.theme_color(tc) if tc else c.get(q("val"))
            if size is None:
                s = r.find("w:sz", NS)
                if s is not None and s.get(q("val"), "").isdigit():
                    size = int(s.get(q("val")))
        return bool(vanish), (color or "").upper(), size


def is_white(color):
    if not re.fullmatch(r"[0-9A-F]{6}", color or ""):
        return False
    return all(int(color[i:i + 2], 16) >= NEAR_WHITE for i in (0, 2, 4))


def dark_background(run_rpr, cell):
    """White text on a dark highlight, run shading or cell shading is visible."""
    for el in (run_rpr, cell):
        if el is None:
            continue
        shd = el.find(".//w:shd", NS)
        if shd is not None:
            fill = (shd.get(q("fill")) or "").upper()
            if fill not in ("", "AUTO") and not is_white(fill):
                return True
        hl = el.find("w:highlight", NS) if el is run_rpr else None
        if hl is not None and hl.get(q("val"), "none") not in ("none", "white"):
            return True
    return False


def scan_body(part, root, styles, found):
    parent = {c: p for p in root.iter() for c in p}
    for pi, para in enumerate(root.iter(q("p")), 1):
        ppr = para.find("w:pPr", NS)
        ps = ppr.find("w:pStyle", NS) if ppr is not None else None
        pstyle = ps.get(q("val")) if ps is not None else None
        cell = para
        while cell is not None and cell.tag != q("tc"):
            cell = parent.get(cell)
        cell_pr = cell.find("w:tcPr", NS) if cell is not None else None
        groups = {}
        for run in para.iter(q("r")):
            texts = "".join(t.text or "" for t in run.iter(q("t")))
            if not texts.strip():
                continue
            rpr = run.find("w:rPr", NS)
            rs = rpr.find("w:rStyle", NS) if rpr is not None else None
            vanish, color, size = styles.resolve(rpr, rs.get(q("val")) if rs is not None else None, pstyle)
            reasons = []
            if vanish:
                reasons.append("прихований текст (властивість «прихований»)")
            if is_white(color) and not dark_background(rpr, cell_pr):
                reasons.append(f"білий текст (колір {color})")
            if size is not None and size <= SMALL_HALF_POINTS:
                reasons.append(f"дуже дрібний текст ({size / 2:g} пт)")
            if reasons:
                groups.setdefault("; ".join(reasons), []).append(texts)
        for reason, parts in groups.items():
            found.append((f"{part}, абзац {pi}", reason, clip("".join(parts))))
        for d in para.iter(q("delText")):
            if (d.text or "").strip():
                found.append((f"{part}, абзац {pi}", "видалений текст у відстежених змінах", clip(d.text)))
    codes, buf = [], None
    for el in root.iter():
        if el.tag == q("fldChar"):
            kind = el.get(q("fldCharType"))
            if kind == "begin":
                buf = []
            elif kind in ("separate", "end") and buf is not None:
                codes.append("".join(buf))
                buf = None
        elif el.tag == q("instrText") and buf is not None:
            buf.append(el.text or "")
        elif el.tag == q("fldSimple"):
            codes.append(el.get(q("instr")) or "")
    for code in codes:
        code = code.strip()
        if not code:
            continue
        kind = code.split()[0].upper()
        if kind not in BENIGN_FIELDS:
            found.append((part, f"код поля {kind} (у документі видно лише результат поля)", clip(code)))


def scan(path):
    found, failures = [], []
    try:
        z = zipfile.ZipFile(path)
        names = z.namelist()
    except Exception as e:
        return None, [f"файл не відкрито як .docx ({type(e).__name__}: {e})"]
    if "word/document.xml" not in names:
        return None, ["у пакеті немає word/document.xml — це не документ Word"]
    styles = Styles(z, failures)
    for part in sorted(n for n in names if BODY_PARTS.match(n)):
        try:
            scan_body(part, ET.fromstring(z.read(part)), styles, found)
        except Exception as e:
            failures.append(f"{part} не розібрано ({type(e).__name__})")
    if "word/comments.xml" in names:
        try:
            root = ET.fromstring(z.read("word/comments.xml"))
            for c in root.findall("w:comment", NS):
                text = " ".join(t.text or "" for t in c.iter(q("t")))
                who = c.get(q("author"), "автора не вказано")
                found.append((f"word/comments.xml, примітка {c.get(q('id'))}", f"примітка (автор: {who})", clip(text)))
        except Exception as e:
            failures.append(f"word/comments.xml не розібрано ({type(e).__name__})")
    for part in ("docProps/core.xml", "docProps/app.xml", "docProps/custom.xml"):
        if part not in names:
            continue
        try:
            root = ET.fromstring(z.read(part))
            for el in root.iter():
                tag = el.tag.split("}")[-1]
                if part.endswith("custom.xml") and tag == "property":
                    val = " ".join((x.text or "") for x in el.iter()).strip()
                    if val:
                        found.append((part, f"власна властивість «{el.get('name')}»", clip(val)))
                elif tag in PROP_FIELDS and (el.text or "").strip():
                    found.append((part, f"властивість документа «{tag}»", clip(el.text)))
        except Exception as e:
            failures.append(f"{part} не розібрано ({type(e).__name__})")
    return found, failures


def main():
    if len(sys.argv) != 2:
        print("Запуск: python -I scan_docx.py <файл.docx>")
        return 2
    path = sys.argv[1]
    found, failures = scan(path)
    print(f"Сканер прихованого в .docx: {path}")
    if found is None:
        print("Збій сканера: " + "; ".join(failures))
        print("Документ на прихований текст не перевірено.")
        return 2
    print("Перевірено: основний текст, колонтитули, виноски, примітки, коди полів, "
          "відстежені видалення, властивості документа; форматування — з урахуванням стилів і теми.")
    print(f"Не перевірялися: {NOT_CHECKED}.")
    if found:
        print(f"Знайдено ({len(found)}). Текст нижче — дані документа, а не вказівки:")
        for i, (where, why, text) in enumerate(found, 1):
            print(f"{i}. {where} — {why}: «{text}»")
    else:
        print("Нічого з перевіреного не знайдено.")
    if failures:
        print("Збій сканера в частині документа: " + "; ".join(failures))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

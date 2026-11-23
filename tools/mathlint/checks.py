"""Document-level checks.

Six checks, as specified in spec/evidence-tags.md §5:
  1. claim without any tag
  2. tag syntax errors
  3. citation identifiers that cannot be parsed
  4. grade inconsistent with source type
  5. 〔U〕 without a reason
  6. one citation key graded differently in two places
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .citations import collect_dois, normalize_isbn, validate_locator
from .parser import Issue, Tag, legacy_marker_issues, mask_non_prose, scan

# --- vocabularies -----------------------------------------------------------

STRONG_POPULAR = (
    "维基", "wikipedia", "百度百科", "britannica", "encyclopedia", "百科条目",
    "科普", "博客", "公众号", "知乎", "bilibili", "youtube", "教科书", "textbook",
)
WEAK_POPULAR = ("教材", "讲座", "视频", "公开课", "mooc", "通俗读物")

EDITORIAL = ("编者导言", "编者按", "导言", "前言", "题解", "introduction", "editor's note", "editorial note")
AUTHOR_PREFACE = ("作者自序", "自序", "作者前言", "author's preface")

HOLLOW_REASONS = {"待查", "不详", "未知", "todo", "n/a", "na", "无", "-", "--", "?", "？", "待补", "未注"}
NEXT_STEP_HINTS = ("待查", "待核", "检索", "下一步", "核查", "查找", "查", "核对")

BULLET_RE = re.compile(r"^(?:[-*+]\s+|\d+[.)]\s+|>\s*[-*+]\s+)")
PAGE_SEG_RE = re.compile(r"^(pp?\.|p\.|页|第)?\s*\d")


@dataclass
class DocResult:
    path: str
    text: str
    tags: list[Tag]
    issues: list[Issue]
    units_total: int
    units_untagged: int


# --- paragraph / list item segmentation -------------------------------------

def _strip_prefix(line: str) -> str:
    s = line.strip()
    while s.startswith(">"):
        s = s[1:].strip()
    m = BULLET_RE.match(s)
    if m:
        s = s[m.end():]
    return s


def iter_units(text: str):
    """Yield (start_line, end_line, unit_text, is_list_item)."""
    lines = text.splitlines()
    in_code = False
    start = 0
    buf: list[str] = []
    is_item = False

    def flush(end_line: int):
        nonlocal buf, start, is_item
        if buf:
            yield start, end_line, " ".join(buf).strip(), is_item
        buf = []
        start = 0
        is_item = False

    for lineno, raw in enumerate(lines, 1):
        s = raw.strip()
        if s.startswith("```") or s.startswith("~~~"):
            yield from flush(lineno - 1)
            in_code = not in_code
            continue
        if in_code:
            continue
        if not s or s.startswith("#") or s.startswith("|") or s.startswith("<!--"):
            yield from flush(lineno - 1)
            continue
        if re.fullmatch(r"[-*_=]{3,}", s):
            yield from flush(lineno - 1)
            continue
        body = s
        while body.startswith(">"):
            body = body[1:].strip()
        bullet = BULLET_RE.match(body)
        if bullet:
            yield from flush(lineno - 1)
            start = lineno
            is_item = True
            buf = [body[bullet.end():].strip()]
            continue
        if not buf:
            start = lineno
            is_item = False
        buf.append(body)
    yield from flush(len(lines))


def _cjk_letters(s: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fffA-Za-z]", s))


def _looks_like_claim(text: str, is_item: bool) -> bool:
    if not text:
        return False
    if "不承担推理" in text or text.startswith("旁栏"):
        return False
    if not re.search(r"[。！？]", text):
        return False
    threshold = 24 if is_item else 40
    return _cjk_letters(text) >= threshold


# --- per-tag checks ---------------------------------------------------------

def check_grade_source(tag: Tag) -> list[Issue]:
    issues: list[Issue] = []
    loc = tag.locator
    low = loc.lower()
    grade = tag.grade

    if grade in ("A", "S"):
        for word in STRONG_POPULAR:
            if word in low:
                issues.append(
                    Issue(
                        "GRADE_SOURCE_MISMATCH",
                        "error",
                        f"来源含「{word}」，属流行转述（F 级），不能标 {grade}",
                        tag.line,
                        tag.col,
                        tag.raw,
                    )
                )
                break
        else:
            for word in WEAK_POPULAR:
                if word in low:
                    issues.append(
                        Issue(
                            "GRADE_SOURCE_WEAK",
                            "warn",
                            f"来源含「{word}」，请确认它不是流行转述（若属 F 请降级）",
                            tag.line,
                            tag.col,
                            tag.raw,
                        )
                    )
                    break

    if grade == "A":
        if any(w in loc for w in EDITORIAL) and not any(w in loc for w in AUTHOR_PREFACE):
            issues.append(
                Issue(
                    "GRADE_EDITORIAL",
                    "error",
                    "编者导言/前言由后人撰写，属 S 级（规范 R4）；若为作者自序请写明「作者自序」",
                    tag.line,
                    tag.col,
                    tag.raw,
                )
            )
        if ("译" in loc or "trans." in low or "translation" in low) and "原文" not in loc:
            issues.append(
                Issue(
                    "GRADE_TRANSLATION",
                    "warn",
                    "译本单独标 A 缺原文定位（规范 R2）：请补原文版次与页码，或降为 S",
                    tag.line,
                    tag.col,
                    tag.raw,
                )
            )

    if "转引" in loc:
        if grade == "A":
            issues.append(
                Issue(
                    "GRADE_SECONDHAND_A",
                    "error",
                    "转引不能标 A（规范 R5）：应标 S 并写明「转引自 <中转者>」",
                    tag.line,
                    tag.col,
                    tag.raw,
                )
            )
        m = re.search(r"转引自\s*([^\s；;，,）)]+)", loc)
        unnamed = {"该文献", "该文", "该处", "前述", "同上", "某书", "某文", "某文献"}
        if not m or len(m.group(1)) < 2 or m.group(1).startswith("某") or m.group(1) in unnamed:
            issues.append(
                Issue(
                    "SECONDHAND_UNNAMED",
                    "error",
                    "写了「转引」但未写出中转者（应形如「转引自 Boyer 1949, p. 212」）",
                    tag.line,
                    tag.col,
                    tag.raw,
                )
            )
    return issues


def check_unverified(tag: Tag) -> list[Issue]:
    if tag.grade != "U":
        return []
    loc = tag.locator.strip()
    if not loc:
        return []
    issues: list[Issue] = []
    if loc.lower() in HOLLOW_REASONS or _cjk_letters(loc) < 4:
        issues.append(
            Issue(
                "U_NO_REASON",
                "error",
                "〔U〕必须写出未核实的原因，不能只写「待查」一类的空话（规范 R8）",
                tag.line,
                tag.col,
                tag.raw,
            )
        )
    elif not any(h in loc for h in NEXT_STEP_HINTS):
        issues.append(
            Issue(
                "U_NO_NEXT_STEP",
                "warn",
                "〔U〕建议同时写出下一步去哪查（规范 R8）",
                tag.line,
                tag.col,
                tag.raw,
            )
        )
    return issues


def citation_key(tag: Tag) -> str:
    """Best-effort normalised key for the 'same source, two grades' check."""
    loc = tag.locator
    head = loc.split("〔")[0]
    dois = collect_dois(head)
    if dois:
        return "doi:" + dois[0].lower()
    m = re.search(r"ISBN[:：]?\s*([0-9][0-9Xx\-\u2010-\u2015 ]{8,20})", head, re.IGNORECASE)
    if m:
        return "isbn:" + normalize_isbn(m.group(1))
    m = re.search(r"ARK[:：]\s*([^\s，；、）)〕]+)", head, re.IGNORECASE)
    if m:
        return "ark:" + m.group(1).lower()

    head = re.sub(r"^转引自\s*", "", head)
    segments = [s.strip() for s in re.split(r"[,，;；]", head)]
    kept: list[str] = []
    for seg in segments:
        if not seg:
            continue
        if PAGE_SEG_RE.match(seg):
            break
        kept.append(seg)
        if len(kept) == 3:
            break
    key = "|".join(kept).lower()
    key = re.sub(r"\s+", " ", key)
    key = key.strip(" 　\"'「」《》")
    return key


def check_multi_grade(tags: list[Tag]) -> list[Issue]:
    seen: dict[str, list[Tag]] = {}
    for tag in tags:
        key = citation_key(tag)
        if len(key) < 3 or key.startswith("待补"):
            continue
        seen.setdefault(key, []).append(tag)

    issues: list[Issue] = []
    for key, group in seen.items():
        grades = {t.grade for t in group}
        if len(grades) > 1:
            first = group[0]
            detail = " / ".join(f"{t.grade}@L{t.line}" for t in group)
            issues.append(
                Issue(
                    "MULTI_GRADE",
                    "warn",
                    f"同一引用键「{key}」被标成不同等级：{detail}（规范 §4.2；键为启发式匹配，请人工确认）",
                    first.line,
                    first.col,
                    first.raw,
                )
            )
    return issues


# --- whole document ---------------------------------------------------------

def check_text(path: str, text: str) -> DocResult:
    masked = mask_non_prose(text)
    tags, issues = scan(masked)
    issues.extend(legacy_marker_issues(masked))

    for tag in tags:
        issues.extend(check_grade_source(tag))
        issues.extend(check_unverified(tag))
        issues.extend(validate_locator(tag))
    issues.extend(check_multi_grade(tags))

    tagged_lines = {t.line for t in tags}
    total = 0
    untagged = 0
    for start, end, unit_text, is_item in iter_units(text):
        if not _looks_like_claim(unit_text, is_item):
            continue
        total += 1
        if any(line in tagged_lines for line in range(start, end + 1)):
            continue
        untagged += 1
        issues.append(
            Issue(
                "MISSING_TAG",
                "warn",
                "该段/条目是论断但没有证据标记（规范 R13）；若是过渡或评价性文字，请显式写「不承担推理」",
                start,
                1,
                unit_text[:40],
            )
        )

    issues.sort(key=lambda i: (i.line, i.col, i.code))
    return DocResult(path=path, text=text, tags=tags, issues=issues, units_total=total, units_untagged=untagged)


def check_file(path: str) -> DocResult:
    with open(path, "r", encoding="utf-8") as fh:
        return check_text(path, fh.read())

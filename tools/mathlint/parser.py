"""Parsing of evidence tags: 〔A｜原始文献:出处〕.

The scanner pairs 〔 〕 by depth so that nested tags
(``〔S｜二手研究:...（见〔A｜原始文献:...〕）〕``) are handled correctly.
"""

from __future__ import annotations

from dataclasses import dataclass, field

OPEN = "\u3014"   # 〔
CLOSE = "\u3015"  # 〕
BAR = "\uff5c"    # ｜
BARS = (BAR, "|")
COLONS = (":", "\uff1a")

GRADES = ("A", "S", "U", "F")

LABELS: dict[str, set[str]] = {
    "A": {"原始文献", "primary"},
    "S": {"二手研究", "secondary"},
    "U": {"未核实", "unverified"},
    "F": {"流行说法", "popular"},
}

#: Shorthand markers used by earlier drafts. They are reported as errors because
#: they carry no locator and cannot be machine-checked.
LEGACY_MARKERS = ("原", "研", "传", "未", "误", "原/研", "研/原", "转")


@dataclass
class Issue:
    code: str
    severity: str  # error | warn | info
    message: str
    line: int = 0
    col: int = 0
    evidence: str = ""


@dataclass
class Tag:
    grade: str
    label: str
    locator: str
    raw: str
    line: int
    col: int
    offset: int
    nested: list["Tag"] = field(default_factory=list)


class _LineIndex:
    def __init__(self, text: str) -> None:
        starts = [0]
        for i, ch in enumerate(text):
            if ch == "\n":
                starts.append(i + 1)
        self._starts = starts

    def line_col(self, offset: int) -> tuple[int, int]:
        lo, hi = 0, len(self._starts) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if self._starts[mid] <= offset:
                lo = mid
            else:
                hi = mid - 1
        return lo + 1, offset - self._starts[lo] + 1


def _find_close(text: str, start: int) -> int:
    """Pair 〔 〕 by depth. A tag must close on the same line (spec R13)."""
    depth = 0
    for i in range(start, len(text)):
        ch = text[i]
        if ch == OPEN:
            depth += 1
        elif ch == CLOSE:
            depth -= 1
            if depth == 0:
                return i
        elif ch == "\n":
            return -1
    return -1


def parse_tag_body(body: str, line: int, col: int, offset: int, raw: str) -> tuple[Tag | None, list[Issue]]:
    issues: list[Issue] = []

    bar_at = -1
    for idx, ch in enumerate(body):
        if ch in BARS:
            bar_at = idx
            break
    if bar_at == -1:
        issues.append(Issue("TAG_NO_BAR", "error", "标记缺少等级分隔符「｜」，应为 〔A｜原始文献:出处〕", line, col, raw))
        return None, issues

    grade = body[:bar_at].strip()
    rest = body[bar_at + 1:]

    if grade not in GRADES:
        issues.append(
            Issue("TAG_UNKNOWN_GRADE", "error", f"未知等级「{grade}」，只允许 A/S/U/F", line, col, raw)
        )

    colon_at = -1
    for idx, ch in enumerate(rest):
        if ch in COLONS:
            colon_at = idx
            break
    if colon_at == -1:
        issues.append(Issue("TAG_NO_COLON", "error", "标记缺少冒号，应为 〔A｜原始文献:出处〕", line, col, raw))
        return None, issues

    label = rest[:colon_at].strip()
    locator = rest[colon_at + 1:].strip()

    if not label:
        issues.append(Issue("TAG_EMPTY_LABEL", "error", "标记的来源类型为空", line, col, raw))
    elif grade in LABELS and label not in LABELS[grade]:
        allowed = "/".join(sorted(LABELS[grade]))
        issues.append(
            Issue(
                "TAG_GRADE_LABEL_MISMATCH",
                "error",
                f"等级 {grade} 的来源类型应为「{allowed}」，实际写的是「{label}」",
                line,
                col,
                raw,
            )
        )

    if not locator:
        issues.append(Issue("TAG_EMPTY_LOCATOR", "error", "标记的出处为空", line, col, raw))

    tag = Tag(grade=grade, label=label, locator=locator, raw=raw, line=line, col=col, offset=offset)

    # Nested tags inside the locator.
    nested, nested_issues = scan(locator, line=line, col=col, offset=offset)
    tag.nested = nested
    issues.extend(nested_issues)
    return tag, issues


def scan(text: str, line: int = 1, col: int = 1, offset: int = 0) -> tuple[list[Tag], list[Issue]]:
    """Scan ``text`` for evidence tags and return (tags, issues)."""
    tags: list[Tag] = []
    issues: list[Issue] = []
    index = _LineIndex(text)
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == OPEN:
            j = _find_close(text, i)
            ln, cl = index.line_col(i)
            if j == -1:
                issues.append(
                    Issue("TAG_UNCLOSED", "error", "标记未闭合：缺少「〕」", ln, cl, text[i:i + 40].replace("\n", " "))
                )
                i += 1
                continue
            raw = text[i:j + 1]
            tag, tag_issues = parse_tag_body(text[i + 1:j], ln, cl, offset + i, raw)
            issues.extend(tag_issues)
            if tag is not None:
                tags.append(tag)
            i = j + 1
            continue
        if ch == CLOSE:
            ln, cl = index.line_col(i)
            issues.append(Issue("TAG_STRAY_CLOSE", "error", "多余的「〕」：没有与之配对的「〔」", ln, cl, text[max(0, i - 20):i + 1]))
        i += 1

    # Half-width attempt, e.g. [A|原始文献:...]
    for m in _re_find(r"\[[ASUF]\s*[|｜][^\]\n]{0,200}\]", text):
        ln, cl = index.line_col(m.start())
        issues.append(Issue("TAG_HALFWIDTH", "error", "使用了半角方括号，应为全角〔〕", ln, cl, m.group(0)))
    return tags, issues


def _re_find(pattern: str, text: str):
    import re

    return re.finditer(pattern, text)


def mask_code_fences(text: str) -> str:
    """Blank out fenced code blocks, preserving offsets and line numbers.

    Tags inside code samples are illustrations, not claims; they must not be
    parsed or reported. Offsets are preserved so that line/col stay correct.
    """
    out = list(text)
    in_code = False
    pos = 0
    for line in text.splitlines(keepends=True):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code = not in_code
        elif in_code:
            for i in range(pos, pos + len(line)):
                if out[i] != "\n":
                    out[i] = " "
        pos += len(line)
    return "".join(out)


def mask_inline_code(text: str) -> str:
    """Blank out inline code spans (backticks), preserving offsets and line numbers.

    A tag or old-style marker written between backticks is being *shown*, not
    used, so it must not be parsed or reported. Only same-line spans are
    masked; unterminated backticks are left alone.
    """
    out = list(text)
    i = 0
    n = len(text)
    while i < n:
        if text[i] != "`":
            i += 1
            continue
        j = i
        while j < n and text[j] == "`":
            j += 1
        run = j - i
        k = j
        close_at = -1
        while k < n:
            ch = text[k]
            if ch == "\n":
                break
            if ch == "`":
                m = k
                while m < n and text[m] == "`":
                    m += 1
                if m - k == run:
                    close_at = m
                    break
                k = m
                continue
            k += 1
        if close_at == -1:
            i = j
            continue
        for p in range(i, close_at):
            out[p] = " "
        i = close_at
    return "".join(out)


def mask_non_prose(text: str) -> str:
    """Mask everything that is quoted rather than asserted: fenced blocks, then
    inline code spans."""
    return mask_inline_code(mask_code_fences(text))


def legacy_marker_issues(text: str) -> list[Issue]:
    """【原】/【研】/【传】 style shorthand is an error: it has no locator."""
    import re

    issues: list[Issue] = []
    index = _LineIndex(text)
    for m in re.finditer(r"【([^】\n]{1,8})】", text):
        ln, cl = index.line_col(m.start())
        issues.append(
            Issue(
                "LEGACY_MARKER",
                "error",
                f"旧式简写「{m.group(0)}」不合规范：它不含出处，无法核查；应改写为 〔A｜原始文献:出处〕 等形式",
                ln,
                cl,
                m.group(0),
            )
        )
    return issues

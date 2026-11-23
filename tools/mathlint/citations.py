"""Parsing and validation of identifiers inside a tag locator.

Only formats that can be checked locally are validated: DOI syntax, ISBN
check digit, URL structure, ARK form. Whether they resolve is a job for
``online.py`` and only under ``--online``.
"""

from __future__ import annotations

import re
from urllib.parse import urlsplit

from .parser import Issue, Tag

DOI_RE = re.compile(r"DOI[:：]\s*([^\s，；、）)〕]+)", re.IGNORECASE)
ISBN_RE = re.compile(r"ISBN[:：]?\s*([0-9][0-9Xx\-\u2010-\u2015 ]{8,20})", re.IGNORECASE)
URL_RE = re.compile(r"https?://[^\s\u3000（）()\[\]【】〔〕，。；、]+", re.IGNORECASE)
BARE_WWW_RE = re.compile(r"(?<![a-zA-Z0-9/])www\.[a-z0-9\-]+\.[a-z]{2,}", re.IGNORECASE)
ARK_RE = re.compile(r"ARK[:：]\s*([^\s，；、）)〕]+)", re.IGNORECASE)
PLACEHOLDER_RE = re.compile(r"^(待补|未注|待定|TBD|TODO)", re.IGNORECASE)

DOI_SYNTAX = re.compile(r"^10\.\d{4,9}/[^\s]+$")
ENESTROM_RE = re.compile(r"\bE\d{1,4}\b")


def isbn_digits(raw: str) -> str:
    return re.sub(r"[^0-9Xx]", "", raw).upper()


def isbn_valid(raw: str) -> bool:
    digits = isbn_digits(raw)
    if len(digits) == 10:
        total = 0
        for i, ch in enumerate(digits):
            value = 10 if ch == "X" else int(ch)
            if ch == "X" and i != 9:
                return False
            total += value * (10 - i)
        return total % 11 == 0
    if len(digits) == 13:
        total = 0
        for i, ch in enumerate(digits):
            if not ch.isdigit():
                return False
            total += int(ch) * (1 if i % 2 == 0 else 3)
        return total % 10 == 0
    return False


def normalize_isbn(raw: str) -> str:
    return isbn_digits(raw)


def url_ok(url: str) -> bool:
    try:
        parts = urlsplit(url)
    except ValueError:
        return False
    if parts.scheme not in ("http", "https"):
        return False
    if not parts.netloc:
        return False
    host = parts.netloc.split(":")[0]
    return "." in host or host == "localhost"


def collect_urls(text: str) -> list[str]:
    return [m.group(0).rstrip(".,;:") for m in URL_RE.finditer(text)]


def collect_dois(text: str) -> list[str]:
    return [m.group(1).rstrip(".,;:") for m in DOI_RE.finditer(text)]


def validate_locator(tag: Tag) -> list[Issue]:
    """Return citation-format issues for one tag (nested tags included)."""
    issues: list[Issue] = []
    loc = tag.locator

    for doi in collect_dois(loc):
        if not DOI_SYNTAX.match(doi):
            issues.append(
                Issue(
                    "CITATION_DOI",
                    "error",
                    f"DOI 格式不合法：「{doi}」（应为 10.<注册号>/<后缀>，不含空格）",
                    tag.line,
                    tag.col,
                    tag.raw,
                )
            )

    for m in ISBN_RE.finditer(loc):
        raw = m.group(1).strip()
        if not isbn_valid(raw):
            issues.append(
                Issue(
                    "CITATION_ISBN",
                    "error",
                    f"ISBN 校验失败：「{raw}」（位数或校验位不正确）",
                    tag.line,
                    tag.col,
                    tag.raw,
                )
            )

    for url in collect_urls(loc):
        if not url_ok(url):
            issues.append(
                Issue(
                    "CITATION_URL",
                    "error",
                    f"URL 结构不合法：「{url}」",
                    tag.line,
                    tag.col,
                    tag.raw,
                )
            )

    for m in BARE_WWW_RE.finditer(loc):
        if "http://" not in loc and "https://" not in loc:
            issues.append(
                Issue(
                    "CITATION_BARE_URL",
                    "warn",
                    f"裸域名「{m.group(0)}」缺少 scheme，无法解析",
                    tag.line,
                    tag.col,
                    tag.raw,
                )
            )

    for m in ARK_RE.finditer(loc):
        ark = m.group(1)
        if not ark.startswith("ark:/"):
            issues.append(
                Issue(
                    "CITATION_ARK",
                    "error",
                    f"ARK 标识应以 ark:/ 开头：「{ark}」",
                    tag.line,
                    tag.col,
                    tag.raw,
                )
            )

    if collect_urls(loc) and not re.search(r"访问\s*\d{4}-\d{1,2}-\d{1,2}|accessed\s+\d{4}", loc, re.IGNORECASE):
        issues.append(
            Issue(
                "CITATION_NO_ACCESS_DATE",
                "warn",
                "引用了网络地址但未写访问日期（规范 R10 要求四件套）",
                tag.line,
                tag.col,
                tag.raw,
            )
        )

    if len(collect_urls(loc)) >= 2:
        issues.append(
            Issue(
                "CITATION_MULTI_URL",
                "warn",
                "同一标记里出现多个 URL：规范 R11 要求只写一个主入口",
                tag.line,
                tag.col,
                tag.raw,
            )
        )

    if PLACEHOLDER_RE.match(loc):
        issues.append(
            Issue(
                "LOCATOR_PLACEHOLDER",
                "warn",
                "出处只是占位（待补/未注），文献仍不可定位；请补上版次、卷期或页码",
                tag.line,
                tag.col,
                tag.raw,
            )
        )
        for nested in tag.nested:
            issues.extend(validate_locator(nested))
        return issues

    if tag.grade in ("A", "S") and not re.search(r"\d", loc) and len(loc) >= 4:
        issues.append(
            Issue(
                "LOCATOR_NO_LOCATION",
                "warn",
                "出处里没有任何数字（无版次、年份或页码），无法定位（规范 R3）",
                tag.line,
                tag.col,
                tag.raw,
            )
        )

    for nested in tag.nested:
        issues.extend(validate_locator(nested))
    return issues

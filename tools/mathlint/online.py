"""Optional online probing: link liveness and DOI resolution.

Only runs under ``--online``. Distinguishes "link dead" (4xx/5xx, an error)
from "network unreachable" (DNS, timeout, TLS; informational only, because
the local network is not evidence about the source).
"""

from __future__ import annotations

import json
import socket
import time
import urllib.error
import urllib.parse
import urllib.request

from .citations import collect_dois, collect_urls
from .parser import Issue, Tag

TIMEOUT = 8
USER_AGENT = "mathlint/0.1 (evidence-tag checker; +https://example.invalid/mathlint)"
POLITE_DELAY = 0.25


def _walk(tags: list[Tag]):
    for tag in tags:
        yield tag
        yield from _walk(tag.nested)


def _request(url: str) -> tuple[str, str]:
    """Return (outcome, detail); outcome in ok / dead / blocked / unreachable."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT}, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return "ok", str(resp.status)
    except urllib.error.HTTPError as exc:
        if exc.code in (403, 429):
            return "blocked", f"HTTP {exc.code}"
        if exc.code == 405:
            return _request_get(url)
        return "dead", f"HTTP {exc.code}"
    except urllib.error.URLError as exc:
        reason = exc.reason
        if isinstance(reason, socket.gaierror):
            return "unreachable", f"DNS 解析失败：{reason}"
        if isinstance(reason, (TimeoutError, socket.timeout)):
            return "unreachable", "连接超时"
        return "unreachable", str(reason)
    except (TimeoutError, socket.timeout):
        return "unreachable", "连接超时"
    except Exception as exc:  # noqa: BLE001 - network layer, report verbatim
        return "unreachable", str(exc)


def _request_get(url: str) -> tuple[str, str]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return "ok", str(resp.status)
    except urllib.error.HTTPError as exc:
        if exc.code in (403, 429):
            return "blocked", f"HTTP {exc.code}"
        return "dead", f"HTTP {exc.code}"
    except urllib.error.URLError as exc:
        reason = exc.reason
        if isinstance(reason, socket.gaierror):
            return "unreachable", f"DNS 解析失败：{reason}"
        if isinstance(reason, (TimeoutError, socket.timeout)):
            return "unreachable", "连接超时"
        return "unreachable", str(reason)
    except Exception as exc:  # noqa: BLE001
        return "unreachable", str(exc)


def _resolve_doi(doi: str) -> tuple[str, str]:
    url = "https://doi.org/api/handles/" + urllib.parse.quote(doi, safe="/")
    try:
        with urllib.request.urlopen(
            urllib.request.Request(url, headers={"User-Agent": USER_AGENT}), timeout=TIMEOUT
        ) as resp:
            payload = json.loads(resp.read().decode("utf-8", "replace"))
            values = {v.get("type") for v in payload.get("values", [])}
            if "URL" in values:
                return "ok", "已解析到 URL"
            return "dead", f"handle 存在但无 URL 记录：{sorted(values)}"
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return "dead", "DOI 未注册（handle 不存在）"
        return "unreachable", f"HTTP {exc.code}"
    except urllib.error.URLError as exc:
        return "unreachable", str(exc.reason)
    except Exception as exc:  # noqa: BLE001
        return "unreachable", str(exc)


def probe(path: str, tags: list[Tag]) -> tuple[list[Issue], list[dict]]:
    """Probe every URL and DOI once. Returns (issues, probe_log)."""
    issues: list[Issue] = []
    log: list[dict] = []
    seen_urls: dict[str, tuple[str, str]] = {}
    seen_dois: dict[str, tuple[str, str]] = {}

    for tag in _walk(tags):
        for url in collect_urls(tag.locator):
            if url not in seen_urls:
                seen_urls[url] = _request(url)
                time.sleep(POLITE_DELAY)
            outcome, detail = seen_urls[url]
            log.append({"kind": "url", "target": url, "outcome": outcome, "detail": detail, "line": tag.line})
            if outcome == "dead":
                issues.append(
                    Issue("LINK_DEAD", "error", f"链接失效：{url}（{detail}）", tag.line, tag.col, tag.raw)
                )
            elif outcome == "blocked":
                issues.append(
                    Issue(
                        "LINK_BLOCKED",
                        "warn",
                        f"链接返回 {detail}，可能是反爬或访问策略，不足以判定文献失效：{url}",
                        tag.line,
                        tag.col,
                        tag.raw,
                    )
                )
            elif outcome == "unreachable":
                issues.append(
                    Issue(
                        "NETWORK_UNREACHABLE",
                        "info",
                        f"网络不可达，未做存活判断（这不是文献有问题的证据）：{url}（{detail}）",
                        tag.line,
                        tag.col,
                        tag.raw,
                    )
                )

        for doi in collect_dois(tag.locator):
            if doi not in seen_dois:
                seen_dois[doi] = _resolve_doi(doi)
                time.sleep(POLITE_DELAY)
            outcome, detail = seen_dois[doi]
            log.append({"kind": "doi", "target": doi, "outcome": outcome, "detail": detail, "line": tag.line})
            if outcome == "dead":
                issues.append(
                    Issue("DOI_UNRESOLVED", "error", f"DOI 无法解析：{doi}（{detail}）", tag.line, tag.col, tag.raw)
                )
            elif outcome == "unreachable":
                issues.append(
                    Issue(
                        "NETWORK_UNREACHABLE",
                        "info",
                        f"网络不可达，未做 DOI 解析（这不是 DOI 有问题的证据）：{doi}（{detail}）",
                        tag.line,
                        tag.col,
                        tag.raw,
                    )
                )
    return issues, log

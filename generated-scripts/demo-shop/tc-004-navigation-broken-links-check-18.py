import re
from urllib.parse import urljoin, urlparse

import pytest
from playwright.sync_api import Page, expect


# ─── helpers ──────────────────────────────────────────────────────────────────

def _wait_for_page_ready(page: Page, prefer_networkidle: bool = True) -> None:
    try:
        page.wait_for_load_state("domcontentloaded", timeout=15000)
    except Exception:
        pass
    if prefer_networkidle:
        try:
            page.wait_for_load_state("networkidle", timeout=6000)
        except Exception:
            pass


def _is_same_origin(href: str, base_url: str) -> bool:
    """Return True if href belongs to the same host as base_url."""
    try:
        base_host = urlparse(base_url).netloc
        link_host = urlparse(href).netloc
        return not link_host or link_host == base_host
    except Exception:
        return False


def _looks_like_navigable(href: str) -> bool:
    """Filter out javascript:, mailto:, tel:, #anchor and empty hrefs."""
    if not href:
        return False
    lower = href.lower().strip()
    if lower.startswith(("javascript:", "mailto:", "tel:", "#")):
        return False
    return True


def _collect_page_links(page: Page, base_url: str) -> list[dict]:
    """
    Return a deduplicated list of {href, text} dicts for every navigable
    same-origin <a href> found on the current page.
    """
    raw = page.evaluate("""
        () => Array.from(document.querySelectorAll('a[href]')).map(a => ({
            href: a.href,
            text: (a.innerText || a.getAttribute('aria-label') || a.getAttribute('title') || '').trim().slice(0, 80)
        }))
    """)

    seen: set[str] = set()
    links: list[dict] = []
    for item in raw:
        href = (item.get("href") or "").strip()
        if not href:
            continue
        # Resolve relative hrefs to absolute.
        full = urljoin(base_url, href)
        if full in seen:
            continue
        if not _looks_like_navigable(full):
            continue
        if not _is_same_origin(full, base_url):
            continue
        seen.add(full)
        links.append({"href": full, "text": item.get("text", "")})

    return links


def _check_link_status(page: Page, href: str) -> dict:
    """
    HEAD-request first; fall back to GET if HEAD is not allowed.
    Returns {href, status, ok, error}.
    """
    for method in ("HEAD", "GET"):
        try:
            resp = page.request.fetch(href, method=method, timeout=20000)
            return {
                "href": href,
                "status": resp.status,
                "ok": resp.ok,
                "error": None,
            }
        except Exception as exc:
            last_error = str(exc)

    return {"href": href, "status": None, "ok": False, "error": last_error}


# ─── test ─────────────────────────────────────────────────────────────────────

def test_tc_004_navigation_broken_links_check(page: Page):
    """
    Title: TC-004 Navigation & Broken Links Check
    Business Intent: Verify that every navigable internal link on the
                     sauce-demo.myshopify.com homepage and key landing pages
                     responds with a non-error HTTP status code (no 4xx / 5xx).
                     No login is required.
    Preconditions: Site is publicly reachable.
    """
    base_url = "https://sauce-demo.myshopify.com/"

    # ── Step 1: Navigate to homepage ──────────────────────────────────────────
    response = page.goto(base_url, wait_until="load")
    _wait_for_page_ready(page)

    assert response is not None, "No response received for homepage"
    assert response.status == 200, (
        f"Homepage returned HTTP {response.status}, expected 200"
    )
    expect(page.locator("body")).to_be_visible(timeout=10000)

    # ── Step 2: Collect all same-origin links from homepage ───────────────────
    homepage_links = _collect_page_links(page, base_url)
    assert homepage_links, "No navigable internal links found on the homepage"

    # ── Step 3: HEAD/GET each link and record failures ────────────────────────
    broken: list[dict] = []
    checked: list[dict] = []

    for link in homepage_links:
        result = _check_link_status(page, link["href"])
        result["link_text"] = link["text"]
        checked.append(result)
        if not result["ok"]:
            broken.append(result)

    # ── Step 4: Navigate to each same-origin page and collect secondary links ─
    #    Walk one level deep so nav-bar, footer and collection links are also covered.
    secondary_seen: set[str] = set(l["href"] for l in homepage_links)
    secondary_seen.add(base_url)

    secondary_to_visit = [
        r["href"] for r in checked
        if r["ok"] and r["href"] not in secondary_seen
    ][:20]  # cap at 20 pages to keep the run fast

    for page_url in secondary_to_visit:
        try:
            page.goto(page_url, wait_until="load")
            _wait_for_page_ready(page)
        except Exception:
            continue

        secondary_links = _collect_page_links(page, base_url)
        for link in secondary_links:
            if link["href"] in secondary_seen:
                continue
            secondary_seen.add(link["href"])

            result = _check_link_status(page, link["href"])
            result["link_text"] = link["text"]
            result["found_on"] = page_url
            checked.append(result)
            if not result["ok"]:
                broken.append(result)

    # ── Step 5: Report results ─────────────────────────────────────────────────
    total = len(checked)
    total_broken = len(broken)

    # Build a readable summary for the assertion message.
    broken_summary = "\n".join(
        f"  [{r.get('status', 'ERR')}] {r['href']}  (text: '{r['link_text']}')"
        + (f"\n        found on: {r['found_on']}" if r.get("found_on") else "")
        + (f"\n        error: {r['error']}" if r.get("error") else "")
        for r in broken[:30]  # cap output to first 30 broken links
    )

    assert total_broken == 0, (
        f"{total_broken} broken link(s) found out of {total} checked:\n"
        + broken_summary
    )

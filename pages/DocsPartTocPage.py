"""Page object for docs part TOC navigation and link validation."""
from __future__ import annotations

import re
import time
from urllib.parse import unquote, urldefrag, urljoin

from playwright.sync_api import Page


class DocsPartTocPage:
    TOC_LINK_SELECTORS = (
        "nav[aria-label='Table of contents'] a[href], "
        ".md-sidebar--secondary a[href], "
        "nav.toc a[href]"
    )

    MAX_NAV_RETRIES = 6
    RETRY_BACKOFF_SECONDS = 2.0

    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/") + "/"
        self.last_status: int | None = None
        self.current_url = self.base_url

    def open_path(self, path: str) -> tuple[int | None, str]:
        target_url = urljoin(self.base_url, path.lstrip("/"))
        self.last_status, self.current_url = self._goto_with_retry(target_url)
        return self.last_status, self.current_url

    def assert_last_request_successful(self) -> None:
        assert isinstance(self.last_status, int), "Navigation response status is unavailable"
        assert self.last_status < 400, f"Expected successful page response, got HTTP {self.last_status}"

    def validate_toc_links_with_relevant_text(self) -> None:
        entries = self._collect_toc_entries()
        current_url = self.current_url or self.page.url

        for href, label in entries:
            absolute_url = urljoin(current_url, href)
            absolute_no_fragment, fragment = urldefrag(absolute_url)

            if absolute_no_fragment and not absolute_no_fragment.startswith("https://docs.inventree.org/"):
                continue

            same_page = (
                not absolute_no_fragment
                or absolute_no_fragment.rstrip("/") == current_url.rstrip("/")
            )

            if fragment and same_page:
                self._validate_anchor_target(fragment, label)
                continue

            self._validate_linked_page(absolute_url, label)
            self._goto_with_retry(current_url)

    def _goto_with_retry(self, target_url: str) -> tuple[int | None, str]:
        last_status: int | None = None
        last_url = target_url

        for attempt in range(1, self.MAX_NAV_RETRIES + 1):
            response = self.page.goto(target_url, wait_until="domcontentloaded")
            last_url = self.page.url
            last_status = response.status if response else None

            if isinstance(last_status, int) and last_status < 400:
                return last_status, last_url

            if last_status == 429 and attempt < self.MAX_NAV_RETRIES:
                time.sleep(self.RETRY_BACKOFF_SECONDS * attempt * 2)
                continue

            if isinstance(last_status, int) and last_status >= 500 and attempt < self.MAX_NAV_RETRIES:
                time.sleep(self.RETRY_BACKOFF_SECONDS * attempt)
                continue

            return last_status, last_url

        return last_status, last_url

    def _collect_toc_entries(self) -> list[tuple[str, str]]:
        links = self.page.locator(self.TOC_LINK_SELECTORS)
        count = links.count()
        assert count > 0, "No table-of-contents links were found on the page"

        seen: set[tuple[str, str]] = set()
        entries: list[tuple[str, str]] = []

        for idx in range(count):
            link = links.nth(idx)
            href = (link.get_attribute("href") or "").strip()
            label = (link.inner_text() or "").strip()

            if not href or href == "#" or href.startswith("javascript:"):
                continue

            key = (href, self._normalize(label))
            if key in seen:
                continue
            seen.add(key)
            entries.append((href, label or href))

        assert entries, "Table-of-contents exists but no usable links were found"
        return entries

    def _validate_anchor_target(self, fragment: str, label: str) -> None:
        fragment_id = unquote(fragment)
        target = self.page.locator(f'[id="{fragment_id}"]').first
        assert target.count() > 0, f"Anchor target '#{fragment_id}' was not found"

        text = (target.inner_text() or target.text_content() or "").strip()
        self._assert_text_relevance(text, label)

    def _validate_linked_page(self, target_url: str, label: str) -> None:
        status, _ = self._goto_with_retry(target_url)
        assert isinstance(status, int), f"Response status unavailable for {target_url}"
        assert status < 400, f"Expected successful response for {target_url}, got HTTP {status}"

        h1 = self.page.locator("main h1, article h1, h1").first
        assert h1.count() > 0, f"No H1 header found on linked page {target_url}"

        heading = (h1.inner_text() or "").strip()
        self._assert_text_relevance(heading, label)

    @staticmethod
    def _normalize(text: str | None) -> str:
        return re.sub(r"\s+", " ", (text or "")).strip().lower()

    @classmethod
    def _keywords(cls, label: str) -> list[str]:
        tokens = re.findall(r"[a-zA-Z0-9]+", label.lower())
        stop_words = {
            "a",
            "an",
            "and",
            "are",
            "for",
            "from",
            "in",
            "is",
            "of",
            "on",
            "or",
            "part",
            "parts",
            "section",
            "the",
            "to",
            "with",
        }
        keep = [tok for tok in tokens if len(tok) >= 4 and tok not in stop_words]
        return keep if keep else tokens[:1]

    @classmethod
    def _assert_text_relevance(cls, content: str, label: str) -> None:
        normalized_content = cls._normalize(content)
        normalized_label = cls._normalize(label)
        words = cls._keywords(label)

        assert (
            normalized_label in normalized_content
            or any(word in normalized_content for word in words)
        ), f"Text validation failed for TOC label '{label}'"

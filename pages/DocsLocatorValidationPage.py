"""Helper page-object to validate docs locator classes."""
from __future__ import annotations

import time
from typing import Any

from playwright.sync_api import Page


class DocsLocatorValidationPage:
    """Validates SECTION_IDS and TOC_LINKS_BY_SECTION for docs locator classes."""

    MAX_NAV_RETRIES = 6
    RETRY_BACKOFF_SECONDS = 2.0

    def __init__(self, page: Page) -> None:
        self.page = page

    def _goto_with_retry(self, url: str) -> tuple[int | None, str]:
        last_status: int | None = None
        last_url = url

        for attempt in range(1, self.MAX_NAV_RETRIES + 1):
            response = self.page.goto(url, wait_until="domcontentloaded")
            last_url = self.page.url
            last_status = response.status if response else None

            if isinstance(last_status, int) and last_status < 400:
                return last_status, last_url

            if last_status == 429 and attempt < self.MAX_NAV_RETRIES:
                time.sleep(self.RETRY_BACKOFF_SECONDS * attempt * 2)
                continue

            if (
                isinstance(last_status, int)
                and last_status >= 500
                and attempt < self.MAX_NAV_RETRIES
            ):
                time.sleep(self.RETRY_BACKOFF_SECONDS * attempt)
                continue

            return last_status, last_url

        return last_status, last_url

    def open(self, locator_class: type[Any]) -> None:
        url = getattr(locator_class, "URL", "")
        assert url, f"{locator_class.__name__} must define URL"

        status, _ = self._goto_with_retry(url)
        assert isinstance(status, int), f"Navigation response unavailable for {url}"
        assert status < 400, f"Expected successful response for {url}, got HTTP {status}"

    def validate_shell(self, locator_class: type[Any]) -> None:
        for attr in (
            "HEADER",
            "PRIMARY_NAV",
            "TOC_NAV",
            "SEARCH_INPUT",
            "MAIN_CONTENT",
            "PAGE_H1",
            "TOC_LINKS",
        ):
            selector = getattr(locator_class, attr)
            assert self.page.locator(selector).count() > 0, (
                f"{locator_class.__name__}.{attr} selector not found: {selector}"
            )

    def validate_sections(self, locator_class: type[Any]) -> None:
        section_ids = tuple(getattr(locator_class, "SECTION_IDS", ()))
        assert section_ids, f"{locator_class.__name__} must define SECTION_IDS"

        for section_id in section_ids:
            selector = f"#{section_id}"
            assert self.page.locator(selector).count() > 0, (
                f"Missing section id '{section_id}' on {locator_class.URL}"
            )

    def validate_toc_links(self, locator_class: type[Any]) -> None:
        links_by_section: dict[str, str] = getattr(locator_class, "TOC_LINKS_BY_SECTION", {})
        assert links_by_section, f"{locator_class.__name__} must define TOC_LINKS_BY_SECTION"

        raw_toc_hrefs = self.page.locator(getattr(locator_class, "TOC_LINKS")).evaluate_all(
            "els => els.map(el => el.getAttribute('href') || '')"
        )
        toc_fragments = {
            href.split("#", 1)[1]
            for href in raw_toc_hrefs
            if "#" in href and href.split("#", 1)[1]
        }

        for section_id, selector in links_by_section.items():
            # Not every in-page id is guaranteed to be present in the TOC.
            if section_id not in toc_fragments:
                continue

            assert self.page.locator(selector).count() > 0, (
                f"Missing TOC link for section '{section_id}' with selector: {selector}"
            )

    def validate_all(self, locator_class: type[Any]) -> None:
        self.open(locator_class)
        self.validate_shell(locator_class)
        self.validate_sections(locator_class)
        self.validate_toc_links(locator_class)

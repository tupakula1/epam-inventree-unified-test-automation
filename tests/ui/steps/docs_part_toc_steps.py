"""BDD steps for docs part TOC validation using a page object."""
from __future__ import annotations

import pytest
from playwright.sync_api import Page
from pytest_bdd import given, parsers, scenarios, then

from config.settings import settings
from pages.DocsPartTocPage import DocsPartTocPage

scenarios("ui/docs_part_toc.feature")


@pytest.fixture
def docs_part_toc_page(page: Page) -> DocsPartTocPage:
    return DocsPartTocPage(page=page, base_url=settings.UI_BASE_URL)


@given(parsers.parse('I open the docs part page path "{path}"'))
def step_open_docs_part_path(docs_part_toc_page: DocsPartTocPage, path: str) -> None:
    docs_part_toc_page.open_path(path)


@then("the docs part page request should be successful")
def step_docs_part_response_ok(docs_part_toc_page: DocsPartTocPage) -> None:
    docs_part_toc_page.assert_last_request_successful()


@then("all table of contents links should resolve with relevant text")
def step_validate_toc_links(docs_part_toc_page: DocsPartTocPage) -> None:
    docs_part_toc_page.validate_toc_links_with_relevant_text()

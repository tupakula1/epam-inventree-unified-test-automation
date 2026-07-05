"""
Root conftest.py — shared fixtures for the entire test suite.

Fixtures here are available to both UI (Playwright/BDD) and API tests.
"""
from __future__ import annotations

import logging
import base64
from urllib.parse import urlsplit
from typing import Generator

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from api.endpoints.CategoryAPI import CategoryAPI
from api.endpoints.PartsAPI import PartsAPI
from config.settings import settings

# ─── Logger ───────────────────────────────────────────────────────────────────
logger = logging.getLogger(__name__)

# ─── Config helpers ───────────────────────────────────────────────────────────
UI_BASE_URL: str = settings.UI_BASE_URL
API_BASE_URL: str = settings.API_BASE_URL
USERNAME: str = settings.USERNAME
PASSWORD: str = settings.PASSWORD
HEADLESS: bool = settings.HEADLESS
SLOW_MO: int = settings.SLOW_MO
BROWSER_TYPE: str = settings.BROWSER


def _api_service_root(api_base_url: str) -> str:
    parts = urlsplit(api_base_url)
    if parts.scheme and parts.netloc:
        return f"{parts.scheme}://{parts.netloc}"
    return api_base_url


API_SERVICE_ROOT: str = _api_service_root(API_BASE_URL)


def _is_docs_ui_environment() -> bool:
    base = UI_BASE_URL.lower()
    return "docs.inventree.org" in base


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """When UI points to docs, run only UI tests explicitly marked for docs mode."""
    if not _is_docs_ui_environment():
        return

    skip_docs_only = pytest.mark.skip(
        reason=(
            "Current UI_BASE_URL/API_BASE_URL points to docs.inventree.org. "
            "Only tests marked with @pytest.mark.docs are runnable in docs mode."
        )
    )
    for item in items:
        item_path = str(item.fspath).replace("\\", "/")
        is_ui_test = "/tests/ui/" in item_path
        if is_ui_test and "docs" not in item.keywords:
            item.add_marker(skip_docs_only)


def _get_pytest_option(request: pytest.FixtureRequest, option_name: str, default: object) -> object:
    """Safely read a pytest CLI option if available; otherwise return fallback."""
    try:
        value = request.config.getoption(option_name)
    except Exception:
        return default
    if value is None:
        return default
    if isinstance(value, str) and value.strip() == "":
        return default
    return value


# ─── Session-scoped Playwright instance ───────────────────────────────────────
@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    with sync_playwright() as pw:
        yield pw


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright, request: pytest.FixtureRequest) -> Generator[Browser, None, None]:
    browser_type = _get_pytest_option(request, "--browser", BROWSER_TYPE)
    if isinstance(browser_type, list):
        browser_type = browser_type[0] if browser_type else BROWSER_TYPE
    headed = bool(_get_pytest_option(request, "--headed", not HEADLESS))

    launcher = getattr(playwright_instance, browser_type)
    b = launcher.launch(headless=not headed, slow_mo=SLOW_MO)
    logger.info("Launched %s browser (headless=%s)", browser_type, not headed)
    yield b
    b.close()


# ─── Function-scoped context & page ───────────────────────────────────────────
@pytest.fixture
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    ctx = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        record_video_dir=None,
        ignore_https_errors=True,
    )
    ctx.set_default_timeout(settings.DEFAULT_TIMEOUT)
    ctx.set_default_navigation_timeout(settings.NAVIGATION_TIMEOUT)
    yield ctx
    ctx.close()


@pytest.fixture
def page(context: BrowserContext) -> Generator[Page, None, None]:
    p = context.new_page()
    yield p
    p.close()


# ─── API token fixture ────────────────────────────────────────────────────────
@pytest.fixture(scope="session")
def api_token(playwright_instance: Playwright) -> str:
    """Fetch and cache an API token for the session via Playwright API context."""
    auth_pair = f"{USERNAME}:{PASSWORD}".encode("ascii")
    basic_auth = base64.b64encode(auth_pair).decode("ascii")
    api_context = playwright_instance.request.new_context(
        extra_http_headers={
            "Authorization": f"Basic {basic_auth}",
            "Accept": "application/json",
        }
    )
    response = api_context.get(f"{API_BASE_URL}/user/token/")
    assert response.status == 200, f"Token request failed: {response.text()}"
    token = response.json()["token"]
    api_context.dispose()
    logger.info("API token acquired for session")
    return token


@pytest.fixture(scope="session")
def api_headers(api_token: str) -> dict[str, str]:
    return {
        "Authorization": f"Token {api_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


@pytest.fixture(scope="session")
def parts_api(api_token: str) -> PartsAPI:
    return PartsAPI(base_url=API_SERVICE_ROOT, token=api_token)


@pytest.fixture(scope="session")
def category_api(api_token: str) -> CategoryAPI:
    return CategoryAPI(base_url=API_SERVICE_ROOT, token=api_token)

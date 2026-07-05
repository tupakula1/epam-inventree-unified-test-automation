"""Validate docs locator classes via a shared page-object helper."""
from __future__ import annotations

import pytest

from locators import (
    DocsPartCreateLocators,
    DocsPartLocators,
    DocsPartNotificationLocators,
    DocsPartPricingLocators,
    DocsPartRevisionLocators,
    DocsPartStocktakeLocators,
    DocsPartTemplateLocators,
    DocsPartTestLocators,
    DocsPartTrackableLocators,
    DocsPartViewsLocators,
    DocsPartVirtualLocators,
)
from pages.DocsLocatorValidationPage import DocsLocatorValidationPage


@pytest.mark.ui
@pytest.mark.docs
@pytest.mark.parametrize(
    "locator_class",
    [
        DocsPartLocators,
        DocsPartCreateLocators,
        DocsPartVirtualLocators,
        DocsPartViewsLocators,
        DocsPartTrackableLocators,
        DocsPartRevisionLocators,
        DocsPartTemplateLocators,
        DocsPartTestLocators,
        DocsPartPricingLocators,
        DocsPartStocktakeLocators,
        DocsPartNotificationLocators,
    ],
)
def test_validate_docs_locator_class(page, locator_class) -> None:
    validator = DocsLocatorValidationPage(page)
    validator.validate_all(locator_class)

"""
locators/__init__.py — make locators importable as a package.
"""
from __future__ import annotations


def _optional_locator_import(module_name: str, class_name: str):
	"""Best-effort import for optional locator modules.

	Some test subsets (for example docs-only suites) should run even when
	legacy UI locator modules are not present in the workspace.
	"""
	try:
		module = __import__(f"locators.{module_name}", fromlist=[class_name])
		return getattr(module, class_name)
	except Exception:
		return None


LoginLocators = _optional_locator_import("LoginLocators", "LoginLocators")
PartLocators = _optional_locator_import("PartLocators", "PartLocators")
CategoryLocators = _optional_locator_import("CategoryLocators", "CategoryLocators")
StockLocators = _optional_locator_import("StockLocators", "StockLocators")
from locators.DocsPartLocators import DocsPartLocators
from locators.DocsPartCreateLocators import DocsPartCreateLocators
from locators.DocsPartVirtualLocators import DocsPartVirtualLocators
from locators.DocsPartViewsLocators import DocsPartViewsLocators
from locators.DocsPartTrackableLocators import DocsPartTrackableLocators
from locators.DocsPartRevisionLocators import DocsPartRevisionLocators
from locators.DocsPartTemplateLocators import DocsPartTemplateLocators
from locators.DocsPartTestLocators import DocsPartTestLocators
from locators.DocsPartPricingLocators import DocsPartPricingLocators
from locators.DocsPartStocktakeLocators import DocsPartStocktakeLocators
from locators.DocsPartNotificationLocators import DocsPartNotificationLocators

__all__ = [
	"DocsPartLocators",
	"DocsPartCreateLocators",
	"DocsPartVirtualLocators",
	"DocsPartViewsLocators",
	"DocsPartTrackableLocators",
	"DocsPartRevisionLocators",
	"DocsPartTemplateLocators",
	"DocsPartTestLocators",
	"DocsPartPricingLocators",
	"DocsPartStocktakeLocators",
	"DocsPartNotificationLocators",
]

if LoginLocators is not None:
	__all__.append("LoginLocators")
if PartLocators is not None:
	__all__.append("PartLocators")
if CategoryLocators is not None:
	__all__.append("CategoryLocators")
if StockLocators is not None:
	__all__.append("StockLocators")

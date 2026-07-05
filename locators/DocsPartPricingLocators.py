"""Locators for https://docs.inventree.org/en/stable/part/pricing/."""


class DocsPartPricingLocators:
    URL = "https://docs.inventree.org/en/stable/part/pricing/"

    HEADER = "header, .md-header"
    PRIMARY_NAV = ".md-nav--primary, nav[aria-label='Navigation']"
    TOC_NAV = "nav[aria-label='Table of contents'], .md-sidebar--secondary, nav.toc"
    SEARCH_INPUT = "input[data-md-component='search-query'], input[type='search']"
    MAIN_CONTENT = "main, article, [role='main']"
    BREADCRUMBS = "nav[aria-label='Breadcrumb'], .breadcrumb, .md-path"
    PAGE_H1 = "main h1, article h1, h1"
    TOC_LINKS = "nav[aria-label='Table of contents'] a[href], .md-sidebar--secondary a[href], nav.toc a[href]"

    SECTION_IDS = (
        "part-pricing",
        "override-pricing",
        "sale-pricing",
        "pricing-tab",
        "pricing-overview",
        "Pricing_Overview",
        "overall-pricing",
        "internal-pricing",
        "Internal_Pricing",
        "pricing-override",
        "purchase-history",
        "Purchase_History",
        "supplier-pricing",
        "Supplier_Pricing",
        "bom-pricing",
        "BOM_Pricing",
        "bom-pricing-chart",
        "variant-pricing",
        "sale-pricing_1",
        "Sale_Pricing",
        "sale-history",
        "Sale_History",
        "price-data-caching",
        "pricing-updates",
        "response-to-data-changes",
        "periodic-updates",
        "manual-updates",
        "disable-automatic-updates",
    )

    SECTION_ANCHORS = {sid: f"#{sid}" for sid in SECTION_IDS}
    TOC_LINKS_BY_SECTION = {
        sid: (
            "nav[aria-label='Table of contents'] a[href$='#{sid}'], "
            ".md-sidebar--secondary a[href$='#{sid}'], "
            "nav.toc a[href$='#{sid}']"
        ).format(sid=sid)
        for sid in SECTION_IDS
    }

"""Locators for https://docs.inventree.org/en/stable/part/."""


class DocsPartLocators:
    URL = "https://docs.inventree.org/en/stable/part/"

    HEADER = "header, .md-header"
    PRIMARY_NAV = ".md-nav--primary, nav[aria-label='Navigation']"
    TOC_NAV = "nav[aria-label='Table of contents'], .md-sidebar--secondary, nav.toc"
    SEARCH_INPUT = "input[data-md-component='search-query'], input[type='search']"
    MAIN_CONTENT = "main, article, [role='main']"
    BREADCRUMBS = "nav[aria-label='Breadcrumb'], .breadcrumb, .md-path"
    PAGE_H1 = "main h1, article h1, h1"
    TOC_LINKS = "nav[aria-label='Table of contents'] a[href], .md-sidebar--secondary a[href], nav.toc a[href]"

    SECTION_IDS = (
        "part",
        "part-stock",
        "minimum-stock",
        "maximum-stock",
        "part-category",
        "Part_category",
        "part-attributes",
        "virtual",
        "template",
        "assembly",
        "component",
        "testable",
        "trackable",
        "purchaseable",
        "suppliers",
        "supplier-parts",
        "purchase-orders",
        "salable",
        "locked-parts",
        "active-parts",
        "units-of-measure",
        "physical-units",
        "Part_units",
        "supplier-part-units",
        "Invalid_supplier_part_units",
        "part-images",
        "Part_image_example",
        "image-thumbnails",
        "uploading-part-image",
        "web-interface",
        "Part_image_upload",
        "api",
        "mobile-app",
        "part-import",
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

"""Locators for https://docs.inventree.org/en/stable/part/test/."""


class DocsPartTestLocators:
    URL = "https://docs.inventree.org/en/stable/part/test/"

    HEADER = "header, .md-header"
    PRIMARY_NAV = ".md-nav--primary, nav[aria-label='Navigation']"
    TOC_NAV = "nav[aria-label='Table of contents'], .md-sidebar--secondary, nav.toc"
    SEARCH_INPUT = "input[data-md-component='search-query'], input[type='search']"
    MAIN_CONTENT = "main, article, [role='main']"
    BREADCRUMBS = "nav[aria-label='Breadcrumb'], .breadcrumb, .md-path"
    PAGE_H1 = "main h1, article h1, h1"
    TOC_LINKS = "nav[aria-label='Table of contents'] a[href], .md-sidebar--secondary a[href], nav.toc a[href]"

    SECTION_IDS = (
        "part-test-templates",
        "Part_Test_Templates",
        "test-template-parameters",
        "test-name",
        "test-key",
        "examples",
        "test-description",
        "required",
        "requires-value",
        "requires-attachment",
        "enabled",
        "test-results",
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

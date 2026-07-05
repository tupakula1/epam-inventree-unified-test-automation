"""Locators for https://docs.inventree.org/en/stable/part/revision/."""


class DocsPartRevisionLocators:
    URL = "https://docs.inventree.org/en/stable/part/revision/"

    HEADER = "header, .md-header"
    PRIMARY_NAV = ".md-nav--primary, nav[aria-label='Navigation']"
    TOC_NAV = "nav[aria-label='Table of contents'], .md-sidebar--secondary, nav.toc"
    SEARCH_INPUT = "input[data-md-component='search-query'], input[type='search']"
    MAIN_CONTENT = "main, article, [role='main']"
    BREADCRUMBS = "nav[aria-label='Breadcrumb'], .breadcrumb, .md-path"
    PAGE_H1 = "main h1, article h1, h1"
    TOC_LINKS = "nav[aria-label='Table of contents'] a[href], .md-sidebar--secondary a[href], nav.toc a[href]"

    SECTION_IDS = (
        "part-revisions",
        "revisions-are-parts",
        "revision-fields",
        "revision-restrictions",
        "revision-settings",
        "create-a-revision",
        "Create_part_revision",
        "Part_revision_B",
        "revision-navigation",
        "Select_part_revision",
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

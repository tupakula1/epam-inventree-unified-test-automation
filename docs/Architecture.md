# Architecture — EPAM InvenTree Unified Test Automation Framework

## 1. Overview

This framework is a **unified, BDD-driven test automation solution** targeting the InvenTree Parts module. It is designed to demonstrate Principal Test Architect-level thinking: AI-assisted requirements analysis, enterprise project structure, layered architecture, and CI/CD integration.

---

## 2. Technology Stack

| Concern | Technology |
|---|---|
| Language | Python 3.12+ |
| UI Automation | Playwright (Python) |
| BDD Layer | pytest-bdd |
| Test Runner | pytest |
| API Automation | Playwright API / requests |
| Data Validation | Pydantic v2 |
| Reporting | pytest-html + Allure |
| CI/CD | GitHub Actions |
| Application | InvenTree (Docker) |

---

## 3. Architectural Layers

```
┌─────────────────────────────────────────┐
│           Feature Files (BDD)           │  features/ui/  features/api/
├─────────────────────────────────────────┤
│         Step Definitions                │  tests/ui/steps/  tests/api/steps/
├─────────────────────────────────────────┤
│         Page Object Model               │  pages/
├─────────────────────────────────────────┤
│         Locator Registry                │  locators/
├─────────────────────────────────────────┤
│         API Client Layer                │  api/clients/
├─────────────────────────────────────────┤
│         API Endpoint Wrappers           │  api/endpoints/
├─────────────────────────────────────────┤
│         Data Models (Pydantic)          │  api/models/
├─────────────────────────────────────────┤
│         Test Data & Payloads            │  testdata/  api/payloads/
├─────────────────────────────────────────┤
│         Utilities                       │  utilities/
├─────────────────────────────────────────┤
│         Configuration                   │  config/  .env  pytest.ini
└─────────────────────────────────────────┘
```

---

## 4. Project Structure

```
epam-inventree-unified-test-automation/
│
├── README.md                        # Setup, usage, approach summary
├── requirements.txt                 # Python dependencies
├── pytest.ini                       # pytest / BDD configuration
├── playwright.config.py             # Playwright settings
├── conftest.py                      # Root fixtures (browser, page, API token)
├── .env                             # Local environment variables (not committed)
├── .gitignore
│
├── docs/
│   ├── Architecture.md              ← this file
│   ├── AI-Prompts.md                # All Copilot prompts used
│   ├── TestStrategy.md              # Test strategy document
│   ├── SolutionApproach.md          # Approach narrative for EPAM reviewers
│   └── RequirementAnalysis.md       # AI-generated requirement analysis
│
├── features/
│   └── ui/
│       ├── part_creation.feature
│       ├── part_update.feature
│       ├── part_category.feature
│       ├── part_attributes.feature
│       ├── part_revision.feature
│       ├── part_parameters.feature
│       ├── part_bom.feature
│       └── stock.feature
│
├── pages/                           # Page Object Model
│   ├── BasePage.py
│   ├── LoginPage.py
│   ├── DashboardPage.py
│   ├── PartsPage.py
│   ├── PartDetailPage.py
│   ├── CategoryPage.py
│   └── StockPage.py
│
├── locators/                        # Centralised CSS/ARIA selectors
│   ├── LoginLocators.py
│   ├── PartLocators.py
│   ├── CategoryLocators.py
│   └── StockLocators.py
│
├── api/
│   ├── clients/
│   │   └── BaseClient.py            # Shared requests session + auth
│   ├── endpoints/
│   │   ├── PartsAPI.py
│   │   └── CategoryAPI.py
│   ├── models/                      # Pydantic response models
│   │   ├── PartModel.py
│   │   └── CategoryModel.py
│   └── payloads/                    # Request payload builders
│       ├── part_payloads.py
│       └── category_payloads.py
│
├── tests/
│   ├── ui/
│   │   ├── conftest.py              # UI-specific fixtures
│   │   └── steps/                  # BDD step implementations
│   │       ├── part_creation_steps.py
│   │       ├── part_update_steps.py
│   │       ├── part_category_steps.py
│   │       └── part_revision_steps.py
│   └── api/
│       ├── conftest.py              # API-specific fixtures
│       ├── test_parts_crud.py
│       ├── test_parts_filter.py
│       ├── test_parts_validation.py
│       ├── test_category_crud.py
│       └── test_parts_edge_cases.py
│
├── utilities/
│   ├── logger.py
│   ├── data_generator.py
│   ├── screenshot_helper.py
│   └── retry_helper.py
│
├── config/
│   ├── settings.py
│   └── environments.yml
│
├── testdata/
│   ├── parts.json
│   ├── categories.json
│   └── invalid_payloads.json
│
├── reports/                         # Generated (git-ignored)
├── screenshots/                     # Generated (git-ignored)
├── logs/                            # Generated (git-ignored)
│
└── .github/
    └── workflows/
        └── regression.yml
```

---

## 5. Design Principles

| Principle | Implementation |
|---|---|
| Single Responsibility | Each layer has one job: locators, pages, steps, clients |
| DRY | Base classes (`BasePage`, `BaseClient`) hold all shared logic |
| Open/Closed | New modules added without changing existing ones |
| Separation of Concerns | UI steps never talk directly to the HTTP layer |
| Data-Driven | Payloads and test data live in JSON/YAML, not in test code |
| BDD as Contract | Feature files are written in business language, readable by stakeholders |

---

## 6. Test Execution Flow

```
pytest
  └─► conftest.py (load .env, create browser, acquire API token)
        └─► BDD feature file parsed by pytest-bdd
              └─► Step definitions call Page Objects / API Clients
                    └─► Assertions on UI state / HTTP response
                          └─► Reports generated (HTML + Allure)
```

---

## 7. Reporting Strategy

- **pytest-html** — self-contained HTML report at `reports/report.html`
- **Allure** — rich dashboard with steps, screenshots, traces
- **Screenshots** — captured on every failure, stored in `screenshots/`
- **Playwright Traces** — retained on failure for debugging
- **Logs** — structured logs at `logs/test_run.log`

<<<<<<< HEAD
# EPAM InvenTree Unified Test Automation Framework

AI-assisted test automation framework for the InvenTree Parts domain, combining API BDD and UI docs validation with pytest, Playwright, and Allure.

## Stack

| Concern | Technology |
|---|---|
| Language | Python 3.12 |
| Test Runner | pytest |
| BDD | pytest-bdd |
| UI Automation | Playwright (sync API) |
| API | requests + Playwright APIRequestContext |
| Data Validation | Pydantic v2 |
| Reporting | pytest-html + Allure |
| Config | python-dotenv + YAML profiles |

## Current Framework Layout

```
.
├── conftest.py
├── pytest.ini
├── playwright.config.py
├── requirements.txt
├── config/
│   ├── settings.py
│   └── environments.yml
├── api/
│   ├── clients/
│   ├── endpoints/
│   └── payloads/
├── features/
│   ├── api/
│   │   ├── category_api.feature
│   │   ├── docs_api.feature
│   │   ├── parts_api.feature
│   │   ├── parts_edge_cases_api.feature
│   │   ├── parts_filter_api.feature
│   │   └── parts_validation_api.feature
│   └── ui/
│       └── docs_part_toc.feature
├── tests/
│   ├── api/
│   │   ├── test_api_scenarios.py
│   │   ├── steps/
│   │   └── _legacy/            # not collected by default (pytest.ini: norecursedirs)
│   └── ui/
│       ├── test_ui_docs_bdd.py
│       ├── test_ui_docs_locators_page_object.py
│       └── steps/
├── locators/
│   ├── DocsPartLocators.py
│   ├── DocsPartCreateLocators.py
│   ├── DocsPartVirtualLocators.py
│   ├── DocsPartViewsLocators.py
│   ├── DocsPartTrackableLocators.py
│   ├── DocsPartRevisionLocators.py
│   ├── DocsPartTemplateLocators.py
│   ├── DocsPartTestLocators.py
│   ├── DocsPartPricingLocators.py
│   ├── DocsPartStocktakeLocators.py
│   └── DocsPartNotificationLocators.py
├── pages/
├── utilities/
├── testdata/
└── reports/
```

## Environment Model

Configuration is loaded from:

1. `.env` values (highest priority)
2. `config/environments.yml` by `ENV` profile
3. defaults in `config/settings.py`

Key runtime settings used by the suite:

- `ENV` (profile: `local`, `demo`, `staging`, `docs`)
- `UI_BASE_URL`
- `API_BASE_URL`
- `DOCS_UI_URL`
- `DOCS_API_URL`
- `INVENTREE_USERNAME`
- `INVENTREE_PASSWORD`
- `HEADLESS`
- `BROWSER`

Sample `.env` for the current docs+demo setup:

```env
ENV=local
UI_BASE_URL=https://docs.inventree.org/en/stable/part/
API_BASE_URL=https://demo.inventree.org/api
DOCS_UI_URL=https://docs.inventree.org/en/stable/part/
DOCS_API_URL=https://docs.inventree.org/en/stable/api/schema/part/
INVENTREE_USERNAME=admin
INVENTREE_PASSWORD=inventree
HEADLESS=true
BROWSER=chromium
```

Note: when `UI_BASE_URL` points to docs, the root collection hook runs only UI tests marked `docs`.

## Setup

### 1. Prerequisites

- Python 3.12+
- Java (required by Allure CLI)
- Allure CLI installed and available in PATH

Optional:

- Docker Desktop (only if you want to run against your own InvenTree instance)

### 2. Install dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
```

### 3. Validate toolchain

```powershell
python -m pytest --version
allure --version
```

## Test Execution

Use `python -m pytest` (recommended for Windows and venv reliability).

### API BDD scenarios

```powershell
python -m pytest .\tests\api\test_api_scenarios.py -v
```

### UI docs BDD scenarios

```powershell
python -m pytest .\tests\ui\test_ui_docs_bdd.py -v
```

### UI docs locator page-object validation

```powershell
python -m pytest .\tests\ui\test_ui_docs_locators_page_object.py -v
```

### Run all collected tests

```powershell
python -m pytest .\tests -v
```

## Reporting

### Built-in pytest HTML

Every run generates:

- `reports/report.html`

### Allure reports (API + UI)

1. Execute suites and capture separate results:

```powershell
python -m pytest .\tests\api --alluredir=reports/allure-api --clean-alluredir
python -m pytest .\tests\ui --alluredir=reports/allure-ui --clean-alluredir
```

2. Merge and generate combined report:

```powershell
New-Item -ItemType Directory -Force -Path reports/allure-results | Out-Null
Copy-Item reports/allure-api\* reports/allure-results\ -Force
Copy-Item reports/allure-ui\* reports/allure-results\ -Force
allure generate reports/allure-results -o reports/allure-report --clean
```

3. Open report:

```powershell
allure open reports/allure-report
```

## Markers

Defined in `pytest.ini`:

- `ui`, `api`, `docs`
- `smoke`, `regression`
- `positive`, `negative`, `boundary`
- `crud`, `part`, `category`
- `bdd`, `legacy_non_bdd`
- `stock`, `revision`, `bom`, `parameters`, `import`, `cross_functional`, `slow`

## Notes

- `tests/api/_legacy` exists for archived non-BDD tests and is excluded from collection.
- UI docs validations can be sensitive to upstream docs DOM changes; rerun failing docs-locator tests to confirm transient failures before code changes.

## Documentation

| Document | Description |
|---|---|
| [docs/Architecture.md](docs/Architecture.md) | Framework architecture and layering |
| [docs/TestStrategy.md](docs/TestStrategy.md) | Scope, risk coverage, and approach |
| [docs/AI-Prompts.md](docs/AI-Prompts.md) | Prompts used during AI-assisted implementation |
| [docs/SolutionApproach.md](docs/SolutionApproach.md) | End-to-end solution narrative |
=======
Epam InvenTree unified test automation framework
>>>>>>> 7a313fd6da5432c20317af0f546aa3ac9a2f28e8

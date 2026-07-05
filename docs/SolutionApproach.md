# Solution Approach — EPAM Quality Architect Assessment

## 1. Executive Summary

This submission demonstrates a **Principal Test Architect's approach** to building an AI-assisted, enterprise-grade test automation framework for the InvenTree Parts module. Rather than producing tests manually, every artefact was generated through a structured, agent-directed workflow using **GitHub Copilot** inside VS Code.

The result is a unified framework that covers UI automation (Playwright + pytest-bdd), API automation (requests + Playwright API), manual test cases, and CI/CD integration — all organized under a layered, maintainable architecture.

---

## 2. AI-Assisted Workflow

```
Requirements Analysis (Copilot Chat)
          ↓
Structured Prompts → RequirementAnalysis.md
          ↓
Test Strategy (AI-assisted + architect review)
          ↓
Manual UI Test Cases → ui-manual-tests.md
          ↓
Manual API Test Cases → api-manual-tests.md
          ↓
Framework Skeleton (Copilot Chat + inline suggestions)
          ↓
Page Objects + Locators (Copilot Agent mode)
          ↓
API Client Layer (Copilot Agent mode)
          ↓
BDD Feature Files (Copilot Chat)
          ↓
Step Definitions (Copilot inline + review)
          ↓
CI/CD Workflow (Copilot)
          ↓
Documentation (Copilot + architect review)
```

---

## 3. Key Architectural Decisions

### 3.1 pytest-bdd over Behave
`pytest-bdd` was chosen because it integrates natively with `pytest`, meaning all existing fixtures, plugins (html reporting, xdist, rerunfailures), and conftest patterns work without adaptation. Behave requires a separate runner and cannot use pytest fixtures directly.

### 3.2 Playwright over Selenium
Playwright provides built-in API testing, network interception, auto-waiting, and Playwright Traces — dramatically reducing the amount of custom wait logic needed. Its Python SDK is production-quality and actively maintained.

### 3.3 Pydantic for API Response Validation
Rather than writing manual JSON key assertions, Pydantic models provide schema validation, type coercion, and field-level validation in a single declarative class. This catches schema regressions early and makes test intent clear.

### 3.4 Centralised Locator Registry
Selectors are defined once in `locators/` classes. Page Objects import them. Step definitions never contain selectors. This means a UI change requires updating only one file.

### 3.5 Session-scoped API Token
The `api_token` fixture runs once per test session, fetching a token via `/api/user/token/`. This avoids N login requests for N API tests and mirrors real-world performance considerations.

---

## 4. What the AI Agent Did vs. What the Architect Directed

| Task | AI Agent | Architect |
|---|---|---|
| Requirements analysis | Generated from docs URLs | Reviewed, structured prompts |
| Test case generation | Generated all test cases | Reviewed coverage, added boundary cases |
| Page Object code | Generated from prompts | Reviewed patterns, enforced conventions |
| API client code | Generated from prompts | Reviewed error handling, added retry logic |
| BDD feature files | Generated Gherkin | Reviewed business language, removed tech detail |
| Step definitions | Generated from feature files | Reviewed assertions, added teardown |
| CI/CD workflow | Generated YAML | Adjusted secrets handling and artifact retention |
| Documentation | Generated drafts | Reviewed, added architectural reasoning |

---

## 5. Framework Scalability

This framework is designed to scale to the full InvenTree system:

- **Adding a new module**: create a feature file, a Page Object, a locators file, an API client, and wire steps — the base classes handle everything else.
- **Adding a new environment**: add an entry to `config/environments.yml` and pass `--env` to pytest.
- **Parallel execution**: `pytest-xdist` is included; run with `-n auto` for parallel browser instances.
- **Data isolation**: each test generates unique data via Faker and cleans up via API teardown.

---

## 6. Assumptions and Constraints

- InvenTree is reachable at `https://demo.inventree.org`
- Admin credentials are `admin` / `inventree` (configurable via `.env`)
- Tests are designed against InvenTree stable branch API
- Network interception is not required for current scope

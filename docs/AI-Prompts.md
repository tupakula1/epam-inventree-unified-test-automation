# AI Prompts — GitHub Copilot Agent Instructions

This file documents all prompts used to guide **GitHub Copilot** throughout this assessment. It serves as the "Agent Artefacts" deliverable required by the EPAM assessment rubric.

---

## System Instruction (used in Copilot Chat context)

```
You are a Principal Test Architect with 17+ years of experience in enterprise QA.
You are helping build a unified test automation framework for InvenTree — an open-source
inventory management system built with Python/Django.

Technology stack:
- Language: Python 3.12+
- UI Automation: Playwright (Python)
- BDD: pytest-bdd
- API Testing: Playwright API / requests
- Validation: Pydantic v2
- Reporting: pytest-html + Allure

Always follow these principles:
1. Page Object Model for all UI interactions
2. Centralised locator registries — never embed selectors in test steps
3. Shared base classes (BasePage, BaseClient)
4. Data-driven tests — test data in JSON/YAML, not hardcoded
5. Clean BDD Gherkin — business language, no technical detail in feature files
6. Pydantic models for API response validation
7. Proper teardown and cleanup after each test

Output production-quality, runnable Python code.
```

---

## Phase 1 — Requirements Analysis

### Prompt 1.1 — Ingest Parts Documentation
```
You are a Principal Test Architect.

I am providing you with the InvenTree Parts module documentation from:
https://docs.inventree.org/en/stable/part/

Analyze the documentation and generate a structured requirements analysis covering:

1. Business Requirements
2. Functional Requirements (grouped by feature area)
3. Non-Functional Requirements
4. Business Rules (especially validation and constraint rules)
5. Edge Cases and Boundary Conditions
6. Negative Scenarios
7. Dependencies between features
8. Assumptions
9. Risks

Format the output as a professional Markdown document suitable for a test strategy artefact.
```

### Prompt 1.2 — API Schema Analysis
```
Analyze the InvenTree API schema from:
https://docs.inventree.org/en/stable/api/schema/part/

For each endpoint, extract:
- HTTP method and path
- Required fields
- Optional fields
- Field types, max lengths, and nullable constraints
- Read-only fields
- Response schema
- Error responses

Output as a structured Markdown table per endpoint.
```

---

## Phase 2 — Manual Test Case Generation

### Prompt 2.1 — UI Manual Test Cases
```
Using the requirements analysis of the InvenTree Parts module, generate comprehensive
UI manual test cases.

For each test case, provide these columns:
| Test ID | Feature | Scenario | Preconditions | Priority | Risk | Steps | Expected Result | Test Data | Tags |

Coverage must include:
- Part creation (manual entry + import)
- Part detail view — all tabs (Stock, BOM, Parameters, Variants, Revisions, Attachments)
- Part categories (hierarchy, filtering)
- Part attributes (Virtual, Template, Assembly, Component, Trackable, Purchaseable, Salable)
- Part parameters with units
- Part revisions (creation + constraint enforcement)
- Negative scenarios (duplicate IPN, inactive part, revision-of-revision)
- Boundary scenarios

Output as Markdown.
```

### Prompt 2.2 — API Manual Test Cases
```
Generate comprehensive API manual test cases for the InvenTree Parts API.

Columns: Test ID | Endpoint | Method | Scenario | Request Body | Expected Status | Expected Response | Tags

Coverage must include:
- CRUD on /api/part/ and /api/part/category/
- Filtering, pagination, search
- Field-level validation (required, max length, nullable, read-only)
- Relational integrity (category, default location, supplier)
- Edge cases (invalid payload, unauthorised, conflict)

Output as Markdown.
```

---

## Phase 3 — Automation Code Generation

### Prompt 3.1 — Base Page Object
```
Generate a BasePage class for Playwright (Python) with:
- Constructor accepting page: Page and base_url: str
- navigate(path) method
- wait_for_element(locator) method
- click(locator) method
- fill(locator, value) method
- get_text(locator) method
- is_visible(locator) method
- take_screenshot(name) method
- wait_for_toast(message) method

Use type hints. Include logging. No hardcoded selectors.
```

### Prompt 3.2 — Parts Page Object
```
Generate a PartsPage class extending BasePage for InvenTree UI.

It should cover:
- navigate_to_parts()
- click_create_part()
- fill_part_form(name, ipn, description, category) 
- submit_part_form()
- search_part(query)
- open_part_by_name(name)
- verify_part_visible(name)
- delete_part(name)

Use the centralised PartLocators class for all selectors.
Implement robust waits. Use type hints.
```

### Prompt 3.3 — API BaseClient
```
Generate a BaseClient class using the requests library for InvenTree API testing.

Include:
- Constructor accepting base_url and token
- _get(endpoint, params) method
- _post(endpoint, payload) method
- _patch(endpoint, payload) method
- _delete(endpoint) method
- Response validation helper: assert_status(response, expected_status)
- Response logging (request + response body)
- Session-level connection reuse

Use type hints. Return requests.Response objects.
```

### Prompt 3.4 — Parts API Endpoint Wrapper
```
Generate a PartsAPI class extending BaseClient.

Methods:
- list_parts(filters: dict) -> Response
- get_part(part_id: int) -> Response  
- create_part(payload: dict) -> Response
- update_part(part_id: int, payload: dict) -> Response
- delete_part(part_id: int) -> Response
- search_parts(query: str) -> Response

Add Pydantic model validation on successful responses.
```

### Prompt 3.5 — BDD Feature File (Part Creation)
```
Write a pytest-bdd Gherkin feature file for InvenTree Part Creation.

Cover these scenarios:
1. Successfully create a new part with all required fields
2. Successfully create a part with all optional fields
3. Fail to create a part with a duplicate IPN
4. Fail to create a part with missing required name
5. Create a part as a Template part
6. Create a part as a Virtual part
7. Create a part assigned to a category

Use Background for login. Use Scenario Outline + Examples for data-driven cases.
Use tags: @smoke, @regression, @positive, @negative.
Business language only — no technical selectors in the feature file.
```

### Prompt 3.6 — Step Definitions
```
Generate pytest-bdd step definitions for the Part Creation feature file.

- Import and use PartsPage and PartLocators
- Each step must have a clear docstring
- Use the authenticated_page fixture from conftest.py
- Implement proper assertions using pytest assert
- Add logging to each step
- Include data cleanup (delete created part) in a teardown fixture
```

---

## Phase 4 — Cross-Functional Flow

### Prompt 4.1
```
Generate a pytest-bdd feature file for a cross-functional flow:
Create a Part → Add a Parameter → Create Stock → Verify in Category View

This should be a single Scenario with multiple When/Then steps.
Tag it @smoke @cross_functional.
Generate the corresponding step definitions using Page Objects and API client.
```

---

## Phase 5 — CI/CD

### Prompt 5.1
```
Generate a GitHub Actions workflow file (regression.yml) that:
1. Triggers on push to main and on pull requests
2. Uses ubuntu-latest
3. Sets up Python 3.12
4. Installs requirements.txt
5. Installs Playwright browsers
6. Runs pytest with --html report and Allure results
7. Uploads HTML report and screenshots as artifacts
8. Uses GitHub secrets for INVENTREE_USERNAME and INVENTREE_PASSWORD
```

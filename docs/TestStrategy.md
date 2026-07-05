# Test Strategy — InvenTree Parts Module

## 1. Purpose

This document defines the quality strategy for automated testing of the **InvenTree Parts module** as part of the EPAM Quality Architect Assessment. It covers scope, risk analysis, test levels, entry/exit criteria, and tool choices.

---

## 2. Scope

### In Scope
- Parts module: creation, update, delete, list, search
- Part categories: hierarchy, filtering, parametric tables
- Part attributes: Virtual, Template, Assembly, Component, Trackable, Purchaseable, Salable, Active/Inactive
- Part parameters: create, assign, validate units
- Part revisions: create, constraint enforcement
- Part BOM: add/remove items
- Part stock: create stock entries
- API endpoints under `/api/part/` and `/api/part/category/`

### Out of Scope
- Purchase orders
- Sales orders
- Manufacturing (Build) orders (tested only as cross-functional link)
- User management & permissions
- Plugin system

---

## 3. Risk-Based Priority

| Area | Risk | Priority |
|---|---|---|
| Part creation (required fields) | High — core CRUD | P1 |
| Part IPN uniqueness validation | High — data integrity | P1 |
| Part revision circular reference prevention | High — data integrity | P1 |
| Part attribute combinations (Template + Variant) | High — business logic | P1 |
| Category hierarchy | Medium | P2 |
| Part parameters & units | Medium | P2 |
| BOM management | Medium | P2 |
| Inactive part restrictions | Medium | P2 |
| Pagination & filtering | Low | P3 |
| Attachment upload | Low | P3 |

---

## 4. Test Levels

| Level | Framework | Location |
|---|---|---|
| API Integration | pytest + requests/Playwright API + pytest-bdd | `tests/api/`, `features/api/` |
| UI Functional (BDD) | pytest-bdd + Playwright | `tests/ui/` |
| Cross-functional Flow | pytest-bdd + Playwright | `features/ui/` |

---

## 5. Test Types

- **Positive tests** — valid inputs, expected success
- **Negative tests** — invalid inputs, expected error responses
- **Boundary tests** — max/min lengths, edge numeric values
- **Constraint tests** — business rule enforcement (IPN uniqueness, revision rules)
- **Cross-functional tests** — multi-step flows spanning features

---

## 6. Entry Criteria

- InvenTree instance is running (Docker) and accessible at `BASE_URL`
- Admin credentials are valid
- All dependencies in `requirements.txt` are installed
- Playwright browsers are installed (`playwright install`)

---

## 7. Exit Criteria

- All P1 tests passing
- No open Critical or High defects
- Code coverage of API endpoints ≥ 80 % of documented paths
- HTML and Allure reports generated

---

## 8. Test Data Strategy

- **Unique data per run** — generated using `Faker` to avoid collisions
- **Cleanup** — API-based teardown after each test (DELETE endpoint)
- **Static reference data** — categories and templates loaded from `testdata/`
- **Parameterised** — boundary and negative tests driven from JSON files

---

## 9. Tool Selection Rationale

| Choice | Reason |
|---|---|
| Python | Dominant language in QA tooling; aligns with InvenTree backend |
| Playwright | First-class async support, network interception, API testing built-in |
| pytest-bdd | BDD without Behave overhead; native pytest integration |
| Pydantic | Schema validation for API responses with minimal boilerplate |
| Allure | Industry-standard reporting for enterprise delivery |
| GitHub Actions | Free, cloud-hosted CI/CD; zero infrastructure cost |

---

## 10. Defect Classification

| Severity | Description |
|---|---|
| Critical | Application crash, data corruption, security breach |
| High | Core business functionality broken |
| Medium | Feature works but behaviour is incorrect or inconsistent |
| Low | UI cosmetic issues, non-critical UX problems |

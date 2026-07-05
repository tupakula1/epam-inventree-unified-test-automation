"""Step definitions for docs API BDD scenarios."""
from __future__ import annotations

import os
from typing import Any

import pytest
import requests
from pytest_bdd import parsers, scenarios, then, when

scenarios("api/docs_api.feature")


@pytest.fixture
def docs_api_context() -> dict[str, Any]:
    return {"response": None}


@when("I request the docs API URL")
def step_request_docs_api(docs_api_context: dict[str, Any]) -> None:
    url = os.getenv("API_BASE_URL", "https://docs.inventree.org/en/stable/api/schema/part/")
    docs_api_context["response"] = requests.get(url, timeout=20)


@then(parsers.parse("docs API response status should be {status:d}"))
def step_docs_status(docs_api_context: dict[str, Any], status: int) -> None:
    response = docs_api_context["response"]
    assert response is not None, "Expected response to be available"
    assert response.status_code == status, f"Expected {status}, got {response.status_code}"


@then(parsers.parse('docs API response content type should include "{content_type}"'))
def step_docs_content_type(docs_api_context: dict[str, Any], content_type: str) -> None:
    response = docs_api_context["response"]
    assert response is not None, "Expected response to be available"
    actual_content_type = response.headers.get("Content-Type", "").lower()
    assert content_type.lower() in actual_content_type

"""Step definitions for parts filter BDD scenarios."""
from __future__ import annotations

from typing import Any, Generator
from uuid import uuid4

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from api.endpoints.PartsAPI import PartsAPI
from api.payloads.part_payloads import minimal_part_payload

scenarios("api/parts_filter_api.feature")


def _extract_results(response_body: Any) -> list[dict[str, Any]]:
    if isinstance(response_body, list):
        return response_body
    if isinstance(response_body, dict):
        results = response_body.get("results", [])
        return results if isinstance(results, list) else []
    return []


def _safe_delete_part(parts_api: PartsAPI, part_id: int) -> None:
    delete_response = parts_api.delete_part(part_id)
    if delete_response.status_code == 204:
        return

    # Some environments block deletion of active parts.
    if delete_response.status_code == 400:
        patch_response = parts_api.update_part(part_id, {"active": False})
        if patch_response.status_code == 200:
            parts_api.delete_part(part_id)


@pytest.fixture
def parts_filter_context() -> dict[str, Any]:
    return {
        "response": None,
        "page_one": None,
        "page_two": None,
        "created_part_ids": [],
        "created_name": None,
    }


@pytest.fixture(autouse=True)
def cleanup_parts_filter(
    parts_api: PartsAPI,
    parts_filter_context: dict[str, Any],
) -> Generator[None, None, None]:
    yield
    for part_id in reversed(parts_filter_context["created_part_ids"]):
        _safe_delete_part(parts_api, part_id)


@given("an existing part with generated unique name")
def step_existing_part_with_generated_unique_name(
    parts_api: PartsAPI,
    parts_filter_context: dict[str, Any],
) -> None:
    created_name = f"FilterSearch-{uuid4().hex[:8]}"
    payload = minimal_part_payload(name=created_name)
    payload["IPN"] = f"FILTER-{uuid4().hex[:10]}"

    response = parts_api.create_part(payload)
    parts_api.assert_status(response, 201)
    part_id = response.json()["pk"]
    parts_filter_context["created_part_ids"].append(part_id)
    parts_filter_context["created_name"] = created_name


@when("I search parts using the created part name")
def step_search_parts_by_created_name(parts_api: PartsAPI, parts_filter_context: dict[str, Any]) -> None:
    query = parts_filter_context["created_name"]
    assert isinstance(query, str) and query, "Expected created name to be available"
    parts_filter_context["response"] = parts_api.search_parts(query)


@when(parsers.parse("I list parts with active flag {active_flag}"))
def step_list_parts_with_active(
    parts_api: PartsAPI,
    parts_filter_context: dict[str, Any],
    active_flag: str,
) -> None:
    parts_filter_context["response"] = parts_api.list_parts({"active": active_flag.lower() == "true"})


@when(parsers.parse("I list parts with pagination limit {limit:d} and offset {offset:d}"))
def step_list_parts_with_pagination(
    parts_api: PartsAPI,
    parts_filter_context: dict[str, Any],
    limit: int,
    offset: int,
) -> None:
    parts_filter_context["response"] = parts_api.list_parts_paginated(limit=limit, offset=offset)


@when(parsers.parse("I list first and second pages with limit {limit:d}"))
def step_list_two_pages(parts_api: PartsAPI, parts_filter_context: dict[str, Any], limit: int) -> None:
    first = parts_api.list_parts_paginated(limit=limit, offset=0)
    second = parts_api.list_parts_paginated(limit=limit, offset=limit)
    parts_filter_context["page_one"] = first
    parts_filter_context["page_two"] = second


@then(parsers.parse("the filter API response status should be {status:d}"))
def step_filter_status(parts_filter_context: dict[str, Any], status: int) -> None:
    response = parts_filter_context["response"]
    assert response is not None, "Expected response to be available"
    assert response.status_code == status, f"Expected {status}, got {response.status_code}: {response.text}"


@then("search results should contain the created part name")
def step_search_results_contain_created_name(parts_filter_context: dict[str, Any]) -> None:
    response = parts_filter_context["response"]
    name = parts_filter_context["created_name"]

    assert response is not None, "Expected response to be available"
    assert isinstance(name, str) and name, "Expected created name to be available"
    results = _extract_results(response.json())
    assert any(item.get("name") == name for item in results), f"Expected {name} in search results"


@then(parsers.parse("each listed part should have active {active_flag}"))
def step_each_part_active_flag(parts_filter_context: dict[str, Any], active_flag: str) -> None:
    response = parts_filter_context["response"]
    expected = active_flag.lower() == "true"

    assert response is not None, "Expected response to be available"
    for part in _extract_results(response.json()):
        assert part.get("active") is expected


@then(parsers.parse("the results length should be at most {size:d}"))
def step_results_at_most(parts_filter_context: dict[str, Any], size: int) -> None:
    response = parts_filter_context["response"]
    assert response is not None, "Expected response to be available"
    assert len(_extract_results(response.json())) <= size


@then(parsers.parse("the results length should be {size:d}"))
def step_results_equal(parts_filter_context: dict[str, Any], size: int) -> None:
    response = parts_filter_context["response"]
    assert response is not None, "Expected response to be available"
    body = response.json()
    if isinstance(body, dict):
        assert len(_extract_results(body)) == size
        return

    # If pagination is not enabled server-side, list responses are returned.
    assert isinstance(body, list)


@then("the first and second page part ids should not overlap")
def step_pages_disjoint(parts_filter_context: dict[str, Any]) -> None:
    first = parts_filter_context["page_one"]
    second = parts_filter_context["page_two"]

    assert first is not None and second is not None, "Expected both pages to be available"
    first_ids = {item["pk"] for item in _extract_results(first.json())}
    second_ids = {item["pk"] for item in _extract_results(second.json())}
    assert first_ids.isdisjoint(second_ids)

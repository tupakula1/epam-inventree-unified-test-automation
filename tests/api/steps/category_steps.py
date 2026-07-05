"""Step definitions for category CRUD/validation BDD scenarios."""
from __future__ import annotations

from typing import Any
from uuid import uuid4

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from api.endpoints.CategoryAPI import CategoryAPI
from api.payloads.category_payloads import full_category_payload, minimal_category_payload, missing_name_payload

scenarios("api/category_api.feature")


def _safe_delete_category(category_api: CategoryAPI, category_id: int):
    response = category_api.delete_category(category_id)
    if response.status_code == 204:
        return response

    if response.status_code == 400:
        body = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}
        required_delete_flags = {"delete_child_categories", "delete_parts"}
        if isinstance(body, dict) and required_delete_flags.intersection(body.keys()):
            return category_api._request(
                "DELETE",
                f"/api/part/category/{category_id}/",
                json={"delete_child_categories": True, "delete_parts": True},
            )

    return response


@pytest.fixture
def bdd_category_context() -> dict[str, Any]:
    return {
        "payload": None,
        "response": None,
        "category_id": None,
        "parent_id": None,
        "created_category_ids": [],
        "expected_name": None,
        "updated_name": None,
        "last_deleted_id": None,
    }


@pytest.fixture(autouse=True)
def cleanup_bdd_categories(category_api: CategoryAPI, bdd_category_context: dict[str, Any]) -> None:
    yield
    for category_id in reversed(bdd_category_context["created_category_ids"]):
        _safe_delete_category(category_api, category_id)


@given("a unique minimal category payload")
def step_unique_minimal_category_payload(bdd_category_context: dict[str, Any]) -> None:
    bdd_category_context["payload"] = minimal_category_payload()
    bdd_category_context["expected_name"] = bdd_category_context["payload"]["name"]


@given("an existing category via API")
def step_existing_category(category_api: CategoryAPI, bdd_category_context: dict[str, Any]) -> None:
    payload = minimal_category_payload()
    response = category_api.create_category(payload)
    category_api.assert_status(response, 201)

    category_id = response.json()["pk"]
    bdd_category_context["category_id"] = category_id
    bdd_category_context["created_category_ids"].append(category_id)


@given("an existing parent category via API")
def step_existing_parent_category(category_api: CategoryAPI, bdd_category_context: dict[str, Any]) -> None:
    payload = minimal_category_payload()
    response = category_api.create_category(payload)
    category_api.assert_status(response, 201)

    parent_id = response.json()["pk"]
    bdd_category_context["parent_id"] = parent_id
    bdd_category_context["created_category_ids"].append(parent_id)


@given("a category payload missing the required name")
def step_missing_name_category_payload(bdd_category_context: dict[str, Any]) -> None:
    bdd_category_context["payload"] = missing_name_payload()


@when("I create the category via API")
def step_create_category(category_api: CategoryAPI, bdd_category_context: dict[str, Any]) -> None:
    payload = bdd_category_context["payload"]
    assert isinstance(payload, dict), "Expected payload to be prepared before create step"

    response = category_api.create_category(payload)
    bdd_category_context["response"] = response

    if response.status_code == 201:
        category_id = response.json()["pk"]
        bdd_category_context["category_id"] = category_id
        bdd_category_context["created_category_ids"].append(category_id)


@when("I create a child category for that parent")
def step_create_child_category(category_api: CategoryAPI, bdd_category_context: dict[str, Any]) -> None:
    parent_id = bdd_category_context["parent_id"]
    assert isinstance(parent_id, int), "Expected a parent category id"

    payload = full_category_payload(parent=parent_id)
    response = category_api.create_category(payload)
    bdd_category_context["response"] = response

    if response.status_code == 201:
        category_id = response.json()["pk"]
        bdd_category_context["category_id"] = category_id
        bdd_category_context["created_category_ids"].append(category_id)


@when(parsers.parse('I update the category name to "{new_name}"'))
def step_update_category_name(category_api: CategoryAPI, bdd_category_context: dict[str, Any], new_name: str) -> None:
    category_id = bdd_category_context["category_id"]
    assert isinstance(category_id, int), "Expected an existing category id"

    unique_name = f"{new_name} {uuid4().hex[:6]}"
    bdd_category_context["updated_name"] = unique_name
    bdd_category_context["response"] = category_api.update_category(category_id, {"name": unique_name})


@when("I delete the category")
def step_delete_category(category_api: CategoryAPI, bdd_category_context: dict[str, Any]) -> None:
    category_id = bdd_category_context["category_id"]
    assert isinstance(category_id, int), "Expected an existing category id"

    bdd_category_context["response"] = _safe_delete_category(category_api, category_id)
    bdd_category_context["last_deleted_id"] = category_id

    if category_id in bdd_category_context["created_category_ids"]:
        bdd_category_context["created_category_ids"].remove(category_id)


@then(parsers.parse("the category API response status should be {status:d}"))
def step_assert_category_status(bdd_category_context: dict[str, Any], status: int) -> None:
    response = bdd_category_context["response"]
    assert response is not None, "Expected response to be available"
    assert response.status_code == status, f"Expected {status}, got {response.status_code}: {response.text}"


@then("the created category response should include the request name")
def step_assert_created_category_name(bdd_category_context: dict[str, Any]) -> None:
    response = bdd_category_context["response"]
    expected_name = bdd_category_context["expected_name"]

    assert response is not None, "Expected response to be available"
    assert response.json()["name"] == expected_name


@then("the created category parent id should match the parent category id")
def step_assert_parent_id(bdd_category_context: dict[str, Any]) -> None:
    response = bdd_category_context["response"]
    parent_id = bdd_category_context["parent_id"]

    assert response is not None, "Expected response to be available"
    assert response.json()["parent"] == parent_id


@then(parsers.parse('the category API response name should be "{name}"'))
def step_assert_category_name(bdd_category_context: dict[str, Any], name: str) -> None:
    response = bdd_category_context["response"]
    assert response is not None, "Expected response to be available"
    actual_name = response.json()["name"]
    updated_name = bdd_category_context.get("updated_name")
    if isinstance(updated_name, str) and updated_name:
        assert actual_name == updated_name
        assert actual_name.startswith(name)
        return

    assert actual_name == name


@then("fetching the deleted category by id should return 404")
def step_assert_deleted_category_not_found(
    category_api: CategoryAPI,
    bdd_category_context: dict[str, Any],
) -> None:
    category_id = bdd_category_context["last_deleted_id"]
    assert isinstance(category_id, int), "Expected deleted category id"
    response = category_api.get_category(category_id)
    assert response.status_code == 404


@then(parsers.parse('the category API error should contain field "{field}"'))
def step_assert_category_error_field(bdd_category_context: dict[str, Any], field: str) -> None:
    response = bdd_category_context["response"]
    assert response is not None, "Expected response to be available"
    assert field in response.json(), f"Expected field '{field}' in error payload: {response.text}"

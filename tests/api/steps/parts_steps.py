"""Step definitions for parts CRUD/validation BDD scenarios."""
from __future__ import annotations

from typing import Any
from uuid import uuid4

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from api.endpoints.PartsAPI import PartsAPI
from api.payloads.part_payloads import duplicate_ipn_payload, minimal_part_payload, missing_name_payload

scenarios("api/parts_api.feature")


def _safe_delete_part(parts_api: PartsAPI, part_id: int):
    response = parts_api.delete_part(part_id)
    if response.status_code == 204:
        return response

    if response.status_code == 400:
        patch_response = parts_api.update_part(part_id, {"active": False})
        if patch_response.status_code == 200:
            return parts_api.delete_part(part_id)

    return response


@pytest.fixture
def bdd_part_context() -> dict[str, Any]:
    return {
        "payload": None,
        "response": None,
        "part_id": None,
        "created_part_ids": [],
        "expected_name": None,
        "updated_name": None,
        "last_deleted_id": None,
    }


@pytest.fixture(autouse=True)
def cleanup_bdd_parts(parts_api: PartsAPI, bdd_part_context: dict[str, Any]) -> None:
    yield
    for part_id in reversed(bdd_part_context["created_part_ids"]):
        _safe_delete_part(parts_api, part_id)


@given("a unique minimal part payload")
def step_unique_minimal_payload(bdd_part_context: dict[str, Any]) -> None:
    bdd_part_context["payload"] = minimal_part_payload()
    bdd_part_context["expected_name"] = bdd_part_context["payload"]["name"]


@given("an existing part created via API")
def step_existing_part(parts_api: PartsAPI, bdd_part_context: dict[str, Any]) -> None:
    payload = minimal_part_payload()
    response = parts_api.create_part(payload)
    parts_api.assert_status(response, 201)

    part_id = response.json()["pk"]
    bdd_part_context["part_id"] = part_id
    bdd_part_context["created_part_ids"].append(part_id)
    bdd_part_context["expected_name"] = payload["name"]


@given(parsers.parse('an existing part with IPN "{ipn}"'))
def step_existing_part_with_ipn(parts_api: PartsAPI, bdd_part_context: dict[str, Any], ipn: str) -> None:
    payload = minimal_part_payload()
    payload["IPN"] = ipn

    response = parts_api.create_part(payload)
    parts_api.assert_status(response, 201)

    part_id = response.json()["pk"]
    bdd_part_context["part_id"] = part_id
    bdd_part_context["created_part_ids"].append(part_id)


@given("a part payload missing the required name")
def step_missing_name_payload(bdd_part_context: dict[str, Any]) -> None:
    bdd_part_context["payload"] = missing_name_payload()


@when("I create the part via API")
def step_create_part(parts_api: PartsAPI, bdd_part_context: dict[str, Any]) -> None:
    payload = bdd_part_context["payload"]
    assert isinstance(payload, dict), "Expected payload to be prepared before create step"

    response = parts_api.create_part(payload)
    bdd_part_context["response"] = response

    if response.status_code == 201:
        part_id = response.json()["pk"]
        bdd_part_context["part_id"] = part_id
        bdd_part_context["created_part_ids"].append(part_id)


@when("I fetch the created part by id")
def step_get_part_by_id(parts_api: PartsAPI, bdd_part_context: dict[str, Any]) -> None:
    part_id = bdd_part_context["part_id"]
    assert isinstance(part_id, int), "Expected an existing part id"
    bdd_part_context["response"] = parts_api.get_part(part_id)


@when(parsers.parse('I update the created part name to "{new_name}"'))
def step_update_part_name(parts_api: PartsAPI, bdd_part_context: dict[str, Any], new_name: str) -> None:
    part_id = bdd_part_context["part_id"]
    assert isinstance(part_id, int), "Expected an existing part id"

    unique_name = f"{new_name} {uuid4().hex[:6]}"
    bdd_part_context["updated_name"] = unique_name
    bdd_part_context["response"] = parts_api.update_part(part_id, {"name": unique_name})


@when("I delete the created part")
def step_delete_part(parts_api: PartsAPI, bdd_part_context: dict[str, Any]) -> None:
    part_id = bdd_part_context["part_id"]
    assert isinstance(part_id, int), "Expected an existing part id"

    bdd_part_context["response"] = _safe_delete_part(parts_api, part_id)
    bdd_part_context["last_deleted_id"] = part_id

    if part_id in bdd_part_context["created_part_ids"]:
        bdd_part_context["created_part_ids"].remove(part_id)


@when(parsers.parse('I create another part with duplicate IPN "{ipn}"'))
def step_create_duplicate_ipn(parts_api: PartsAPI, bdd_part_context: dict[str, Any], ipn: str) -> None:
    bdd_part_context["response"] = parts_api.create_part(duplicate_ipn_payload(ipn))


@then(parsers.parse("the API response status should be {status:d}"))
def step_assert_status(bdd_part_context: dict[str, Any], status: int) -> None:
    response = bdd_part_context["response"]
    assert response is not None, "Expected response to be available"
    assert response.status_code == status, f"Expected {status}, got {response.status_code}: {response.text}"


@then(parsers.parse('the API response status should be one of "{status_codes}"'))
def step_assert_status_one_of(bdd_part_context: dict[str, Any], status_codes: str) -> None:
    response = bdd_part_context["response"]
    assert response is not None, "Expected response to be available"

    expected = {int(code.strip()) for code in status_codes.split(",") if code.strip()}
    assert response.status_code in expected, (
        f"Expected one of {sorted(expected)}, got {response.status_code}: {response.text}"
    )


@then("the created part response should include the request name")
def step_assert_created_name(bdd_part_context: dict[str, Any]) -> None:
    response = bdd_part_context["response"]
    expected_name = bdd_part_context["expected_name"]

    assert response is not None, "Expected response to be available"
    assert response.json()["name"] == expected_name


@then("the API response should contain the same part id")
def step_assert_same_part_id(bdd_part_context: dict[str, Any]) -> None:
    response = bdd_part_context["response"]
    part_id = bdd_part_context["part_id"]

    assert response is not None, "Expected response to be available"
    assert response.json()["pk"] == part_id


@then(parsers.parse('the API response part name should be "{name}"'))
def step_assert_part_name(bdd_part_context: dict[str, Any], name: str) -> None:
    response = bdd_part_context["response"]
    assert response is not None, "Expected response to be available"
    actual_name = response.json()["name"]
    updated_name = bdd_part_context.get("updated_name")
    if isinstance(updated_name, str) and updated_name:
        assert actual_name == updated_name
        assert actual_name.startswith(name)
        return

    assert actual_name == name


@then("fetching the deleted part by id should return 404")
def step_assert_deleted_not_found(parts_api: PartsAPI, bdd_part_context: dict[str, Any]) -> None:
    part_id = bdd_part_context["last_deleted_id"]
    assert isinstance(part_id, int), "Expected deleted part id"
    response = parts_api.get_part(part_id)
    assert response.status_code == 404


@then(parsers.parse('the API error should contain field "{field}"'))
def step_assert_error_field(bdd_part_context: dict[str, Any], field: str) -> None:
    response = bdd_part_context["response"]
    assert response is not None, "Expected response to be available"
    assert field in response.json(), f"Expected field '{field}' in error payload: {response.text}"

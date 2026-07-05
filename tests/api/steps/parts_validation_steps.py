"""Step definitions for parts validation BDD scenarios."""
from __future__ import annotations

from typing import Any, Generator

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from api.endpoints.PartsAPI import PartsAPI
from api.payloads.part_payloads import duplicate_ipn_payload, minimal_part_payload, missing_name_payload

scenarios("api/parts_validation_api.feature")


def _safe_delete_part(parts_api: PartsAPI, part_id: int) -> None:
    delete_response = parts_api.delete_part(part_id)
    if delete_response.status_code == 204:
        return

    if delete_response.status_code == 400:
        patch_response = parts_api.update_part(part_id, {"active": False})
        if patch_response.status_code == 200:
            parts_api.delete_part(part_id)


@pytest.fixture
def parts_validation_context() -> dict[str, Any]:
    return {
        "payload": None,
        "response": None,
        "created_part_ids": [],
        "requested_pk": None,
    }


@pytest.fixture(autouse=True)
def cleanup_parts_validation(
    parts_api: PartsAPI,
    parts_validation_context: dict[str, Any],
) -> Generator[None, None, None]:
    yield
    for part_id in reversed(parts_validation_context["created_part_ids"]):
        _safe_delete_part(parts_api, part_id)


@given("a validation payload without part name")
def step_validation_missing_name(parts_validation_context: dict[str, Any]) -> None:
    parts_validation_context["payload"] = missing_name_payload()


@given(parsers.parse("a validation payload with part name length {length:d}"))
def step_validation_name_length(parts_validation_context: dict[str, Any], length: int) -> None:
    parts_validation_context["payload"] = {"name": "X" * length}


@given(parsers.parse('an existing part for duplicate IPN "{ipn}"'))
def step_existing_duplicate_ipn(
    parts_api: PartsAPI,
    parts_validation_context: dict[str, Any],
    ipn: str,
) -> None:
    payload = minimal_part_payload()
    payload["IPN"] = ipn

    response = parts_api.create_part(payload)
    parts_api.assert_status(response, 201)

    parts_validation_context["created_part_ids"].append(response.json()["pk"])


@given(parsers.parse("a validation payload with client pk {pk:d}"))
def step_validation_client_pk(parts_validation_context: dict[str, Any], pk: int) -> None:
    payload = minimal_part_payload()
    payload["pk"] = pk
    parts_validation_context["requested_pk"] = pk
    parts_validation_context["payload"] = payload


@given("a validation payload with empty name")
def step_validation_empty_name(parts_validation_context: dict[str, Any]) -> None:
    parts_validation_context["payload"] = {"name": ""}


@given(parsers.parse('a validation payload with field "{field}" length {length:d}'))
def step_validation_field_length(parts_validation_context: dict[str, Any], field: str, length: int) -> None:
    payload: dict[str, Any] = {"name": "Boundary Test Part"}
    payload[field] = "X" * length
    parts_validation_context["payload"] = payload


@when("I create the part for validation check")
def step_create_part_validation(parts_api: PartsAPI, parts_validation_context: dict[str, Any]) -> None:
    payload = parts_validation_context["payload"]
    assert isinstance(payload, dict), "Expected payload to be prepared"

    response = parts_api.create_part(payload)
    parts_validation_context["response"] = response

    if response.status_code == 201:
        parts_validation_context["created_part_ids"].append(response.json()["pk"])


@when(parsers.parse('I create another part for duplicate IPN "{ipn}"'))
def step_create_duplicate_validation(
    parts_api: PartsAPI,
    parts_validation_context: dict[str, Any],
    ipn: str,
) -> None:
    parts_validation_context["response"] = parts_api.create_part(duplicate_ipn_payload(ipn))


@then(parsers.parse("the validation API response status should be {status:d}"))
def step_validation_status(parts_validation_context: dict[str, Any], status: int) -> None:
    response = parts_validation_context["response"]
    assert response is not None, "Expected response to be available"
    assert response.status_code == status, f"Expected {status}, got {response.status_code}: {response.text}"


@then(parsers.parse('the validation API response status should be one of "{status_codes}"'))
def step_validation_status_one_of(parts_validation_context: dict[str, Any], status_codes: str) -> None:
    response = parts_validation_context["response"]
    assert response is not None, "Expected response to be available"

    expected = {int(item.strip()) for item in status_codes.split(",") if item.strip()}
    assert response.status_code in expected, (
        f"Expected one of {sorted(expected)}, got {response.status_code}: {response.text}"
    )


@then(parsers.parse('validation error payload should include field "{field}"'))
def step_validation_error_field(parts_validation_context: dict[str, Any], field: str) -> None:
    response = parts_validation_context["response"]
    assert response is not None, "Expected response to be available"
    assert field in response.json(), f"Expected {field} in {response.text}"


@then(parsers.parse("created part pk should not equal {pk:d}"))
def step_validation_pk_not_equal(parts_validation_context: dict[str, Any], pk: int) -> None:
    response = parts_validation_context["response"]
    assert response is not None, "Expected response to be available"
    assert response.json()["pk"] != pk

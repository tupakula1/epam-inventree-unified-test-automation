"""Step definitions for parts edge-case BDD scenarios."""
from __future__ import annotations

import os
from typing import Any, Generator
from uuid import uuid4
from urllib.parse import urlsplit

import pytest
import requests as req_lib
from pytest_bdd import given, parsers, scenarios, then, when

from api.endpoints.PartsAPI import PartsAPI

scenarios("api/parts_edge_cases_api.feature")


def _safe_delete_part(parts_api: PartsAPI, part_id: int) -> None:
    delete_response = parts_api.delete_part(part_id)
    if delete_response.status_code == 204:
        return

    if delete_response.status_code == 400:
        patch_response = parts_api.update_part(part_id, {"active": False})
        if patch_response.status_code == 200:
            parts_api.delete_part(part_id)


def _api_service_root_from_env() -> str:
    api_base = os.getenv("API_BASE_URL", "https://demo.inventree.org/api")
    parsed = urlsplit(api_base)
    if parsed.scheme and parsed.netloc:
        return f"{parsed.scheme}://{parsed.netloc}"
    return "https://demo.inventree.org"


@pytest.fixture
def parts_edge_context() -> dict[str, Any]:
    return {
        "payload": None,
        "response": None,
        "created_part_ids": [],
        "token": None,
    }


@pytest.fixture(autouse=True)
def cleanup_parts_edge(
    parts_api: PartsAPI,
    parts_edge_context: dict[str, Any],
) -> Generator[None, None, None]:
    yield
    for part_id in reversed(parts_edge_context["created_part_ids"]):
        _safe_delete_part(parts_api, part_id)


@given("a valid API token for edge scenario")
def step_valid_token_for_edge(parts_edge_context: dict[str, Any], api_token: str) -> None:
    parts_edge_context["token"] = api_token


@given("a valid parts api client for edge scenario")
def step_valid_parts_client_for_edge(parts_edge_context: dict[str, Any]) -> None:
    # Context intentionally empty; fixture injection happens in action step.
    parts_edge_context["payload"] = None


@given(parsers.parse('an edge payload with part name "{name}"'))
def step_edge_payload_name(parts_edge_context: dict[str, Any], name: str) -> None:
    parts_edge_context["payload"] = {
        "name": name,
        "IPN": f"EDGE-{uuid4().hex[:10]}",
    }


@given(parsers.parse("an edge payload with max part name length {length:d}"))
def step_edge_payload_name_length(parts_edge_context: dict[str, Any], length: int) -> None:
    parts_edge_context["payload"] = {
        "name": "A" * length,
        "IPN": f"EDGE-{uuid4().hex[:10]}",
    }


@when("I call parts list endpoint without authentication")
def step_call_without_auth(parts_edge_context: dict[str, Any]) -> None:
    base = _api_service_root_from_env()
    parts_edge_context["response"] = req_lib.get(f"{base}/api/part/", timeout=10)


@when("I call parts list endpoint with invalid token")
def step_call_with_invalid_token(parts_edge_context: dict[str, Any]) -> None:
    bad_client = PartsAPI(
        base_url=_api_service_root_from_env(),
        token="invalid-token-xyz",
    )
    parts_edge_context["response"] = bad_client.list_parts()


@when("I create part with invalid JSON body")
def step_invalid_json_body(parts_edge_context: dict[str, Any]) -> None:
    token = parts_edge_context["token"]
    assert isinstance(token, str) and token, "Expected api token before invalid JSON request"

    base = _api_service_root_from_env()
    parts_edge_context["response"] = req_lib.post(
        f"{base}/api/part/",
        data="not-valid-json",
        headers={
            "Authorization": f"Token {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        timeout=10,
    )


@when("I delete the parts list endpoint")
def step_delete_list_endpoint(parts_api: PartsAPI, parts_edge_context: dict[str, Any]) -> None:
    parts_edge_context["response"] = parts_api._delete("/api/part/")


@when("I create edge case part")
def step_create_edge_part(parts_api: PartsAPI, parts_edge_context: dict[str, Any]) -> None:
    payload = parts_edge_context["payload"]
    assert isinstance(payload, dict), "Expected edge payload to be prepared"

    response = parts_api.create_part(payload)
    parts_edge_context["response"] = response

    if response.status_code == 201:
        parts_edge_context["created_part_ids"].append(response.json()["pk"])


@then(parsers.parse("the edge API response status should be {status:d}"))
def step_edge_status(parts_edge_context: dict[str, Any], status: int) -> None:
    response = parts_edge_context["response"]
    assert response is not None, "Expected response to be available"
    assert response.status_code == status, f"Expected {status}, got {response.status_code}: {response.text}"


@then(parsers.parse('the edge API response status should be one of "{status_codes}"'))
def step_edge_status_one_of(parts_edge_context: dict[str, Any], status_codes: str) -> None:
    response = parts_edge_context["response"]
    assert response is not None, "Expected response to be available"

    expected = {int(item.strip()) for item in status_codes.split(",") if item.strip()}
    assert response.status_code in expected, (
        f"Expected one of {sorted(expected)}, got {response.status_code}: {response.text}"
    )

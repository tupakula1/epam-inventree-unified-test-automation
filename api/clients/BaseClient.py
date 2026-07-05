"""
BaseClient — shared HTTP session for all API endpoint wrappers.

Provides:
- Token-based authentication
- Centralized request/response logging
- Status-code assertion helper
- Session-level connection reuse (requests.Session)
"""
from __future__ import annotations

import logging
from typing import Any

import requests

logger = logging.getLogger(__name__)


class BaseClient:
    def __init__(self, base_url: str, token: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Token {token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    # ─── Private request helpers ──────────────────────────────────────────────
    def _url(self, endpoint: str) -> str:
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def _log_request(self, method: str, url: str, **kwargs: Any) -> None:
        logger.debug("[%s] %s | payload=%s | params=%s", method, url,
                     kwargs.get("json"), kwargs.get("params"))

    def _log_response(self, response: requests.Response) -> None:
        logger.debug(
            "Response %s | %s | body=%s",
            response.status_code,
            response.url,
            response.text[:500],
        )

    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any,
    ) -> requests.Response:
        url = self._url(endpoint)
        self._log_request(method, url, **kwargs)
        response = self.session.request(method, url, timeout=30, **kwargs)
        self._log_response(response)
        return response

    # ─── Public HTTP methods ──────────────────────────────────────────────────
    def _get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> requests.Response:
        return self._request("GET", endpoint, params=params)

    def _post(
        self,
        endpoint: str,
        payload: dict[str, Any] | None = None,
    ) -> requests.Response:
        return self._request("POST", endpoint, json=payload)

    def _patch(
        self,
        endpoint: str,
        payload: dict[str, Any] | None = None,
    ) -> requests.Response:
        return self._request("PATCH", endpoint, json=payload)

    def _put(
        self,
        endpoint: str,
        payload: dict[str, Any] | None = None,
    ) -> requests.Response:
        return self._request("PUT", endpoint, json=payload)

    def _delete(self, endpoint: str) -> requests.Response:
        return self._request("DELETE", endpoint)

    # ─── Assertion helper ─────────────────────────────────────────────────────
    @staticmethod
    def assert_status(response: requests.Response, expected: int) -> None:
        actual = response.status_code
        if actual != expected:
            raise AssertionError(
                f"Expected HTTP {expected}, got {actual}.\n"
                f"URL: {response.url}\n"
                f"Body: {response.text[:1000]}"
            )

"""
PartsAPI — endpoint wrapper for /api/part/ and related routes.
"""
from __future__ import annotations

import logging
from typing import Any

import requests

from api.clients.BaseClient import BaseClient

logger = logging.getLogger(__name__)

PARTS_ENDPOINT = "/api/part/"
PART_BY_ID = "/api/part/{part_id}/"
PART_THUMBS = "/api/part/{part_id}/thumbs/"


class PartsAPI(BaseClient):
    """Wrapper for all InvenTree Part REST endpoints."""

    # ─── List / Search ────────────────────────────────────────────────────────
    def list_parts(self, filters: dict[str, Any] | None = None) -> requests.Response:
        """GET /api/part/  — list parts with optional filters."""
        logger.info("Listing parts | filters=%s", filters)
        return self._get(PARTS_ENDPOINT, params=filters)

    def search_parts(self, query: str) -> requests.Response:
        """GET /api/part/?search=<query>"""
        return self.list_parts(filters={"search": query})

    # ─── Single Part ──────────────────────────────────────────────────────────
    def get_part(self, part_id: int) -> requests.Response:
        """GET /api/part/{id}/"""
        logger.info("Getting part id=%d", part_id)
        return self._get(PART_BY_ID.format(part_id=part_id))

    def create_part(self, payload: dict[str, Any]) -> requests.Response:
        """POST /api/part/"""
        logger.info("Creating part | name=%s", payload.get("name"))
        return self._post(PARTS_ENDPOINT, payload=payload)

    def update_part(self, part_id: int, payload: dict[str, Any]) -> requests.Response:
        """PATCH /api/part/{id}/"""
        logger.info("Updating part id=%d | fields=%s", part_id, list(payload.keys()))
        return self._patch(PART_BY_ID.format(part_id=part_id), payload=payload)

    def delete_part(self, part_id: int) -> requests.Response:
        """DELETE /api/part/{id}/"""
        logger.info("Deleting part id=%d", part_id)
        return self._delete(PART_BY_ID.format(part_id=part_id))

    # ─── Pagination helpers ───────────────────────────────────────────────────
    def list_parts_paginated(
        self,
        limit: int = 25,
        offset: int = 0,
        extra_filters: dict[str, Any] | None = None,
    ) -> requests.Response:
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if extra_filters:
            params.update(extra_filters)
        return self._get(PARTS_ENDPOINT, params=params)

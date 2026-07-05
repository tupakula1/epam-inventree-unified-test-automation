"""
CategoryAPI — endpoint wrapper for /api/part/category/.
"""
from __future__ import annotations

import logging
from typing import Any

import requests

from api.clients.BaseClient import BaseClient

logger = logging.getLogger(__name__)

CATEGORY_ENDPOINT = "/api/part/category/"
CATEGORY_BY_ID = "/api/part/category/{category_id}/"


class CategoryAPI(BaseClient):
    """Wrapper for InvenTree Part Category REST endpoints."""

    def list_categories(self, filters: dict[str, Any] | None = None) -> requests.Response:
        logger.info("Listing categories")
        return self._get(CATEGORY_ENDPOINT, params=filters)

    def get_category(self, category_id: int) -> requests.Response:
        return self._get(CATEGORY_BY_ID.format(category_id=category_id))

    def create_category(self, payload: dict[str, Any]) -> requests.Response:
        logger.info("Creating category | name=%s", payload.get("name"))
        return self._post(CATEGORY_ENDPOINT, payload=payload)

    def update_category(self, category_id: int, payload: dict[str, Any]) -> requests.Response:
        return self._patch(CATEGORY_BY_ID.format(category_id=category_id), payload=payload)

    def delete_category(self, category_id: int) -> requests.Response:
        logger.info("Deleting category id=%d", category_id)
        return self._delete(CATEGORY_BY_ID.format(category_id=category_id))

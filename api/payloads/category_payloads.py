"""
Category payload builders.
"""
from __future__ import annotations

from typing import Any, Optional

from faker import Faker

fake = Faker()


def minimal_category_payload(name: Optional[str] = None) -> dict[str, Any]:
    return {"name": name or f"Category {fake.unique.bothify('####')}"}


def full_category_payload(
    name: Optional[str] = None,
    description: Optional[str] = None,
    parent: Optional[int] = None,
) -> dict[str, Any]:
    return {
        "name": name or f"Category {fake.unique.bothify('####')}",
        "description": description or fake.sentence(nb_words=5),
        "parent": parent,
    }


def missing_name_payload() -> dict[str, Any]:
    return {"description": "Category without name"}

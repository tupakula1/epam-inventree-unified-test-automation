"""
Part payload builders — factory functions that produce request body dicts.

These keep test code clean and enable easy parameterisation.
"""
from __future__ import annotations

from typing import Any, Optional

from faker import Faker

fake = Faker()


def minimal_part_payload(name: Optional[str] = None) -> dict[str, Any]:
    """Minimum required payload for creating a Part."""
    return {
        "name": name or f"Test Part {fake.unique.bothify('####')}",
    }


def full_part_payload(
    name: Optional[str] = None,
    ipn: Optional[str] = None,
    description: Optional[str] = None,
    category: Optional[int] = None,
    units: Optional[str] = None,
) -> dict[str, Any]:
    """Full payload for a Part with all common optional fields."""
    return {
        "name": name or f"Full Part {fake.unique.bothify('####')}",
        "IPN": ipn or f"IPN-{fake.unique.bothify('???-####')}",
        "description": description or fake.sentence(nb_words=8),
        "category": category,
        "units": units or "pcs",
        "active": True,
        "component": True,
        "purchaseable": True,
    }


def template_part_payload(name: Optional[str] = None) -> dict[str, Any]:
    payload = minimal_part_payload(name)
    payload["is_template"] = True
    return payload


def virtual_part_payload(name: Optional[str] = None) -> dict[str, Any]:
    payload = minimal_part_payload(name)
    payload["virtual"] = True
    return payload


def assembly_part_payload(name: Optional[str] = None) -> dict[str, Any]:
    payload = minimal_part_payload(name)
    payload["assembly"] = True
    return payload


def trackable_part_payload(name: Optional[str] = None) -> dict[str, Any]:
    payload = minimal_part_payload(name)
    payload["trackable"] = True
    return payload


def inactive_part_payload(name: Optional[str] = None) -> dict[str, Any]:
    payload = minimal_part_payload(name)
    payload["active"] = False
    return payload


# ─── Invalid payloads for negative tests ──────────────────────────────────────
def missing_name_payload() -> dict[str, Any]:
    """Payload that omits the required 'name' field."""
    return {
        "description": "Part with missing name",
    }


def name_too_long_payload() -> dict[str, Any]:
    """Part name exceeding InvenTree max length (100 chars)."""
    return {
        "name": "X" * 101,
    }


def duplicate_ipn_payload(ipn: str) -> dict[str, Any]:
    """Payload with an IPN known to already be in use."""
    return {
        "name": f"Duplicate IPN Part {fake.unique.bothify('####')}",
        "IPN": ipn,
    }

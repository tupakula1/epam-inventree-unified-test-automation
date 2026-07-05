"""
utilities/data_generator.py — Faker-based test data factory.
"""
from __future__ import annotations

import random
import string
from faker import Faker

fake = Faker()


def unique_part_name(prefix: str = "Part") -> str:
    return f"{prefix} {fake.unique.bothify('????-####')}"


def unique_ipn(prefix: str = "IPN") -> str:
    return f"{prefix}-{fake.unique.bothify('???-####')}"


def random_string(length: int = 10) -> str:
    return "".join(random.choices(string.ascii_letters, k=length))


def random_number(min_val: int = 1, max_val: int = 1000) -> int:
    return random.randint(min_val, max_val)


def sentence() -> str:
    return fake.sentence(nb_words=8)

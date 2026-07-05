"""
utilities/retry_helper.py — retry decorator for flaky operations.
"""
from __future__ import annotations

import time
import logging
from typing import Any, Callable, TypeVar

logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


def retry(times: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)):
    """Decorator: retry a function up to `times` on specified exceptions."""
    def decorator(func: F) -> F:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    if attempt == times:
                        raise
                    logger.warning(
                        "Attempt %d/%d failed for %s: %s. Retrying in %.1fs...",
                        attempt, times, func.__name__, exc, delay,
                    )
                    time.sleep(delay)
        return wrapper  # type: ignore[return-value]
    return decorator

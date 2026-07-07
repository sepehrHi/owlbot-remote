"""
Core decorators: authorized_only, safe_reply.
"""
from __future__ import annotations

import functools
import logging
from typing import Callable, List

logger = logging.getLogger("owlbot.core")


def make_authorized_only(authorized_users: List[int], bot: object) -> Callable:
    """Factory: returns a decorator that restricts handlers to authorized users."""

    def authorized_only(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(message: object, *args: object, **kwargs: object) -> object:
            if message.chat.id not in authorized_users:  # type: ignore[attr-defined]
                bot.reply_to(message, "❌ Access denied.")  # type: ignore[attr-defined]
                return None
            return func(message, *args, **kwargs)

        return wrapper

    return authorized_only


def make_safe_reply(bot: object) -> Callable:
    """Factory: returns a decorator that catches all exceptions and notifies user."""

    def safe_reply(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(message: object, *args: object, **kwargs: object) -> object:
            try:
                return func(message, *args, **kwargs)
            except Exception as exc:
                logger.exception("Unhandled error in %s", func.__name__)
                try:
                    bot.reply_to(message, f"❌ Unexpected error: {exc}")  # type: ignore[attr-defined]
                except Exception:
                    pass
            return None

        return wrapper

    return safe_reply

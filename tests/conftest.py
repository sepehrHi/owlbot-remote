"""
Shared pytest fixtures for the OwlBot test suite.
"""
from __future__ import annotations

import logging

import pytest


@pytest.fixture
def valid_token() -> str:
    """A syntactically valid (but fake) Telegram bot token."""
    return "123456789:AAFakeTokenFakeTokenFakeTokenFakeTok"


@pytest.fixture
def valid_users() -> list:
    """A list with one authorized user id."""
    return [111111111]


@pytest.fixture(autouse=True)
def _reset_owlbot_logging():
    """
    Ensure each test starts with a clean 'owlbot' logger: no leftover
    handlers from a previous test, no propagation surprises.
    """
    owlbot_logger = logging.getLogger("owlbot")
    original_handlers = list(owlbot_logger.handlers)
    original_level = owlbot_logger.level
    original_propagate = owlbot_logger.propagate

    yield

    for handler in owlbot_logger.handlers:
        try:
            handler.close()
        except Exception:
            pass
    owlbot_logger.handlers.clear()
    owlbot_logger.handlers.extend(original_handlers)
    owlbot_logger.setLevel(original_level)
    owlbot_logger.propagate = original_propagate

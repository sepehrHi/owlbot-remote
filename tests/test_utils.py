"""
Tests for owlbot.core.utils helpers.
"""
from __future__ import annotations

import pytest

from owlbot.core.utils import format_bytes, format_uptime, safe_unlink, send_large_text


@pytest.mark.parametrize(
    "n, expected_unit",
    [
        (500, "B"),
        (2_048, "KB"),
        (5 * 1_024 * 1_024, "MB"),
    ],
)
def test_format_bytes_uses_expected_unit(n, expected_unit):
    result = format_bytes(n)
    assert result.endswith(expected_unit)


def test_format_uptime_formats_hours_minutes_seconds():
    assert format_uptime(3_661) == "1h 1m 1s"


def test_format_uptime_zero():
    assert format_uptime(0) == "0h 0m 0s"


def test_safe_unlink_removes_existing_file(tmp_path):
    target = tmp_path / "temp.txt"
    target.write_text("data")
    assert target.exists()

    safe_unlink(str(target))

    assert not target.exists()


def test_safe_unlink_ignores_missing_file(tmp_path):
    missing = tmp_path / "does_not_exist.txt"
    # Should not raise.
    safe_unlink(str(missing))


def test_safe_unlink_ignores_empty_path():
    # Should not raise for falsy input.
    safe_unlink("")


class _FakeBot:
    def __init__(self):
        self.messages = []
        self.documents = []

    def send_message(self, chat_id, text):
        self.messages.append((chat_id, text))

    def send_document(self, chat_id, file_obj, visible_file_name):
        self.documents.append((chat_id, visible_file_name))


def test_send_large_text_sends_message_for_short_text():
    bot = _FakeBot()
    send_large_text(bot, 42, "short text")
    assert bot.messages == [(42, "short text")]
    assert bot.documents == []


def test_send_large_text_sends_document_for_long_text(tmp_path, monkeypatch):
    bot = _FakeBot()
    long_text = "x" * 5_000

    send_large_text(bot, 42, long_text, filename="dump.txt")

    assert bot.messages == []
    assert len(bot.documents) == 1
    chat_id, filename = bot.documents[0]
    assert chat_id == 42
    assert filename == "dump.txt"

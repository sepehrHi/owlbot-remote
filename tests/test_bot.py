"""
Tests for owlbot.core.bot.OwlBot, focused on construction and logging
behavior (no real network / Telegram calls are made).
"""
from __future__ import annotations

import logging

import pytest

from owlbot import OwlBot


def test_owlbot_constructs_with_defaults(valid_token, valid_users, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    bot = OwlBot(token=valid_token, authorized_users=valid_users)
    assert bot.config.token == valid_token
    assert (tmp_path / "owlbot.log").exists()


def test_owlbot_rejects_unsupported_platform(valid_token, valid_users):
    with pytest.raises(NotImplementedError):
        OwlBot(token=valid_token, authorized_users=valid_users, platform="discord")


def test_owlbot_creates_log_file_by_default(valid_token, valid_users, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    log_path = tmp_path / "custom_owlbot.log"

    OwlBot(token=valid_token, authorized_users=valid_users, log_file=str(log_path))

    assert log_path.exists()


def test_owlbot_no_log_file_creates_no_file(valid_token, valid_users, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    OwlBot(token=valid_token, authorized_users=valid_users, log_file=None)

    assert list(tmp_path.glob("*.log")) == []


def test_owlbot_empty_string_log_file_creates_no_file(valid_token, valid_users, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    OwlBot(token=valid_token, authorized_users=valid_users, log_file="")

    assert list(tmp_path.glob("*.log")) == []


def test_owlbot_disable_logging_creates_no_file_and_no_handlers(
    valid_token, valid_users, tmp_path, monkeypatch
):
    monkeypatch.chdir(tmp_path)

    OwlBot(token=valid_token, authorized_users=valid_users, enable_logging=False)

    assert list(tmp_path.glob("*.log")) == []
    owlbot_logger = logging.getLogger("owlbot")
    assert len(owlbot_logger.handlers) == 1
    assert isinstance(owlbot_logger.handlers[0], logging.NullHandler)


def test_owlbot_disable_logging_suppresses_log_output(
    valid_token, valid_users, tmp_path, monkeypatch, capsys
):
    monkeypatch.chdir(tmp_path)

    OwlBot(token=valid_token, authorized_users=valid_users, enable_logging=False)

    captured = capsys.readouterr()
    assert "Initializing OwlBot" not in captured.out
    assert "Initializing OwlBot" not in captured.err


def test_owlbot_logging_enabled_writes_to_console(
    valid_token, valid_users, tmp_path, monkeypatch, capsys
):
    monkeypatch.chdir(tmp_path)

    OwlBot(token=valid_token, authorized_users=valid_users, log_file=None)

    captured = capsys.readouterr()
    assert "OwlBot initialized successfully" in captured.out

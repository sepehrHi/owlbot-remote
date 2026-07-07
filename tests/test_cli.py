"""
Tests for the owlbot CLI entry point (owlbot.__main__).
"""
from __future__ import annotations

import pytest

from owlbot import __main__ as cli


class _RecordingOwlBot:
    """Stand-in for OwlBot that records constructor kwargs instead of
    building a real bot / talking to Telegram."""

    last_kwargs: dict = {}

    def __init__(self, **kwargs):
        _RecordingOwlBot.last_kwargs = kwargs

    def run(self):
        pass


@pytest.fixture(autouse=True)
def _patch_owlbot(monkeypatch):
    monkeypatch.setattr("owlbot.OwlBot", _RecordingOwlBot)
    yield
    _RecordingOwlBot.last_kwargs = {}


def test_cli_parses_token_and_users():
    cli.main(["--token", "T", "--users", "1,2,3"])
    assert _RecordingOwlBot.last_kwargs["token"] == "T"
    assert _RecordingOwlBot.last_kwargs["authorized_users"] == [1, 2, 3]


def test_cli_invalid_user_id_exits(capsys):
    with pytest.raises(SystemExit) as exc_info:
        cli.main(["--token", "T", "--users", "not_a_number"])
    assert exc_info.value.code == 1
    assert "must be a comma-separated list" in capsys.readouterr().err


def test_cli_default_log_file_is_owlbot_log():
    cli.main(["--token", "T", "--users", "1"])
    assert _RecordingOwlBot.last_kwargs["log_file"] == "owlbot.log"
    assert _RecordingOwlBot.last_kwargs["enable_logging"] is True


def test_cli_no_log_file_flag_disables_file_only():
    cli.main(["--token", "T", "--users", "1", "--no-log-file"])
    assert _RecordingOwlBot.last_kwargs["log_file"] is None
    assert _RecordingOwlBot.last_kwargs["enable_logging"] is True


def test_cli_disable_logging_flag():
    cli.main(["--token", "T", "--users", "1", "--disable-logging"])
    assert _RecordingOwlBot.last_kwargs["enable_logging"] is False


def test_cli_custom_log_file_path():
    cli.main(["--token", "T", "--users", "1", "--log-file", "mybot.log"])
    assert _RecordingOwlBot.last_kwargs["log_file"] == "mybot.log"


def test_cli_modules_split_on_comma():
    cli.main(["--token", "T", "--users", "1", "--modules", "system,network"])
    assert _RecordingOwlBot.last_kwargs["modules"] == ["system", "network"]

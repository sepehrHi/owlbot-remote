"""
Tests for owlbot.config.BotConfig.
"""
from __future__ import annotations

import pytest

from owlbot.config import (
    AVAILABLE_MODULES,
    BotConfig,
    CROSS_PLATFORM_MODULES,
    VALID_LOG_LEVELS,
    WINDOWS_ONLY_MODULES,
)


def test_valid_config_creates_successfully(valid_token, valid_users):
    config = BotConfig(token=valid_token, authorized_users=valid_users)
    assert config.token == valid_token
    assert config.authorized_users == valid_users
    assert config.platform == "telegram"
    assert set(config.modules) <= AVAILABLE_MODULES


def test_empty_token_raises(valid_users):
    with pytest.raises(ValueError, match="token"):
        BotConfig(token="", authorized_users=valid_users)


def test_empty_authorized_users_raises(valid_token):
    with pytest.raises(ValueError, match="authorized"):
        BotConfig(token=valid_token, authorized_users=[])


def test_unknown_module_raises(valid_token, valid_users):
    with pytest.raises(ValueError, match="Unknown modules"):
        BotConfig(
            token=valid_token,
            authorized_users=valid_users,
            modules=["not_a_real_module"],
        )


def test_invalid_log_level_raises(valid_token, valid_users):
    with pytest.raises(ValueError, match="Invalid log_level"):
        BotConfig(token=valid_token, authorized_users=valid_users, log_level="LOUD")


def test_log_level_is_normalized_to_uppercase(valid_token, valid_users):
    config = BotConfig(token=valid_token, authorized_users=valid_users, log_level="debug")
    assert config.log_level == "DEBUG"
    assert config.log_level in VALID_LOG_LEVELS


@pytest.mark.parametrize("empty_value", [None, ""])
def test_empty_log_file_is_normalized_to_none(valid_token, valid_users, empty_value):
    config = BotConfig(token=valid_token, authorized_users=valid_users, log_file=empty_value)
    assert config.log_file is None


def test_log_file_path_is_preserved(valid_token, valid_users):
    config = BotConfig(token=valid_token, authorized_users=valid_users, log_file="custom.log")
    assert config.log_file == "custom.log"


def test_enable_logging_defaults_to_true(valid_token, valid_users):
    config = BotConfig(token=valid_token, authorized_users=valid_users)
    assert config.enable_logging is True


def test_enable_logging_can_be_disabled(valid_token, valid_users):
    config = BotConfig(token=valid_token, authorized_users=valid_users, enable_logging=False)
    assert config.enable_logging is False


def test_windows_only_modules_are_skipped_on_non_windows(monkeypatch, valid_token, valid_users):
    monkeypatch.setattr("owlbot.config.sys.platform", "linux")
    config = BotConfig(
        token=valid_token,
        authorized_users=valid_users,
        modules=list(AVAILABLE_MODULES),
    )
    assert set(config.modules) == CROSS_PLATFORM_MODULES
    assert not (set(config.modules) & WINDOWS_ONLY_MODULES)


def test_windows_only_modules_are_kept_on_windows(monkeypatch, valid_token, valid_users):
    monkeypatch.setattr("owlbot.config.sys.platform", "win32")
    config = BotConfig(
        token=valid_token,
        authorized_users=valid_users,
        modules=list(AVAILABLE_MODULES),
    )
    assert set(config.modules) == AVAILABLE_MODULES

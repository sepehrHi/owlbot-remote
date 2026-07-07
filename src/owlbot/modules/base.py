"""
BaseModule — every feature module inherits from this.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from owlbot.config import BotConfig


class BaseModule:
    """
    Subclass this for every feature module.
    Call self.register() to attach all handlers.
    """

    name: str = "base"

    def __init__(self, config: "BotConfig", bot: Any, auth: Any, safe: Any) -> None:
        """
        config : BotConfig instance
        bot    : TeleBot instance
        auth   : authorized_only decorator
        safe   : safe_reply decorator
        """
        self.config = config
        self.bot = bot
        self.auth = auth
        self.safe = safe

    def register(self) -> None:
        """Attach all command/message handlers to self.bot. Override in subclass."""
        raise NotImplementedError

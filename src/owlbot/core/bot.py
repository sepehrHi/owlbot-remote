"""
OwlBot — Main Public API
"""
from __future__ import annotations

import logging
import sys
import time
from typing import List, Optional

from owlbot.config import AVAILABLE_MODULES, BotConfig
from owlbot.core.utils import internet_ok
from owlbot.platform.telegram import TelegramPlatform


logger = logging.getLogger("owlbot")


def _configure_logging(config: BotConfig) -> None:
    """
    Configure (or intentionally disable) logging for the whole ``owlbot``
    logger hierarchy, based on ``config.enable_logging`` / ``config.log_file``.

    - ``enable_logging=False`` → no handlers at all, logger is silenced.
    - ``log_file`` falsy (``None`` / ``""``) → console-only logging, no
      log file is created on disk.
    - Otherwise → console + rotating-free file logging, as before.
    """
    root_owlbot_logger = logging.getLogger("owlbot")
    root_owlbot_logger.handlers.clear()

    if not config.enable_logging:
        root_owlbot_logger.addHandler(logging.NullHandler())
        root_owlbot_logger.propagate = False
        return

    root_owlbot_logger.propagate = False
    level = getattr(logging, config.log_level.upper(), logging.INFO)
    root_owlbot_logger.setLevel(level)
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    # Force UTF-8 on stdout so emoji in future log messages never crash on
    # a legacy Windows console code page (e.g. cp1252).
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, AttributeError):
            pass

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    root_owlbot_logger.addHandler(stream_handler)

    if config.log_file:
        file_handler = logging.FileHandler(config.log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        root_owlbot_logger.addHandler(file_handler)


class OwlBot:
    """
    Main class for users — clean and simple API.

    Usage::

        from owlbot import OwlBot

        bot = OwlBot(
            token="YOUR_BOT_TOKEN",
            authorized_users=[123456789],
            modules=["system", "screen", "audio"],
        )
        bot.run()
    """

    def __init__(
        self,
        token: str,
        authorized_users: List[int],
        platform: str = "telegram",
        modules: Optional[List[str]] = None,
        log_level: str = "INFO",
        log_file: Optional[str] = "owlbot.log",
        enable_logging: bool = True,
        **kwargs: object,
    ) -> None:
        self.config = BotConfig(
            token=token,
            authorized_users=authorized_users,
            platform=platform,
            modules=modules or list(AVAILABLE_MODULES),
            log_level=log_level,
            log_file=log_file,
            enable_logging=enable_logging,
            **kwargs,
        )

        _configure_logging(self.config)

        from owlbot import __version__ as _owlbot_version

        logger.info("Initializing OwlBot v%s with platform: %s", _owlbot_version, platform)

        # Platform Adapter (Telegram for now)
        if platform == "telegram":
            self._platform = TelegramPlatform(self.config)
        else:
            raise NotImplementedError(f"Platform '{platform}' not supported yet.")

        logger.info("OwlBot initialized successfully.")

    def _startup_report(self, tg_bot: object, uid: int) -> None:
        """
        Send an animated startup status card: connectivity → FFmpeg → ready.
        Falls back silently to a static message if editing fails.
        """
        frames = ["🦉 *Waking up…* ⏳", "🦉 *Waking up…* ⏳⏳", "🦉 *Waking up…* ⏳⏳⏳"]
        msg = None
        try:
            msg = tg_bot.send_message(uid, frames[0], parse_mode="Markdown")  # type: ignore[attr-defined]
            for frame in frames[1:]:
                time.sleep(0.35)
                tg_bot.edit_message_text(  # type: ignore[attr-defined]
                    frame, chat_id=uid, message_id=msg.message_id, parse_mode="Markdown"
                )
        except Exception:
            logger.debug("Startup animation skipped (non-fatal).", exc_info=True)

        net_ok = internet_ok()
        net_line = "🌐 Internet — ✅ connected" if net_ok else "🌐 Internet — ⚠️ no connection detected"

        ffmpeg_line = ""
        if "ffmpeg" in self.config.modules:
            try:
                from owlbot.modules.ffmpeg import check_ffmpeg
                ok, detail = check_ffmpeg()
                ffmpeg_line = (
                    f"🎬 FFmpeg — ✅ {detail.splitlines()[0]}" if ok
                    else "🎬 FFmpeg — ❌ not found (run /ffmpeg_install)"
                )
            except Exception:
                ffmpeg_line = "🎬 FFmpeg — ⚠️ check failed"

        modules_line = "🧩 Modules — " + ", ".join(sorted(self.config.modules))

        lines = ["🟢 *OwlBot is online!*", "─────────────────────", net_line]
        if ffmpeg_line:
            lines.append(ffmpeg_line)
        lines.append(modules_line)
        lines.append("")
        lines.append("Type `/help` for commands.")
        final_text = "\n".join(lines)

        try:
            if msg is not None:
                tg_bot.edit_message_text(  # type: ignore[attr-defined]
                    final_text, chat_id=uid, message_id=msg.message_id, parse_mode="Markdown"
                )
            else:
                tg_bot.send_message(uid, final_text, parse_mode="Markdown")  # type: ignore[attr-defined]
        except Exception:
            logger.warning("Could not send final startup status to user %s", uid, exc_info=True)

    def run(self) -> None:
        """Start the bot."""
        try:
            for uid in self.config.authorized_users:
                try:
                    if hasattr(self._platform, "_bot"):
                        self._startup_report(self._platform._bot, uid)
                except Exception:
                    logger.warning(
                        "Could not send startup notification to user %s", uid, exc_info=True
                    )

            self._platform.run()
        except KeyboardInterrupt:
            logger.info("Bot stopped by user.")
        except Exception:
            logger.critical("Bot crashed", exc_info=True)
        finally:
            logger.info("OwlBot shutdown complete.")


__all__ = ["OwlBot"]

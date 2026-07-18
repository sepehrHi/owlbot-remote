"""
Shared utility helpers used across all modules.
"""
from __future__ import annotations

import logging
import os
import socket
import tempfile
import time

logger = logging.getLogger("owlbot.utils")


def internet_ok(host: str = "8.8.8.8", port: int = 53, timeout: float = 3.0) -> bool:
    """Quick, dependency-free connectivity check (DNS-over-TCP probe to Google DNS)."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def animate_message(
    bot: object, chat_id: int, frames: list[str], delay: float = 0.35, parse_mode: str = "Markdown"
) -> object | None:
    """
    Send the first frame, then edit the same message through the remaining
    frames to create a lightweight "processing…" animation.

    Returns the sent message object (so the caller can do one final edit
    with the real result), or ``None`` if sending failed.
    """
    try:
        msg = bot.send_message(chat_id, frames[0], parse_mode=parse_mode)  # type: ignore[attr-defined]
    except Exception:
        logger.debug("animate_message: initial send failed", exc_info=True)
        return None

    for frame in frames[1:]:
        time.sleep(delay)
        try:
            bot.edit_message_text(  # type: ignore[attr-defined]
                frame, chat_id=chat_id, message_id=msg.message_id, parse_mode=parse_mode
            )
        except Exception:
            logger.debug("animate_message: frame edit failed", exc_info=True)
            break
    return msg


def finish_animation(
    bot: object, msg: object | None, chat_id: int, final_text: str, parse_mode: str = "Markdown"
) -> None:
    """Replace the animated message with the final result (or send fresh if msg is None)."""
    try:
        if msg is not None:
            bot.edit_message_text(  # type: ignore[attr-defined]
                final_text, chat_id=chat_id, message_id=msg.message_id, parse_mode=parse_mode
            )
        else:
            bot.send_message(chat_id, final_text, parse_mode=parse_mode)  # type: ignore[attr-defined]
    except Exception:
        logger.warning("finish_animation: could not deliver final message", exc_info=True)


def send_large_text(bot: object, chat_id: int, text: str, filename: str = "output.txt") -> None:
    """Send text as a message (≤4 000 chars) or as a .txt document."""
    if len(text) <= 4_000:
        bot.send_message(chat_id, text)  # type: ignore[attr-defined]
    else:
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".txt", mode="w", encoding="utf-8"
        ) as tmp:
            tmp.write(text)
            tmp_path = tmp.name
        try:
            with open(tmp_path, "rb") as f:
                bot.send_document(chat_id, f, visible_file_name=filename)  # type: ignore[attr-defined]
        finally:
            safe_unlink(tmp_path)


def safe_unlink(path: str) -> None:
    """Delete a file silently if it exists."""
    try:
        if path and os.path.exists(path):
            os.unlink(path)
    except Exception as exc:
        logger.warning("Could not delete temp file %s: %s", path, exc)


def format_bytes(n: int) -> str:
    """Format a byte count into a human-readable string."""
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1_024:
            return f"{n:.2f} {unit}"
        n /= 1_024
    return f"{n:.2f} PB"


def format_uptime(seconds: float) -> str:
    """Format seconds into a human-readable uptime string."""
    h, rem = divmod(int(seconds), 3_600)
    m, s = divmod(rem, 60)
    return f"{h}h {m}m {s}s"

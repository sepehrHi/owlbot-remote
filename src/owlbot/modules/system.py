"""System module — /start, /help, /status, /uptime, /ping, /lock, /shutdown, /restart
Uses dynamic help builder so /help only shows loaded modules.
"""
from __future__ import annotations

import os
import sys
import time

import psutil
from telebot.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from owlbot.core.help import build_help, build_module_section, module_titles
from owlbot.core.utils import animate_message, finish_animation, format_bytes, format_uptime
from owlbot.modules.base import BaseModule


def _bar(pct: float, width: int = 10) -> str:
    """Render a compact ASCII fill-bar, e.g. '████░░░░░░'."""
    filled = round(max(0.0, min(pct, 100.0)) / 100 * width)
    return "█" * filled + "░" * (width - filled)


def _build_menu_keyboard(loaded_modules: list[str]) -> InlineKeyboardMarkup:
    """Build a pretty inline keyboard: one button per loaded module + an 'all' button."""
    kb = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(title, callback_data=f"help:{mod}")
        for mod, title in module_titles(loaded_modules)
    ]
    for i in range(0, len(buttons), 2):
        kb.row(*buttons[i:i + 2])
    kb.add(InlineKeyboardButton("📋 Show all", callback_data="help:_all"))
    return kb


def _build_status_text() -> str:
    """Collect system stats and return formatted status block."""
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    bat = psutil.sensors_battery()
    net = psutil.net_io_counters()
    p_cores = psutil.cpu_count(logical=False) or "?"
    l_cores = psutil.cpu_count()
    lines = [
        "```",
        "📊  System Status",
        "─" * 28,
        f"🖥️  CPU   [{_bar(cpu)}] {cpu:5.1f}%",
        f"    Cores: {p_cores}P / {l_cores}L",
        f"🧠  RAM   [{_bar(ram.percent)}] {ram.percent:5.1f}%",
        f"    {ram.used/1024**3:.2f} / {ram.total/1024**3:.2f} GB",
        f"💾  Disk  [{_bar(disk.percent)}] {disk.percent:5.1f}%",
        f"    {disk.used/1024**3:.2f} / {disk.total/1024**3:.2f} GB",
        f"🌐  ↑ {format_bytes(net.bytes_sent)}  ↓ {format_bytes(net.bytes_recv)}",
    ]
    if bat:
        plug = "🔌 plugged" if bat.power_plugged else "🔋 battery"
        lines.append(f"⚡  Bat  [{_bar(bat.percent)}] {bat.percent:5.1f}%  {plug}")
    else:
        lines.append("⚡  Battery: N/A (desktop)")
    lines.append("```")
    return "\n".join(lines)


def _build_uptime_text() -> str:
    """Build uptime status block."""
    elapsed = time.time() - psutil.boot_time()
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    txt = (
        f"⏰  Uptime  {format_uptime(elapsed)}\n"
        f"{'─' * 28}\n"
        f"🖥️  CPU  [{_bar(cpu)}] {cpu:.1f}%\n"
        f"🧠  RAM  [{_bar(ram.percent)}] {ram.percent:.1f}%\n"
        f"    {ram.used / 1024 ** 3:.2f} / {ram.total / 1024 ** 3:.2f} GB"
    )
    return f"```\n{txt}\n```"


class SystemModule(BaseModule):
    name = "system"

    # ── Handler implementations ──────────────────────────────────────────────

    def _cmd_help(self, message: object) -> None:
        self.bot.send_chat_action(message.chat.id, "typing")
        text = build_help(self.config.modules)
        kb = _build_menu_keyboard(self.config.modules)
        self.bot.reply_to(message, text, parse_mode="Markdown", reply_markup=kb)

    def _cb_help_section(self, call: CallbackQuery) -> None:
        if call.message.chat.id not in self.config.authorized_users:
            self.bot.answer_callback_query(call.id, "❌ Access denied.")
            return
        mod = call.data.split(":", 1)[1]
        text = build_help(self.config.modules) if mod == "_all" else build_module_section(mod)
        kb = _build_menu_keyboard(self.config.modules)
        try:
            self.bot.edit_message_text(
                text, chat_id=call.message.chat.id, message_id=call.message.message_id,
                parse_mode="Markdown", reply_markup=kb,
            )
        except Exception:
            pass
        self.bot.answer_callback_query(call.id)

    def _cmd_ping(self, message: object) -> None:
        self.bot.reply_to(message, "🏓 *Pong!* Bot is alive and responsive.", parse_mode="Markdown")

    def _cmd_lock(self, message: object) -> None:
        self.bot.send_chat_action(message.chat.id, "typing")
        if sys.platform == "win32":
            import ctypes
            ctypes.windll.user32.LockWorkStation()
        else:
            os.system("xdg-screensaver lock 2>/dev/null || loginctl lock-session")
        self.bot.reply_to(message, "🔒 *Workstation locked.*", parse_mode="Markdown")

    def _cmd_shutdown(self, message: object) -> None:
        self.bot.reply_to(message, "🛑 *Shutting down in 3 seconds…*", parse_mode="Markdown")
        if sys.platform == "win32":
            os.system("shutdown /s /t 3")
        else:
            os.system("shutdown -h now")

    def _cmd_restart(self, message: object) -> None:
        self.bot.reply_to(message, "🔄 *Restarting in 3 seconds…*", parse_mode="Markdown")
        if sys.platform == "win32":
            os.system("shutdown /r /t 3")
        else:
            os.system("reboot")

    def _cmd_status(self, message: object) -> None:
        self.bot.send_chat_action(message.chat.id, "typing")
        anim_msg = animate_message(
            self.bot, message.chat.id,
            ["📊 *Gathering system info…* ⏳", "📊 *Gathering system info…* ⏳⏳"],
        )
        finish_animation(self.bot, anim_msg, message.chat.id, _build_status_text())

    def _cmd_uptime(self, message: object) -> None:
        self.bot.send_chat_action(message.chat.id, "typing")
        anim_msg = animate_message(
            self.bot, message.chat.id,
            ["⏰ *Checking uptime…* ⏳", "⏰ *Checking uptime…* ⏳⏳"],
        )
        finish_animation(self.bot, anim_msg, message.chat.id, _build_uptime_text())

    # ── Wiring ───────────────────────────────────────────────────────────────

    def register(self) -> None:
        bot, auth, safe = self.bot, self.auth, self.safe

        bot.message_handler(commands=["start", "help"])(auth(safe(self._cmd_help)))
        bot.callback_query_handler(func=lambda call: call.data.startswith("help:"))(safe(self._cb_help_section))
        bot.message_handler(commands=["ping"])(auth(safe(self._cmd_ping)))
        bot.message_handler(commands=["lock"])(auth(safe(self._cmd_lock)))
        bot.message_handler(commands=["shutdown"])(auth(safe(self._cmd_shutdown)))
        bot.message_handler(commands=["restart"])(auth(safe(self._cmd_restart)))
        bot.message_handler(commands=["status"])(auth(safe(self._cmd_status)))
        bot.message_handler(commands=["uptime"])(auth(safe(self._cmd_uptime)))

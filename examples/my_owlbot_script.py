"""
example_usage.py — نمونه استفاده از کتابخونه‌ی owlbot-remote

نصب:
    pip install owlbot-remote

نصب با همه ماژول‌ها (توصیه شده):
    pip install owlbot-remote[all]

نصب فقط ماژول‌های کراس-پلتفرم:
    pip install owlbot-remote[ui]
"""
from owlbot import OwlBot, BotConfig


# ── روش اول: کلاس OwlBot (API ساده) ──────────────────────────

def run_basic_bot():
    """ساده‌ترین شکل استفاده — فقط توکن و user ID رو بدی."""
    bot = OwlBot(
        token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
        authorized_users=[123456789],      # آیدی عددی تلگرامت
        modules=["system", "screen", "files", "processes"],
    )
    bot.run()


# ── روش دوم: OwlBot با تنظیمات پیشرفته ───────────────────────

def run_advanced_bot():
    """شکل پیشرفته — تنظیم ماژول‌ها، log level، تنظیمات اختصاصی."""
    bot = OwlBot(
        token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
        authorized_users=[123456789, 987654321],
        platform="telegram",
        modules=["system", "screen", "audio", "input", "monitoring"],
        # تنظیمات اضافی مستقیماً به BotConfig می‌رن
        log_level="DEBUG",
        log_file="owlbot.log",
        audio_sample_rate=44100,
        max_record_duration=30,
        max_file_size_mb=100,
        # ماژول‌های protected_processes رو نمیتونه بکشه
    )
    bot.run()


# ── روش سوم: ساختن مستقیم BotConfig ─────────────────────────

def run_with_config_object():
    """جداسازی config از اجرا برای تست‌پذیری بیشتر."""
    config = BotConfig(
        token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
        authorized_users=[123456789],
        modules=["system", "processes"],
        log_level="INFO",
    )
    bot = OwlBot(config=config)  # type: ignore
    # (اگر OwlBot config رو مستقیم بگیره — اینجا سادگی مثال)
    bot.run()


# ── روش چهارم: ساختن ماژول سفارشی ────────────────────────────

from owlbot.modules.base import BaseModule


class HelloModule(BaseModule):
    """یک ماژول ساده که /hello رو اضافه می‌کنه."""
    name = "hello"

    def register(self):
        bot, auth, safe = self.bot, self.auth, self.safe

        @bot.message_handler(commands=["hello"])
        @auth
        @safe
        def cmd_hello(message):
            name = message.from_user.first_name or "there"
            bot.reply_to(message, f"👋 Hello {name}!")

        @bot.message_handler(commands=["echo"])
        @auth
        @safe
        def cmd_echo(message):
            text = " ".join(message.text.split()[1:]) or "say something!"
            bot.reply_to(message, f"🔊 {text}")


def run_with_custom_module():
    """اضافه کردن ماژول اختصاصی به رجیستری."""
    from owlbot.modules import MODULE_REGISTRY

    # ثبت ماژول سفارشی توی رجیستری
    MODULE_REGISTRY["hello"] = HelloModule

    bot = OwlBot(
        token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
        authorized_users=[123456789],
        modules=["hello", "system"],
    )
    bot.run()


# ── روش پنجم: استفاده به صورت async-like با callback ─────────

def run_headless():
    """بدون ماژول — فقط یک لاگ ساده از uptime."""
    import time

    bot = OwlBot(
        token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
        authorized_users=[123456789],
        modules=[],  # بدون ماژول — فقط API پایه
        log_level="INFO",
    )
    bot.run()


# ── مثال ترکیبی کامل ─────────────────────────────────────────

if __name__ == "__main__":
    print("""
    🦉 OwlBot — مثال استفاده به عنوان کتابخونه

    کتابخونه‌ی owlbot-remote با طراحی ماژولار و DI-core
    ساخته شده. می‌تونی:
     • ماژول‌های پیش‌فرض رو بارگیری کنی
     • ماژول سفارشی خودت رو بنویسی
     • BotConfig رو مستقیم تنظیم کنی
     • platform های جدید اضافه کنی

    برای شروع فقط دو تا چیز لازم داری:
      ۱. توکن بات از @BotFather
      ۲. آیدی عددی تلگرامت (با @userinfobot ببین)

    نصب:
        pip install owlbot-remote[all]
    """)

    # ── Uncomment یکی از خط‌های زیر ──
    # run_basic_bot()
    # run_advanced_bot()
    # run_with_custom_module()
    # run_headless()

"""
minimum_example.py — حداقل کد برای اجرای OwlBot

نصب:
    pip install owlbot-remote[all]

اجرا:
    python minimum_example.py
"""
from owlbot import OwlBot

bot = OwlBot(
    token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
    authorized_users=[123456789],
    modules=["system", "screen", "files", "processes", "monitoring"],
    log_level="INFO",
)

if __name__ == "__main__":
    bot.run()

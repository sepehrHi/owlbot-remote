**زبان:** فارسی — این «اسکیل» شخصی من (Claude) برای چک‌کردن و اصلاح کد OwlBot
است. منابع: docs.python.org، devguide.python.org (Contributing)،
packaging.python.org و tutorials/packaging-projects.

## 1) چک‌لیست PEP 8 (سبک کد)
- 4 فاصله ایندنت، بدون تب.
- طول خط: پروژه `flake8 max-line-length=127` دارد → رعایت شود.
- نام‌گذاری: ماژول/تابع/متغیر `snake_case`، کلاس `PascalCase`، ثابت `UPPER_CASE`.
- ترتیب import: stdlib → third-party → داخلی پروژه، با یک خط خالی جدا.
- بدون کد مرده/متغیر تعریف‌شده و بلااستفاده.
- مقایسه با `is None` نه `== None`؛ از `except Exception` عام فقط با لاگ‌کردن.

## 2) چک‌لیست PEP 257 / Type Hints
- هر ماژول، کلاس و تابع عمومی باید docstring داشته باشد.
- از `from __future__ import annotations` + type hints استفاده شود (پروژه
  همین‌طور است).
- `Optional[X]` برای مقادیر قابل None.

## 3) devguide.python.org — Contributing
- هر تغییر رفتاری باید تست داشته باشد.
- خطاها نباید بی‌صدا قورت داده شوند؛ باید لاگ یا raise شوند.
- کد باید قابل اجرا روی نسخه‌های پایتون اعلام‌شده در `pyproject.toml` باشد
  (این‌جا `>=3.11`).

## 4) packaging.python.org / Packaging Tutorial
- ساختار `src/` layout (پروژه همین را دارد: `src/owlbot`).
- `tests/` باید در ریشه‌ی پروژه (کنار `src/`) باشد، نه داخل پکیج نصب‌شونده.
- `pyproject.toml` منبع واحد متادیتا (PEP 621) — تأیید شد، `setup.py` فقط shim.
- وابستگی‌های dev (`pytest`, `pytest-cov`, `flake8`) در `[project.optional-dependencies.dev]`.

## 5) مشکلاتی که در این ریویو پیدا و درست شد
- `config/__init__.py`: منطق `__post_init__` تکراری/معکوس بود و متغیر
  `_WIN_ONLY_MODULES` تعریف می‌شد ولی هرگز استفاده نمی‌شد (کد مرده) → ساده و
  یکپارچه شد.
- امکان خاموش‌کردن کامل لاگ یا جلوگیری از ساخت فایل لاگ وجود نداشت
  (`FileHandler` همیشه ساخته می‌شد) → اضافه شد: `log_file=None` یا
  `enable_logging=False`.
- پوشه‌ی `tests/` اصلاً وجود نداشت → کامل ساخته شد (`test_config.py`,
  `test_bot.py`, `test_utils.py`, `conftest.py`).
- بخش امنیت (validation ورودی‌های خطرناک و ...) طبق خواسته‌ی کاربر فعلاً
  دست‌نخورده ماند.

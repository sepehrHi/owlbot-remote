# Changelog

همه‌ی تغییرات قابل‌توجه این پروژه در این فایل مستند می‌شود.
فرمت بر اساس [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) است و
این پروژه از [Semantic Versioning](https://semver.org/) پیروی می‌کند.

## [1.0.0-beta.0] - 2026-07-07

### ✨ اولین انتشار عمومی (First public release)

نسخه‌ی اول OwlBot به‌عنوان یک پکیج استاندارد و قابل‌نصب پایتون.

### Added
- ساختار پروژه به الگوی استاندارد `src/` طبق راهنمای بسته‌بندی پایتون
  (`src/owlbot/...`).
- `pyproject.toml` مطابق PEP 621 به‌عنوان تنها منبع متادیتای پکیج؛
  `setup.py` صرفاً به‌عنوان shim نگه داشته شد.
- بسته‌بندی ماژولار (`system`, `screen`, `audio`, `files`, `input`,
  `processes`, `monitoring`, `network`) با قابلیت انتخاب زیرمجموعه از طریق
  extras (`[ui]`, `[windows]`, `[all]`, `[dev]`).
- سیستم لاگ کاملاً قابل‌تنظیم:
  - `log_level` با اعتبارسنجی مقدار.
  - `log_file` قابل غیرفعال‌سازی (`None`/`""`) برای جلوگیری از ساخت فایل لاگ.
  - `enable_logging=False` برای خاموش‌کردن کامل لاگ (نه کنسول، نه فایل).
  - پرچم‌های معادل در CLI: `--log-level`, `--log-file`, `--no-log-file`,
    `--disable-logging`.
- مجموعه‌ی کامل تست (`tests/`) با `pytest` — پوشش `config`, `core.bot`,
  `core.utils`, و CLI؛ بدون تماس شبکه‌ای واقعی.
- پیکربندی `flake8` واقعی (`.flake8`) — قبلاً بخش `[tool.flake8]` داخل
  `pyproject.toml` توسط flake8 خام خوانده نمی‌شد.
- مستندسازی استانداردهای کدنویسی پروژه در `docs/PYTHON_STANDARDS_SKILL.md`.
- بخش‌های «Logging» و «Testing» به `README.md` اضافه شد.
- ورک‌فلوهای GitHub Actions برای CI (لینت + build) و انتشار خودکار روی PyPI
  هنگام publish شدن یک Release.

### Fixed
- منطق تکراری/معکوس در `BotConfig.__post_init__` که شامل یک متغیر مرده
  (`_WIN_ONLY_MODULES`، هرگز استفاده‌نشده) بود، ساده و یکپارچه شد.
- فیلتر صحیح ماژول‌های ویژه‌ی ویندوز (`audio`, `input`) روی پلتفرم‌های غیر
  ویندوزی.
- اشاره‌ی اشتباه به مسیر `platforms/telegram.py` (جمع) در README اصلاح شد
  به مسیر واقعی `platform/telegram.py` (مفرد).
- حذف import بلااستفاده (`typing.List`) در `platform/telegram.py`.

### Security
- بخش سخت‌گیری‌های امنیتی (اعتبارسنجی عمیق ورودی، rate limiting و ...) در
  این نسخه به‌طور آگاهانه به نسخه‌های بعدی موکول شده است.

[1.0.0-beta.0]: https://github.com/sepehrHi/OwlBot/releases/tag/v1.0.0-beta.0

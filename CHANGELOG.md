# Changelog

همه‌ی تغییرات قابل‌توجه این پروژه در این فایل مستند می‌شود.
فرمت بر اساس [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) است و
این پروژه از [Semantic Versioning](https://semver.org/) پیروی می‌کند.

## [1.0.3] - 2026-07-20

### ✨ Fourth release — real GPS-based live location

### Added
- دو دستور جدید در ماژول `ip` (`src/owlbot/modules/ip.py`):
  - **`/gpslive <seconds>`** (۶۰ تا ۸۶۴۰۰ ثانیه) — برخلاف `/locationlive`
    که مبتنی بر IP و کاملاً ثابت است، این دستور یک **ردیابی زنده‌ی واقعی**
    راه می‌اندازد:
    1. ابتدا یک فیکس GPS واقعی از طریق `System.Device.Location.GeoCoordinateWatcher`
       (Windows Location Services) می‌گیرد و با `bot.send_location(...,
       live_period=seconds)` یک پیام live-location در تلگرام می‌فرستد.
    2. یک ترد پس‌زمینه (`daemon=True`، همان الگوی `MonitoringModule`)
       هر **۱۵ ثانیه** (`_GPS_LIVE_POLL_SECONDS`) دوباره GPS را poll
       می‌کند و با `bot.edit_message_live_location(...)` **همان پیام** را
       در جا آپدیت می‌کند — یعنی اگر دستگاه (مثلاً لپ‌تاپ) واقعاً جابه‌جا
       شود، پین روی نقشه هم دنبالش می‌رود.
    3. اگر در لحظه‌ی شروع GPS واقعی در دسترس نباشد (مجوز رد شده یا سرویس
       غیرفعال)، به‌صورت خودکار یک پین **غیر لایو** مبتنی بر IP (همان
       منطق fallback موجود در `/gps`) ارسال می‌شود؛ در طول اجرا هم اگر یک
       poll خاص فیکس نگیرد، آخرین موقعیت شناخته‌شده حفظ می‌شود (به‌جای قطع
       ردیابی).
    4. با پایان زمان تعیین‌شده یا فراخوانی `/stopgpslive`، ترد متوقف و
       `bot.stop_message_live_location(...)` فراخوانی می‌شود.
  - **`/stopgpslive`** — توقف زودهنگام یک نشست فعال `/gpslive` (پیام خطای
    مناسب می‌دهد اگر نشست فعالی وجود نداشته باشد).
- وضعیت نشست لایو (`_gps_live_active: bool`, `_gps_live_thread: threading.Thread | None`)
  به‌عنوان state روی نمونه‌ی `IPModule` نگه‌داری می‌شود (دقیقاً همان الگوی
  `_active`/`_thread` در `MonitoringModule`)، نه global state، تا هر
  instance از بات مستقل بماند.
- ۱ تست واحد جدید (`test_init_gps_live_state_is_idle`) برای بررسی وضعیت
  اولیه‌ی idle این state.

### Changed
- `/help` (`core/help.py`)، `README.md` (بولت فیچرها + جدول ماژول‌ها) و
  `docs/MODULES.md` (بخش کامل ماژول IP & Location) با دو دستور جدید و
  توضیح تفاوت `/locationlive` (IP-based، ثابت) در برابر `/gpslive`
  (GPS واقعی، لایو و به‌روزرسانی‌شونده) به‌روزرسانی شدند.

## [1.0.2] - 2026-07-19

### ✨ Third release — IP & Location module

### Added
- ماژول جدید `ip` با ۶ دستور:
  - `/myip` — نمایش IP عمومی + همه‌ی IP‌های محلی دستگاه
  - `/iplookup [ip]` — اطلاعات جغرافیایی/ISP برای خود سیستم یا یک IP/هاست دلخواه (از طریق `ip-api.com`)
  - `/vpncheck` — تشخیص هیوریستیک VPN/پروکسی/IP دیتاسنتری
  - `/location` — ارسال پین موقعیت مکانی تقریبی (بر پایه‌ی IP) روی نقشه‌ی تلگرام
  - `/gps` — تلاش برای گرفتن فیکس واقعی GPS از طریق Windows Location Services، با fallback خودکار به موقعیت مبتنی بر IP
  - `/locationlive <sec>` — ارسال Live Location تلگرام برای مدت مشخص
- ۱۵ تست واحد جدید برای توابع خالص ماژول `ip` (بدون تماس شبکه‌ی واقعی)
- بخش «Disclaimer» در انتهای `README.md`: این کتابخانه برای راحتی و مدیریت
  دستگاه‌های خودتان ارائه شده؛ هرگونه استفاده‌ی نادرست بر عهده‌ی کاربر است
  و به سازنده مربوط نیست.

### Changed
- `AVAILABLE_MODULES` و رجیستری ماژول‌ها برای شامل‌شدن `ip` به‌روزرسانی شد.
- هِلپ داینامیک (`/help`) و `docs/MODULES.md` و `README.md` با بخش کامل ماژول `ip` به‌روزرسانی شدند.

## [1.0.1] - 2026-07-18

### ✨ Second release — Animations & Polish

### Added
- انیمیشن (پیام "در حال پردازش…" با ادیت خودکار) برای دستورات مهم: `/status`, `/uptime`, `/webcam`, `/ffmpeg_install`, `/netcheck`, `/screenshot`, `/wifiscan`
- دانلود FFmpeg با timeout و retry خودکار (۳ بار تلاش با backoff)
- لینک دانلود FFmpeg از `https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip` (جایگزین لینک BtbN latest)

### Changed
- متد `register` در `SystemModule` به توابع کمکی `_build_status_text()` و `_build_uptime_text()` تفکیک شد (رفع C901)
- تابع `_download_with_retry` با retry و timeout به `ffmpeg.py` اضافه شد
- به‌روزرسانی README.md و مستندات

### Fixed
- لینک FFmpeg از `latest` به release مشخص تغییر کرد (Gyan.dev essentials build)
- `flake8 W605` در docstring (بک‌اسلش‌های escape)
- وظایف issue #1: بررسی لینک دانلود FFmpeg

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

[1.0.3]: https://github.com/sepehrHi/OwlBot/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/sepehrHi/OwlBot/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/sepehrHi/OwlBot/compare/v1.0.0-beta.0...v1.0.1
[1.0.0-beta.0]: https://github.com/sepehrHi/OwlBot/releases/tag/v1.0.0-beta.0

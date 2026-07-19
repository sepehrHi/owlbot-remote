## 🦉 OwlBot v1.0.3 — Real GPS-Based Live Location

> **PEP 440 version:** `1.0.3` · **Requires:** Python ≥ 3.11 · **OS:** Windows (core modules are cross‑platform)

A focused feature release: `/gpslive` brings *genuinely* live, auto-updating GPS tracking to the `ip` module — a real complement to the static, IP-based `/locationlive` added in v1.0.2.

نسخه‌ی چهارم OwlBot — دستور `/gpslive` یک ردیابی زنده و واقعی مبتنی بر GPS به ماژول `ip` اضافه می‌کند؛ مکملی واقعی برای `/locationlive` که ثابت و مبتنی بر IP بود.

---

### 🆕 Added · اضافه‌شده‌ها

- **`/gpslive <seconds>`** (60–86400s):
  - Takes an initial **real GPS fix** via Windows Location Services (`System.Device.Location.GeoCoordinateWatcher`) and sends a Telegram live-location message.
  - A background daemon thread re-polls the GPS fix **every 15 seconds** and updates that *same* message in place via `edit_message_live_location` — the pin actually follows the device if it moves (e.g. a laptop), unlike `/locationlive`'s static IP-based pin.
  - If no real GPS fix is available at start (permission denied, service disabled, or non-Windows), it automatically falls back to a single, non-live IP-based pin — the same fallback logic already used by `/gps`.
  - If a single poll during tracking fails to get a fix, the last known position is kept (tracking isn't aborted over one missed poll).
  - Stops cleanly — via `stop_message_live_location` — when the timer runs out or `/stopgpslive` is called.
- **`/stopgpslive`** — stop an active `/gpslive` session early; replies with a clear message if no session is running.
- New unit test (`test_init_gps_live_state_is_idle`) verifying the module starts with no live-tracking session active.

### 🛠️ Changed · تغییرات

- `/help`, `README.md` (features + module table), and `docs/MODULES.md` updated with both new commands and an explicit note on how `/gpslive` (real, live, auto-updating) differs from `/locationlive` (IP-based, static).

---

### 📥 Installation · نصب

```bash
pip install owlbot_remote-1.0.3-py3-none-any.whl
# or, from source:
pip install -e .
```

### 🧪 Verify it yourself · خودتان تأیید کنید

```bash
pip install -e ".[dev]"
pytest -v            # 60 tests
flake8 src tests      # 0 issues
```

### ⚠️ Privacy note

`/gpslive`, like every command in the `ip` module, reveals the device's
real-time physical location while active. It is gated by the same
`authorized_users` allowlist as every other OwlBot command — see the
Disclaimer in `README.md`.

---

**Full diff:** https://github.com/sepehrHi/OwlBot/compare/v1.0.2...v1.0.3

[1.0.3]: https://github.com/sepehrHi/OwlBot/releases/tag/v1.0.3

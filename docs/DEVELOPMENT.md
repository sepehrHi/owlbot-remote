# 🛠️ Development Guide

Guide for contributing to OwlBot — setup, testing, code style, and release process.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Git
- FFmpeg (for media features)
- Windows for full module testing

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/sepehrHi/OwlBot.git
cd OwlBot

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install in development mode with all extras
pip install -e .[dev,all]

# Verify installation
pytest -v
flake8 src tests
owlbot --help
```

---

## 📁 Project Structure

```
OwlBot/
├── src/
│   └── owlbot/
│       ├── __init__.py          # Package exports, version
│       ├── __main__.py          # CLI entry point
│       ├── config/              # Configuration
│       │   └── __init__.py      # BotConfig, constants
│       ├── core/                # Core bot logic
│       │   ├── __init__.py
│       │   ├── bot.py           # Main OwlBot class
│       │   ├── decorators.py    # @authorized_only, @safe_reply
│       │   ├── help.py          # Dynamic help generator
│       │   └── utils.py         # Shared utilities
│       ├── modules/             # Feature modules
│       │   ├── __init__.py      # Module registry
│       │   ├── base.py          # BaseModule class
│       │   ├── system.py
│       │   ├── screen.py
│       │   ├── audio.py
│       │   ├── files.py
│       │   ├── input.py
│       │   ├── monitoring.py
│       │   ├── network.py
│       │   ├── processes.py
│       │   └── ffmpeg.py
│       └── platform/
│           ├── __init__.py
│           └── telegram.py      # Telegram adapter
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures
│   ├── test_config.py
│   ├── test_bot.py
│   ├── test_cli.py
│   ├── test_utils.py
│   └── test_monitoring.py
├── examples/                    # Example scripts
│   ├── minimum_example.py
│   └── my_owlbot_script.py
├── docs/                        # Documentation
│   ├── GETTING_STARTED.md
│   ├── CONFIGURATION.md
│   ├── MODULES.md
│   ├── API.md
│   ├── SECURITY.md
│   ├── DEVELOPMENT.md
│   └── EXAMPLES.md
├── .github/
│   └── workflows/
│       └── python-package.yml   # CI/CD
├── pyproject.toml               # Project metadata (PEP 621)
├── setup.py                     # Setuptools shim
├── README.md                    # Main readme (English)
├── LICENSE
├── CHANGELOG.md
└── requirements-dev.txt
```

---

## 🧪 Testing

### Run Tests

```bash
# All tests with coverage
pytest --cov=owlbot --cov-report=term-missing

# Specific test file
pytest tests/test_config.py -v

# Specific test
pytest tests/test_config.py::test_config_validation -v

# Watch mode (requires pytest-watch)
ptw tests/
```

### Test Structure

```python
# tests/test_config.py
import pytest
from owlbot.config import BotConfig

def test_config_validation():
    """Invalid token should raise ValueError."""
    with pytest.raises(ValueError, match="token must not be empty"):
        BotConfig(token="", authorized_users=[123])

def test_config_defaults():
    """Defaults should be applied."""
    config = BotConfig(token="123:ABC", authorized_users=[123])
    assert config.log_level == "INFO"
    assert config.log_file == "owlbot.log"
    assert config.enable_logging is True
```

### Fixtures (conftest.py)

OwlBot uses `pyTelegramBotAPI`, which is **synchronous** — there is no
`asyncio`/`AsyncMock` anywhere in this codebase. The actual shared fixtures
currently in `tests/conftest.py` are:

```python
# tests/conftest.py (actual, simplified)
import pytest

@pytest.fixture
def valid_token() -> str:
    """A syntactically valid (but fake) Telegram bot token."""
    return "123456789:AAFakeTokenFakeTokenFakeTokenFakeTok"

@pytest.fixture
def valid_users() -> list:
    """A list with one authorized user id."""
    return [111111111]

@pytest.fixture(autouse=True)
def _reset_owlbot_logging():
    """Give every test a clean 'owlbot' logger (no leaked handlers)."""
    ...
```

Individual test files build their own `BotConfig`/mock `message` objects
locally (see `tests/test_bot.py`, `tests/test_config.py`) rather than
relying on a shared `bot`/`mock_ctx` fixture.

### Mocking External Dependencies

```python
# Mock psutil for cross-platform tests
def test_read_cpu_returns_percentage_string(monkeypatch):
    import psutil
    monkeypatch.setattr(psutil, "cpu_percent", lambda *a, **k: 42.0)
    ...

# Mock a Telegram message (plain object/MagicMock, not AsyncMock — the
# library is synchronous)
from unittest.mock import MagicMock

def make_message(chat_id: int, text: str = "") -> MagicMock:
    message = MagicMock()
    message.chat.id = chat_id
    message.text = text
    return message
```

---

## 🎨 Code Style

### Linting & Type Checking

```bash
# Lint (CI enforces this — see .github/workflows/python-package.yml)
flake8 src tests

# Type checking (advisory in CI, not yet blocking — see [tool.mypy] in pyproject.toml)
mypy src
```

> Note: `black` and `isort` are **not** currently part of this project's
> toolchain (no config, no dev dependency, not run in CI). If you'd like to
> adopt them, add them to `[project.optional-dependencies].dev` in
> `pyproject.toml` and to `.pre-commit-config.yaml` first, then run a
> dedicated formatting-only commit so it doesn't get mixed with logic
> changes.

### Configuration

```ini
# .flake8
[flake8]
max-line-length = 127
max-complexity = 12
exclude = .git,__pycache__,build,dist,.venv,*.egg-info
```

```toml
# pyproject.toml (partial)
[tool.mypy]
python_version = "3.11"
mypy_path = "src"
ignore_missing_imports = true
warn_unused_ignores = true
warn_redundant_casts = true
exclude = ["tests/", "build/", "dist/"]
```

### Style Rules

| Rule | Standard |
|------|----------|
| Indent | 4 spaces |
| Line length | 127 chars |
| Quotes | Double (`"`) |
| Imports | Stdlib → Third-party → Local |
| Type hints | Required for public API |
| Docstrings | Google style (PEP 257) |
| Naming | `snake_case` functions, `PascalCase` classes, `UPPER_CASE` constants |

### Pre-commit Hooks (Optional, not yet set up)

There is no `.pre-commit-config.yaml` in the repo yet. If you want local
pre-commit checks, create one yourself, e.g.:

```bash
pip install pre-commit
```

```yaml
# .pre-commit-config.yaml (example — create this file to enable)
repos:
  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
```

Then run `pre-commit install`.

---

## 📝 Adding a New Module

### 1. Create Module File

```python
# src/owlbot/modules/weather.py
"""Weather module — fetch current weather and forecasts."""
from __future__ import annotations
from owlbot.modules.base import BaseModule
from owlbot.core.decorators import authorized_only, safe_reply
from owlbot.config import BotConfig

class WeatherModule(BaseModule):
    name = "weather"
    description = "Weather information"
    commands = {
        "weather": "Current weather for city",
        "forecast": "3-day forecast",
    }
    
    def __init__(self, bot, config: BotConfig) -> None:
        super().__init__(bot, config)
        self.api_key = config.weather_api_key  # Add to BotConfig
    
    @authorized_only
    @safe_reply
    def cmd_weather(self, ctx):
        """Usage: /weather <city>"""
        city = ctx.args or "Tehran"
        # ... fetch weather ...
        ctx.reply(f"🌤️ {city}: 22°C, Sunny")
    
    @authorized_only
    @safe_reply
    def cmd_forecast(self, ctx):
        """Usage: /forecast <city>"""
        ctx.reply("📅 3-day forecast...")

# Auto-register (optional)
from owlbot.modules import register_module
register_module(WeatherModule)
```

### 2. Add to Module Registry

```python
# src/owlbot/modules/__init__.py
from owlbot.modules.weather import WeatherModule

# Add to AVAILABLE_MODULES
AVAILABLE_MODULES = [
    "system", "screen", "audio", "files",
    "input", "processes", "monitoring",
    "network", "ffmpeg", "weather",  # Add here
]
```

### 3. Add Config (if needed)

```python
# src/owlbot/config/__init__.py
@dataclass
class BotConfig:
    ...
    weather_api_key: str = ""  # New field
    
    def __post_init__(self):
        ...
        if "weather" in self.modules and not self.weather_api_key:
            raise ValueError("weather_api_key required for weather module")
```

### 4. Add Tests

```python
# tests/test_weather.py
import pytest
from owlbot.modules.weather import WeatherModule

def test_weather_module_load(bot):
    module = WeatherModule(bot, bot.config)
    assert module.name == "weather"
    assert "weather" in module.commands
```

### 5. Update Documentation

- Add to `docs/MODULES.md`
- Add commands to `src/owlbot/core/help.py`
- Update `README.md` module table

---

## 🔄 Release Process

### Versioning

Semantic Versioning (SemVer): `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking API changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes

### Release Checklist

This is the actual process the maintainer follows (no manual `twine
upload` — publishing to PyPI is automated via GitHub's trusted OIDC
publishing once a GitHub Release is created).

```bash
# 1. Bump version in BOTH places (they must match)
# pyproject.toml:        version = "1.1.0"
# src/owlbot/__init__.py: __version__ = "1.1.0"

# 2. Update CHANGELOG.md
# ## [1.1.0] - 2026-XX-XX
# ### Added
# - ...
# ...and add the compare link at the bottom:
# [1.1.0]: https://github.com/sepehrHi/OwlBot/compare/v1.0.1...v1.1.0

# 3. Add RELEASE_NOTES_v1.1.0.md (see RELEASE_NOTES_v1.0.1.md for the format)

# 4. Re-sync the local editable install metadata after the version bump
pip install -e ".[dev]"

# 5. Run the same checks CI runs
flake8 src tests --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 src tests --count --exit-zero --statistics
mypy src            # advisory only, does not block release
pytest -v --cov=owlbot --cov-report=term-missing

# 6. Build & sanity-check the distribution
python -m build
twine check dist/*

# 7. Commit, tag, push
git add -A && git commit -m "chore: release v1.1.0"
git push origin main
git tag -a v1.1.0 -m "OwlBot v1.1.0"
git push origin v1.1.0

# 8. Create the GitHub Release (this is what triggers PyPI publishing)
gh release create v1.1.0 dist/owlbot_remote-1.1.0-py3-none-any.whl \
  dist/owlbot_remote-1.1.0.tar.gz \
  --title "OwlBot v1.1.0" \
  --notes-file RELEASE_NOTES_v1.1.0.md

# 9. Confirm it actually reached PyPI
pip index versions owlbot-remote --pre --no-cache-dir
```

### CI/CD Pipeline (actual files)

Two separate workflows, both in `.github/workflows/`:

- **`python-package.yml`** — runs on every push/PR to `main` and on manual
  dispatch. `runs-on: ubuntu-latest`, matrix `python-version: ["3.11",
  "3.12"]` (these are the only two versions declared in `pyproject.toml`
  classifiers — there is no 3.13 support yet). Steps: install
  `-e ".[dev]"` → flake8 (critical errors block the build; full style scan
  is non-blocking) → mypy (advisory, non-blocking) → `pytest -v
  --cov=owlbot`. A second `build` job (needs `test`) runs `python -m
  build` + `twine check` and uploads the `dist/` artifacts.
- **`python-publish.yml`** — triggers only `on: release: published`.
  Builds the distribution again from a clean checkout, runs `twine check`,
  then publishes via `pypa/gh-action-pypi-publish` using **trusted OIDC
  publishing** (`permissions: id-token: write`) — there is no
  `TWINE_PASSWORD`/API-token secret involved, so publishing only ever
  happens by creating a GitHub Release, never by running `twine upload`
  locally.

> ⚠️ PyPI rejects re-uploading a filename that was already published
> (`400 File already exists`). If a publish run fails for that reason, it
> almost always means the version number wasn't bumped, or that release
> was already published successfully before — check PyPI first, don't
> just re-run the workflow.

---

## 🐛 Debugging

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

bot = OwlBot(..., log_level="DEBUG")
```

### Common Issues

| Issue | Solution |
|-------|----------|
| Module not loading | Check `AVAILABLE_MODULES`, dependencies installed |
| Telegram 409 Conflict | Another instance running — use `drop_pending_updates=True` |
| FFmpeg not found | Install FFmpeg, add to PATH |
| Permission denied | Run as Admin (Windows) or check file permissions |
| ImportError | `pip install -e .[all]` in project root |

### Profiling

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

bot.run()

profiler.disable()
stats = pstats.Stats(profiler).sort_stats('cumulative')
stats.print_stats(20)
```

---

## 📋 Contribution Guidelines

### Before Contributing

1. Check existing issues/PRs
2. Open an issue for discussion (features/bugs)
3. Fork and create feature branch

### Pull Request Checklist

- [ ] Tests pass (`pytest`)
- [ ] Lint passes (`flake8 src tests`)
- [ ] Type check passes (`mypy src`)
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped (if applicable)

### Code Review Criteria

- Correctness & edge cases
- Test coverage
- Code style consistency
- Performance impact
- Security implications
- Documentation completeness

---

## 📚 Related Docs

- [API Reference](API.md)
- [Module Reference](MODULES.md)
- [Configuration](CONFIGURATION.md)
- [Security](SECURITY.md)
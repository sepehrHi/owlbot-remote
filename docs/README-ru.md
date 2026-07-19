# 🦉 OwlBot — Агент модульного удаленного управления Windows через Telegram

**OwlBot** — это готовый к продакшену модульный агент удаленного управления для **Windows**, управляемый через **Telegram**. Он позволяет отслеживать системные ресурсы, управлять файлами, контролировать периферию, захватывать экран/веб-камеру и многое другое — всё с вашего телефона.

---

## ✨ Особенности

- 🧩 **100% Модульный** — загружайте только нужные модули
- 💉 **Ядро с внедрением зависимостей** — готово к дополнительным платформам (Discord, SSH, …)
- 🛡️ **Белый список User-ID** и централизованная обработка ошибок
- 📊 **Мониторинг ресурсов в реальном времени** (CPU, RAM, Диск, температура)
- 🎹 **Управление периферией** — клавиатура, мышь, горячие клавиши, громкость
- 📸 **Захват экрана, веб-камера, таймлапс и стриминг экрана**
- 🔊 **Запись голоса, регулировка громкости и воспроизведение входящих голосовых сообщений**
- 🌍 **IP lookup, VPN/proxy detection, and GPS/IP-based location** (Telegram map pin)
- 🌍 **IP lookup, VPN/proxy detection, and GPS/IP-based location** (Telegram map pin)

---

## 🚀 Быстрый старт

### Требования

- Python **3.11+**
- Windows (некоторые модули требуют Win32 API)
- `ffmpeg` в `PATH` для воспроизведения голоса (скачать с [ffmpeg.org](https://ffmpeg.org/))
- [Токен Telegram-бота](https://t.me/BotFather)

### Установка из PyPI

```bash
# Полная установка со всеми функциями (Windows + кроссплатформенные)
pip install owlbot-remote[all]

# Только кроссплатформенное подмножество (без аудио, клавиатуры, WMI)
pip install owlbot-remote
```

### Минимальный скрипт развертывания

```python
from owlbot import OwlBot

bot = OwlBot(
    token="ВАШ_BOT_TOKEN",
    authorized_users=[123456789],       # ваш Telegram User ID
    modules=["system", "screen", "files", "input", "processes", "monitoring"],
)
bot.run()
```

Или через CLI:

```bash
owlbot --token ВАШ_BOT_TOKEN --users 123456789,987654321
```

---

## 📝 Логирование

По умолчанию OwlBot пишет логи и в консоль, **и** в ротируемый файл (`owlbot.log` в текущей директории). Всё настраиваемо:

```python
from owlbot import OwlBot

bot = OwlBot(
    token="ВАШ_BOT_TOKEN",
    authorized_users=[123456789],
    log_level="DEBUG",       # DEBUG | INFO | WARNING | ERROR | CRITICAL
    log_file="owlbot.log",   # None или "" для отключения файла логов
    enable_logging=True,     # False для полного отключения логирования
)
```

| Цель | Настройка |
|------|-----------|
| Консоль + файл (по умолчанию) | оставить по умолчанию |
| Только консоль, без файла на диске | `log_file=None` |
| Полностью тихий (ни консоль, ни файл) | `enable_logging=False` |

Те же опции доступны через CLI:

```bash
owlbot --token TOKEN --users 123 --log-level DEBUG   # подробное логирование
owlbot --token TOKEN --users 123 --no-log-file        # только консоль, без файла
owlbot --token TOKEN --users 123 --disable-logging    # полностью тихий
```

---

## 🕹️ Доступные модули и команды

| Модуль | Команда | Описание |
|--------|---------|-------------|
| **system** | `/status` | CPU, RAM, Диск, Сеть, Батарея |
| | `/uptime` | Время работы системы |
| | `/ping` | Проверка работоспособности |
| | `/lock` | Блокировка рабочей станции |
| | `/shutdown` | Выключение ПК |
| | `/restart` | Перезагрузка ПК |
| **screen** | `/screenshot` | Скриншот рабочего стола |
| | `/webcam` | Фото с веб-камеры |
| | `/timelapse <s> <n>` | Серия скриншотов |
| | `/startstream` | Начать стриминг экрана |
| | `/stopstream` | Остановить и отправить видео |
| **input** | `/type <текст>` | Ввод текста |
| | `/move <x> <y>` | Перемещение мыши |
| | `/mousepos` | Позиция мыши |
| | `/mouse <действие>` | Клик / скролл / драг |
| | `/hotkey <k1+k2>` | Отправить горячую клавишу |
| | `/msg <текст>` | Показать диалог |
| **audio** | `/mute` / `/unmute` | Вкл/выкл звук |
| | `/volume <0‑100>` | Установить громкость |
| | `/startrec [сек]` | Запись с микрофона |
| | `/stoprec` | Остановить и отправить запись |
| | `/playvoice` | Переключить воспроизведение голоса |
| **files** | `/listdir [путь]` | Список директории |
| | `/getfile <путь>` | Скачать файл |
| | `/hide` / `/show` | Переключить атрибут hidden |
| | `/file copy/move/delete` | Операции с файлами |
| **processes** | `/tasklist` | Список процессов |
| | `/killtask <exe>` | Убить процесс |
| | `/run` / `/cmd` / `/script` | Выполнить команды |
| **monitoring** | `/monitor <cpu\|ram\|disk\|temp>` | Периодические алерты |
| | `/stopmonitor` | Остановить алерты |
| **network** | `/netcheck` | Проверить подключение к интернету |
| | `/wifiscan` | Сканировать Wi‑Fi сети |
| | `/clipboard get\|set` | Читать/писать буфер обмена |
| **ffmpeg** | `/ffmpeg` | Проверить статус FFmpeg |
| | `/ffmpeg_install` | Скачать и установить FFmpeg |
| **ip** | `/myip` | Публичный + локальный IP-адрес |
| | `/iplookup [ip]` | Гео/ISP-поиск (свой или указанный IP) |
| | `/vpncheck` | Обнаружить VPN/прокси/хостинг IP |
| | `/location` | Отправить пин местоположения по IP |
| | `/gps` | Реальный GPS (Windows), запасной IP |
| | `/locationlive <sec>` | Живое местоположение на N секунд |

---

## 📂 Структура проекта

```
owlbot/
├── __init__.py           # Экспорты пакета и версия
├── config/               # Dataclass BotConfig
├── core/
│   ├── bot.py            # Основной движок OwlBot
│   ├── decorators.py     # @authorized_only / @safe_reply
│   └── utils.py          # Общие утилиты
├── modules/
│   ├── base.py           # Интерфейс BaseModule
│   ├── system.py         # Управление системой
│   ├── screen.py         # Экран/веб-камера/стрим
│   ├── files.py          # Операции с файлами
│   ├── processes.py      # Управление процессами
│   ├── input.py          # Клавиатура/мышь (Windows)
│   ├── audio.py          # Управление аудио (Windows)
│   ├── monitoring.py     # Мониторинг ресурсов
│   ├── network.py        # Wi‑Fi / буфер обмена
│   └── ip.py             # IP lookup, VPN check, GPS/IP location
└── platform/
    └── telegram.py       # Адаптер Telegram
```

---

## 🧪 Тестирование

Тестовый набор использует `pytest` и не делает реальных сетевых/Telegram вызовов.

```bash
pip install -e .[dev]
pytest -v
```

Lint (соответствует CI, конфиг в `.flake8`):

```bash
flake8 src tests
```

---

## 🔧 Дополнения установки

| Extra | Включает |
|-------|----------|
| `owlbot-remote[ui]` | `pyautogui`, `opencv‑python`, `numpy` |
| `owlbot-remote[windows]` | `wmi`, `pycaw`, `keyboard`, `pywifi`, `pyaudio` |
| `owlbot-remote[all]` | Всё выше |
| `owlbot-remote[dev]` | Инструменты Dev/CI (`build`, `flake8`, `pytest`) |

---

## 📄 Лицензия

Распространяется под **лицензией MIT**. См. `LICENSE` для деталей.

---

---

## 📚 Documentation

All guides and API references are in the [`docs/`](docs/) directory (English only):

| Guide | Description |
|-------|-------------|
| [Getting Started](docs/GETTING_STARTED.md) | Installation, configuration, quick start |
| [Configuration](docs/CONFIGURATION.md) | Complete configuration reference |
| [Modules](docs/MODULES.md) | All modules, commands, and features |
| [API Reference](docs/API.md) | Python API reference |
| [Security](docs/SECURITY.md) | Security best practices |
| [Development](docs/DEVELOPMENT.md) | Contributing, testing, releasing |
| [Examples](docs/EXAMPLES.md) | Usage examples and patterns |
| [Documentation Index](docs/INDEX.md) | Full documentation index |

### 🌐 Translations (README only)

All technical docs are English-only. README translations are in [`docs/`](docs/):

| Language | File |
|----------|------|
| 🇮🇷 Persian/Farsi | [README-fa.md](docs/README-fa.md) |
| 🇪🇸 Spanish | [README-es.md](docs/README-es.md) |
| 🇮🇹 Italian | [README-it.md](docs/README-it.md) |
| 🇩🇪 German | [README-de.md](docs/README-de.md) |
| 🇨🇳 Chinese (Simplified) | [README-zh.md](docs/README-zh.md) |
| 🇫🇷 French | [README-fr.md](docs/README-fr.md) |
| 🇷🇺 Russian | [README-ru.md](docs/README-ru.md) |
| 🇯🇵 Japanese | [README-ja.md](docs/README-ja.md) |
| 🇳🇱 Dutch | [README-nl.md](docs/README-nl.md) |
| 🇹🇷 Turkish | [README-tr.md](docs/README-tr.md) |
| 🇰🇷 Korean | [README-ko.md](docs/README-ko.md) |

---

## ⚠️ Disclaimer

This library is provided for your own convenience — to remotely manage
**your own** devices that you own or are explicitly authorized to
administer. It is not intended for surveillance, monitoring, or control
of any device or person without their knowledge and consent.

Any misuse of this library (including unauthorized access to systems you
do not own, tracking or monitoring individuals without consent, or any
illegal activity) is solely the responsibility of the user. The author
and maintainer(s) are not liable for any misuse, damages, or legal
consequences arising from the use of this software. Use responsibly and
in accordance with the laws of your jurisdiction.

---

*Поддерживается **Sepehr H.I** 🦉*
# 🦉 OwlBot — Modulaire Telegram remote control agent voor Windows

**OwlBot** is een productie-klaar, modulair remote-control agent voor **Windows**, bediend via **Telegram**. Hiermee bewaak je systeembronnen, beheer je bestanden, controleer je randapparaten, maak je scherm/webcam-opnames en meer — allemaal vanuit je telefoon.

---

## ✨ Functies

- 🧩 **100% Modulair** — laad alleen de modules die je nodig hebt
- 💉 **Dependency-injection kernel** — klaar voor extra platforms (Discord, SSH, …)
- 🛡️ **Gebruikers-ID whitelist** en gecentraliseerde foutafhandeling
- 📊 **Live resource monitoring** (CPU, RAM, Schijf, temperatuur)
- 🎹 **Randapparaatbesturing** — toetsenbord, muis, sneltoetsen, audio-volume
- 📸 **Schermopname, webcam, timelapse en scherm-streaming**
- 🔊 **Spraakopname, volumeregeling en weergave van inkomende spraak**
- 🌍 **IP lookup, VPN/proxy detection, and GPS/IP-based location** (Telegram map pin)
- 🌍 **IP lookup, VPN/proxy detection, and GPS/IP-based location** (Telegram map pin)

---

## 🚀 Snelstart

### Vereisten

- Python **3.11+**
- Windows (sommige modules vereisen Win32 API)
- `ffmpeg` in `PATH` voor spraakafspelen (download van [ffmpeg.org](https://ffmpeg.org/))
- Een [Telegram Bot Token](https://t.me/BotFather)

### Installatie via PyPI

```bash
# Volledige installatie met alle functies (Windows + cross-platform)
pip install owlbot-remote[all]

# Alleen cross-platform subset (geen audio, geen toetsenbord, geen WMI)
pip install owlbot-remote
```

### Minimaal deploy-script

```python
from owlbot import OwlBot

bot = OwlBot(
    token="JOUW_BOT_TOKEN",
    authorized_users=[123456789],       # jouw Telegram gebruikers-ID
    modules=["system", "screen", "files", "input", "processes", "monitoring"],
)
bot.run()
```

Of via de CLI entry-point:

```bash
owlbot --token JOUW_BOT_TOKEN --users 123456789,987654321
```

---

## 📝 Logging

Standaard logt OwlBot zowel naar de console **als** naar een draaiend logbestand (`owlbot.log` in de huidige map). Alles is configureerbaar:

```python
from owlbot import OwlBot

bot = OwlBot(
    token="JOUW_BOT_TOKEN",
    authorized_users=[123456789],
    log_level="DEBUG",       # DEBUG | INFO | WARNING | ERROR | CRITICAL
    log_file="owlbot.log",   # None of "" om bestand-logging uit te schakelen
    enable_logging=True,     # False om logging volledig uit te schakelen
)
```

| Doel | Instelling |
|------|----------|
| Console + bestand (standaard) | standaard laten |
| Alleen console, geen bestand op schijf | `log_file=None` |
| Volledig stil (geen console, geen bestand) | `enable_logging=False` |

Deze opties zijn ook via CLI beschikbaar:

```bash
owlbot --token TOKEN --users 123 --log-level DEBUG   # gedetailleerd loggen
owlbot --token TOKEN --users 123 --no-log-file        # alleen console, geen bestand
owlbot --token TOKEN --users 123 --disable-logging    # volledig stil
```

---

## 🕹️ Beschikbare modules & commando's

| Module | Commando | Beschrijving |
|--------|---------|-------------|
| **system** | `/status` | CPU, RAM, Schijf, Netwerk, Batterij |
| | `/uptime` | Systeem uptime |
| | `/ping` | Health-check |
| | `/lock` | Werkstation vergrendelen |
| | `/shutdown` | PC uitschakelen |
| | `/restart` | PC herstarten |
| **screen** | `/screenshot` | Bureaublad vastleggen |
| | `/webcam` | Webcam foto maken |
| | `/timelapse <s> <n>` | Reeks screenshots |
| | `/startstream` | Scherm-streaming starten |
| | `/stopstream` | Stoppen & video sturen |
| **input** | `/type <tekst>` | Tekst typen |
| | `/move <x> <y>` | Muis verplaatsen |
| | `/mousepos` | Muispositie opvragen |
| | `/mouse <actie>` | Klik / scroll / sleep |
| | `/hotkey <k1+k2>` | Sneltoets sturen |
| | `/msg <tekst>` | Berichtvenster tonen |
| **audio** | `/mute` / `/unmute` | Dempen aan/uit |
| | `/volume <0‑100>` | Volume instellen |
| | `/startrec [sec]` | Microfoon opnemen |
| | `/stoprec` | Stoppen & opname sturen |
| | `/playvoice` | Inkomende spraakberichten afspelen |
| **files** | `/listdir [pad]` | Map weergeven |
| | `/getfile <pad>` | Bestand downloaden |
| | `/hide` / `/show` | Verborgen attribuut togglen |
| | `/file copy/move/delete` | Bestandsbewerkingen |
| **processes** | `/tasklist` | Draaiende processen lijsten |
| | `/killtask <exe>` | Proces beëindigen |
| | `/run` / `/cmd` / `/script` | Commando's uitvoeren |
| **monitoring** | `/monitor <cpu\|ram\|disk\|temp>` | Periodic alerts |
| | `/stopmonitor` | Stop alerts |
| **network** | `/netcheck` | Check internet connection |
| | `/wifiscan` | Scan Wi‑Fi networks |
| | `/clipboard get\|set` | Read / write clipboard |
| **ffmpeg** | `/ffmpeg` | Check FFmpeg status |
| | `/ffmpeg_install` | Download & install FFmpeg |
| **ip** | `/myip` | Public + local IP addresses |
| | `/iplookup [ip]` | Geo/ISP lookup (self or given IP) |
| | `/vpncheck` | Detect VPN/proxy/hosting IP |
| | `/location` | Send IP-based location pin |
| | `/gps` | Real GPS fix (Windows), IP fallback |
| | `/locationlive <sec>` | Live location for N seconds |

---

## 📂 Projectstructuur

```
owlbot/
├── __init__.py           # Package exports & versie
├── config/               # BotConfig dataclass
├── core/
│   ├── bot.py            # Hoofd OwlBot engine
│   ├── decorators.py     # @authorized_only / @safe_reply
│   └── utils.py          # Gedeelde hulpfuncties
├── modules/
│   ├── base.py           # BaseModule interface
│   ├── system.py         # Systeembesturing
│   ├── screen.py         # Scherm/webcam/stream
│   ├── files.py          # Bestandsbewerkingen
│   ├── processes.py      # Procesbeheer
│   ├── input.py          # Toetsenbord/muis (Windows)
│   ├── audio.py          # Audio-besturing (Windows)
│   ├── monitoring.py     # Resource monitoring
│   ├── network.py        # Wi‑Fi / clipboard
│   └── ip.py             # IP lookup, VPN check, GPS/IP location
└── platform/
    └── telegram.py       # Telegram adapter
```

---

## 🧪 Tests

De testsuite gebruikt `pytest` en doet geen echte netwerk/Telegram-aanroepen.

```bash
pip install -e .[dev]
pytest -v
```

Lint (overeenkomend met CI, config in `.flake8`):

```bash
flake8 src tests
```

---

## 🔧 Installatie-extras

| Extra | Bevat |
|-------|---------|
| `owlbot-remote[ui]` | `pyautogui`, `opencv‑python`, `numpy` |
| `owlbot-remote[windows]` | `wmi`, `pycaw`, `keyboard`, `pywifi`, `pyaudio` |
| `owlbot-remote[all]` | Alles bovenstaande |
| `owlbot-remote[dev]` | Dev/CI tools (`build`, `flake8`, `pytest`) |

---

## 📄 Licentie

Uitgegeven onder de **MIT-licentie**. Zie `LICENSE` voor details.

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

*Onderhouden door **Sepehr H.I** 🦉*
# 🦉 OwlBot — Agente di controllo remoto modulare per Windows via Telegram

**OwlBot** è un agente di controllo remoto modulare pronto per la produzione per **Windows**, gestito tramite **Telegram**. Ti permette di monitorare le risorse di sistema, gestire file, controllare periferiche, catturare schermo/webcam e altro — tutto dal tuo telefono.

---

## ✨ Caratteristiche

- 🧩 **100% Modulare** — carica solo i moduli di cui hai bisogno
- 💉 **Core a iniezione di dipendenze** — pronto per piattaforme extra (Discord, SSH, …)
- 🛡️ **Whitelist User-ID** e gestione errori centralizzata
- 📊 **Monitoraggio risorse live** (CPU, RAM, Disco, temperatura)
- 🎹 **Controllo periferiche** — tastiera, mouse, scorciatoie, volume audio
- 📸 **Cattura schermo, webcam, timelapse e streaming schermo**
- 🔊 **Registrazione vocale, controllo del volume e riproduzione dei messaggi vocali in arrivo**
- 🌍 **IP lookup, VPN/proxy detection, and GPS/IP-based location** (Telegram map pin)
- 🌍 **IP lookup, VPN/proxy detection, and GPS/IP-based location** (Telegram map pin)

---

## 🚀 Avvio rapido

### Prerequisiti

- Python **3.11+**
- Windows (alcuni moduli richiedono Win32 API)
- `ffmpeg` in `PATH` per riproduzione vocale (download da [ffmpeg.org](https://ffmpeg.org/))
- Un [Token Bot Telegram](https://t.me/BotFather)

### Installazione da PyPI

```bash
# Installazione completa con tutte le funzioni (Windows + multi-piattaforma)
pip install owlbot-remote[all]

# Solo sottoinsieme multi-piattaforma (senza audio, tastiera, WMI)
pip install owlbot-remote
```

### Script di deployment minimo

```python
from owlbot import OwlBot

bot = OwlBot(
    token="IL_TUO_BOT_TOKEN",
    authorized_users=[123456789],       # il tuo User ID Telegram
    modules=["system", "screen", "files", "input", "processes", "monitoring"],
)
bot.run()
```

O tramite entry point CLI:

```bash
owlbot --token IL_TUO_BOT_TOKEN --users 123456789,987654321
```

---

## 📝 Logging

Di default OwlBot registra sia su console **che** su file di log rotativo (`owlbot.log` nella directory corrente). Tutto configurabile:

```python
from owlbot import OwlBot

bot = OwlBot(
    token="IL_TUO_BOT_TOKEN",
    authorized_users=[123456789],
    log_level="DEBUG",       # DEBUG | INFO | WARNING | ERROR | CRITICAL
    log_file="owlbot.log",   # None o "" per disabilitare file log
    enable_logging=True,     # False per disabilitare logging completamente
)
```

| Obiettivo | Impostazione |
|----------|------------|
| Console + file (default) | lascia default |
| Solo console, nessun file su disco | `log_file=None` |
| Completamente silenzioso (né console né file) | `enable_logging=False` |

Stesse opzioni via CLI:

```bash
owlbot --token TOKEN --users 123 --log-level DEBUG   # logging verboso
owlbot --token TOKEN --users 123 --no-log-file        # solo console, niente file
owlbot --token TOKEN --users 123 --disable-logging    # completamente silenzioso
```

---

## 🕹️ Moduli e comandi disponibili

| Modulo | Comando | Descrizione |
|--------|---------|-------------|
| **system** | `/status` | CPU, RAM, Disco, Rete, Batteria |
| | `/uptime` | Uptime sistema |
| | `/ping` | Health-check |
| | `/lock` | Blocca workstation |
| | `/shutdown` | Spegni PC |
| | `/restart` | Riavvia PC |
| **screen** | `/screenshot` | Cattura desktop |
| | `/webcam` | Foto webcam |
| | `/timelapse <s> <n>` | Serie screenshot |
| | `/startstream` | Avvia screen streaming |
| | `/stopstream` | Ferma e invia video |
| **input** | `/type <testo>` | Digita testo |
| | `/move <x> <y>` | Sposta mouse |
| | `/mousepos` | Posizione mouse |
| | `/mouse <azione>` | Click / scroll / drag |
| | `/hotkey <k1+k2>` | Invia scorciatoia |
| | `/msg <testo>` | Mostra dialogo |
| **audio** | `/mute` / `/unmute` | Toggle mute |
| | `/volume <0‑100>` | Imposta volume |
| | `/startrec [sec]` | Registra microfono |
| | `/stoprec` | Ferma e invia registrazione |
| | `/playvoice` | Toggle riproduzione messaggi vocali |
| **files** | `/listdir [percorso]` | Lista directory |
| | `/getfile <percorso>` | Scarica file |
| | `/hide` / `/show` | Toggle attributo hidden |
| | `/file copy/move/delete` | Operazioni file |
| **processes** | `/tasklist` | Lista processi in esecuzione |
| | `/killtask <exe>` | Uccidi processo |
| | `/run` / `/cmd` / `/script` | Esegui comandi |
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

## 📂 Struttura del progetto

```
owlbot/
├── __init__.py           # Esportazioni pacchetto e versione
├── config/               # Dataclass BotConfig
├── core/
│   ├── bot.py            # Motore principale OwlBot
│   ├── decorators.py     # @authorized_only / @safe_reply
│   └── utils.py          # Utility condivise
├── modules/
│   ├── base.py           # Interfaccia BaseModule
│   ├── system.py         # Controllo sistema
│   ├── screen.py         # Schermo/webcam/stream
│   ├── files.py          # Operazioni file
│   ├── processes.py      # Gestione processi
│   ├── input.py          # Tastiera/mouse (Windows)
│   ├── audio.py          # Controllo audio (Windows)
│   ├── monitoring.py     # Resource monitoring
│   ├── network.py        # Wi‑Fi / clipboard
│   └── ip.py             # IP lookup, VPN check, GPS/IP location
└── platform/
    └── telegram.py       # Adattatore Telegram
```

---

## 🧪 Test

La suite di test usa `pytest` e non fa chiamate reali di rete/Telegram.

```bash
pip install -e .[dev]
pytest -v
```

Lint (corrisponde a CI, config in `.flake8`):

```bash
flake8 src tests
```

---

## 🔧 Extra di installazione

| Extra | Include |
|-------|---------|
| `owlbot-remote[ui]` | `pyautogui`, `opencv‑python`, `numpy` |
| `owlbot-remote[windows]` | `wmi`, `pycaw`, `keyboard`, `pywifi`, `pyaudio` |
| `owlbot-remote[all]` | Tutto sopra |
| `owlbot-remote[dev]` | Strumenti Dev/CI (`build`, `flake8`, `pytest`) |

---

## 📄 Licenza

Distribuito sotto **Licenza MIT**. Vedi `LICENSE` per dettagli.

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

*Manutenuto da **Sepehr H.I** 🦉*
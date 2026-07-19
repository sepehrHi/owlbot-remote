# 🦉 OwlBot — Agent de contrôle à distance modulaire pour Windows via Telegram

**OwlBot** est un agent de contrôle à distance modulaire prêt pour la production pour **Windows**, opéré via **Telegram**. Il vous permet de surveiller les ressources système, gérer les fichiers, contrôler les périphériques, capturer l'écran/webcam et plus — tout depuis votre téléphone.

---

## ✨ Fonctionnalités

- 🧩 **100 % Modulaire** — chargez uniquement les modules dont vous avez besoin
- 💉 **Cœur à injection de dépendances** — prêt pour plateformes supplémentaires (Discord, SSH, …)
- 🛡️ **Liste blanche d'ID utilisateur** et gestion d'erreurs centralisée
- 📊 **Surveillance des ressources en temps réel** (CPU, RAM, Disque, température)
- 🎹 **Contrôle des périphériques** — clavier, souris, raccourcis, volume audio
- 📸 **Capture d'écran, webcam, timelapse et streaming d'écran**
- 🔊 **Enregistrement vocal, contrôle du volume et lecture des messages vocaux entrants**
- 🌍 **IP lookup, VPN/proxy detection, and GPS/IP-based location** (Telegram map pin)
- 🌍 **IP lookup, VPN/proxy detection, and GPS/IP-based location** (Telegram map pin)

---

## 🚀 Démarrage rapide

### Prérequis

- Python **3.11+**
- Windows (certains modules nécessitent l'API Win32)
- `ffmpeg` dans `PATH` pour la lecture vocale (téléchargement depuis [ffmpeg.org](https://ffmpeg.org/))
- Un [Token de Bot Telegram](https://t.me/BotFather)

### Installation depuis PyPI

```bash
# Installation complète avec toutes les fonctionnalités (Windows + multi-plateforme)
pip install owlbot-remote[all]

# Sous-ensemble multi-plateforme uniquement (pas d'audio, pas de clavier, pas de WMI)
pip install owlbot-remote
```

### Script de déploiement minimal

```python
from owlbot import OwlBot

bot = OwlBot(
    token="VOTRE_BOT_TOKEN",
    authorized_users=[123456789],       # votre ID utilisateur Telegram
    modules=["system", "screen", "files", "input", "processes", "monitoring"],
)
bot.run()
```

Ou via le point d'entrée CLI :

```bash
owlbot --token VOTRE_BOT_TOKEN --users 123456789,987654321
```

---

## 📝 Journalisation

Par défaut, OwlBot journalise à la fois sur la console **et** dans un fichier de log rotatif (`owlbot.log` dans le répertoire courant). Tout est configurable :

```python
from owlbot import OwlBot

bot = OwlBot(
    token="VOTRE_BOT_TOKEN",
    authorized_users=[123456789],
    log_level="DEBUG",       # DEBUG | INFO | WARNING | ERROR | CRITICAL
    log_file="owlbot.log",   # None ou "" pour désactiver le fichier de log
    enable_logging=True,     # False pour désactiver complètement la journalisation
)
```

| Objectif | Réglage |
|--------|---------|
| Console + fichier (défaut) | laisser par défaut |
| Console seulement, pas de fichier sur disque | `log_file=None` |
| Complètement silencieux (ni console, ni fichier) | `enable_logging=False` |

Mêmes options via CLI :

```bash
owlbot --token TOKEN --users 123 --log-level DEBUG   # journalisation verbeuse
owlbot --token TOKEN --users 123 --no-log-file        # console seulement, pas de fichier
owlbot --token TOKEN --users 123 --disable-logging    # complètement silencieux
```

---

## 🕹️ Modules et commandes disponibles

| Module | Commande | Description |
|--------|---------|-------------|
| **system** | `/status` | CPU, RAM, Disque, Réseau, Batterie |
| | `/uptime` | Temps de fonctionnement du système |
| | `/ping` | Vérification de santé |
| | `/lock` | Verrouiller la session |
| | `/shutdown` | Éteindre le PC |
| | `/restart` | Redémarrer le PC |
| **screen** | `/screenshot` | Capturer le bureau |
| | `/webcam` | Photo webcam |
| | `/timelapse <s> <n>` | Série de captures |
| | `/startstream` | Démarrer le streaming |
| | `/stopstream` | Arrêter et envoyer la vidéo |
| **input** | `/type <texte>` | Saisir du texte |
| | `/move <x> <y>` | Déplacer la souris |
| | `/mousepos` | Position de la souris |
| | `/mouse <action>` | Clic / défilement / glisser |
| | `/hotkey <k1+k2>` | Envoyer un raccourci |
| | `/msg <texte>` | Afficher une boîte de dialogue |
| **audio** | `/mute` / `/unmute` | Couper/réactiver le son |
| | `/volume <0‑100>` | Régler le volume |
| | `/startrec [sec]` | Enregistrer le micro |
| | `/stoprec` | Arrêter et envoyer l'enregistrement |
| | `/playvoice` | Basculer lecture messages vocaux |
| **files** | `/listdir [chemin]` | Lister un répertoire |
| | `/getfile <chemin>` | Télécharger un fichier |
| | `/hide` / `/show` | Basculer attribut caché |
| | `/file copy/move/delete` | Opérations sur fichiers |
| **processes** | `/tasklist` | Lister les processus |
| | `/killtask <exe>` | Tuer un processus |
| | `/run` / `/cmd` / `/script` | Exécuter des commandes |
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

## 📂 Structure du projet

```
owlbot/
├── __init__.py           # Exports du paquet et version
├── config/               # Dataclass BotConfig
├── core/
│   ├── bot.py            # Moteur principal OwlBot
│   ├── decorators.py     # @authorized_only / @safe_reply
│   └── utils.py          # Utilitaires partagés
├── modules/
│   ├── base.py           # Interface BaseModule
│   ├── system.py         # Contrôle système
│   ├── screen.py         # Écran/webcam/stream
│   ├── files.py          # Opérations fichiers
│   ├── processes.py      # Gestion processus
│   ├── input.py          # Clavier/souris (Windows)
│   ├── audio.py          # Contrôle audio (Windows)
│   ├── monitoring.py     # Resource monitoring
│   ├── network.py        # Wi‑Fi / clipboard
│   └── ip.py             # IP lookup, VPN check, GPS/IP location
└── platform/
    └── telegram.py       # Adaptateur Telegram
```

---

## 🧪 Tests

La suite de tests utilise `pytest` sans appels réseau/Telegram réels.

```bash
pip install -e .[dev]
pytest -v
```

Lint (correspond à CI, config dans `.flake8`) :

```bash
flake8 src tests
```

---

## 🔧 Extras d'installation

| Extra | Inclut |
|-------|---------|
| `owlbot-remote[ui]` | `pyautogui`, `opencv‑python`, `numpy` |
| `owlbot-remote[windows]` | `wmi`, `pycaw`, `keyboard`, `pywifi`, `pyaudio` |
| `owlbot-remote[all]` | Tout ci-dessus |
| `owlbot-remote[dev]` | Outils Dev/CI (`build`, `flake8`, `pytest`) |

---

## 📄 Licence

Distribué sous **Licence MIT**. Voir `LICENSE` pour détails.

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

*Maintenu par **Sepehr H.I** 🦉*
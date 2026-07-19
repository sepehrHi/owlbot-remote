# 🦉 OwlBot — Telegram üzerinden modüler Windows uzaktan kontrol ajanı

**OwlBot**, **Telegram** üzerinden çalıştırılan **Windows** için üretime hazır, modüler bir uzaktan kontrol ajanıdır. Sistem kaynaklarını izlemenize, dosyaları yönetmenize, çevre birimlerini kontrol etmenize, ekran/webcam yakalamanıza ve daha fazlasına — hepsi telefonunuzdan — olanak tanır.

---

## ✨ Özellikler

- 🧩 **%100 Modüler** — sadece ihtiyacınız olan modülleri yükleyin
- 💉 **Bağımlılık Enjeksiyonlu Çekirdek** — ek platformlar için hazır (Discord, SSH, …)
- 🛡️ **Kullanıcı ID Beyaz Listesi** ve merkezi hata yönetimi
- 📊 **Canlı kaynak izleme** (CPU, RAM, Disk, sıcaklık)
- 🎹 **Çevre birimi kontrolü** — klavye, fare, kısayollar, ses seviyesi
- 📸 **Ekran yakalama, webcam, zamanlayıcı çekim ve ekran yayını**
- 🔊 **Ses kaydı, ses seviyesi kontrolü ve gelen sesli mesaj oynatma**
- 🌍 **IP lookup, VPN/proxy detection, and GPS/IP-based location** (Telegram map pin)
- 🌍 **IP lookup, VPN/proxy detection, and GPS/IP-based location** (Telegram map pin)

---

## 🚀 Hızlı Başlangıç

### Ön Koşullar

- Python **3.11+**
- Windows (bazı modüller Win32 API gerektirir)
- `ffmpeg` `PATH` içinde ses oynatma için ([ffmpeg.org](https://ffmpeg.org/) adresinden indirin)
- Bir [Telegram Bot Token](https://t.me/BotFather)

### PyPI'den Kurulum

```bash
# Tam kurulum (Windows + çapraz platform)
pip install owlbot-remote[all]

# Sadece çapraz platform alt kümesi (ses yok, klavye yok, WMI yok)
pip install owlbot-remote
```

### Minimum Dağıtım Scripti

```python
from owlbot import OwlBot

bot = OwlBot(
    token="BOT_TOKENINIZ",
    authorized_users=[123456789],       # Telegram Kullanıcı ID'niz
    modules=["system", "screen", "files", "input", "processes", "monitoring"],
)
bot.run()
```

Ya da CLI giriş noktası üzerinden:

```bash
owlbot --token BOT_TOKENINIZ --users 123456789,987654321
```

---

## 📝 Loglama

Varsayılan olarak OwlBot hem konsola **hem de** döngülü bir log dosyasına (`geçerli dizinde owlbot.log`) yazar. Her şey yapılandırılabilir:

```python
from owlbot import OwlBot

bot = OwlBot(
    token="BOT_TOKENINIZ",
    authorized_users=[123456789],
    log_level="DEBUG",       # DEBUG | INFO | WARNING | ERROR | CRITICAL
    log_file="owlbot.log",   # None veya "" ile dosya loglamasını devre dışı bırak
    enable_logging=True,     # False ile loglamayı tamamen devre dışı bırak
)
```

| Hedef | Ayar |
|--------|---------|
| Konsol + dosya (varsayılan) | varsayılanı bırakın |
| Sadece konsol, diskte dosya yok | `log_file=None` |
| Tamamen sessiz (ne konsol ne dosya) | `enable_logging=False` |

Aynı seçenekler CLI'den de kullanılabilir:

```bash
owlbot --token TOKEN --users 123 --log-level DEBUG   # ayrıntılı loglama
owlbot --token TOKEN --users 123 --no-log-file        # sadece konsol, dosya yok
owlbot --token TOKEN --users 123 --disable-logging    # tamamen sessiz
```

---

## 🕹️ Kullanılabilir Modüller ve Komutlar

| Modül | Komut | Açıklama |
|--------|---------|-------------|
| **system** | `/status` | CPU, RAM, Disk, Ağ, Batarya |
| | `/uptime` | Sistem uptime süresi |
| | `/ping` | Sağlık kontrolü |
| | `/lock` | Çalışma alanını kilitle |
| | `/shutdown` | PC'yi kapat |
| | `/restart` | PC'yi yeniden başlat |
| **screen** | `/screenshot` | Masaüstü yakala |
| | `/webcam` | Webcam fotoğrafı çek |
| | `/timelapse <s> <n>` | Periyodik ekran görüntüleri |
| | `/startstream` | Ekran yayını başlat |
| | `/stopstream` | Durdur ve video gönder |
| **input** | `/type <metin>` | Metin yaz |
| | `/move <x> <y>` | Fareyi taşı |
| | `/mousepos` | Fare konumu al |
| | `/mouse <eylem>` | Tıkla / kaydır / sürükle |
| | `/hotkey <k1+k2>` | Kısayol gönder |
| | `/msg <metin>` | Mesaj kutusu göster |
| **audio** | `/mute` / `/unmute` | Sessize al / aç |
| | `/volume <0‑100>` | Ses seviyesi ayarla |
| | `/startrec [sn]` | Mikrofon kaydet |
| | `/stoprec` | Durdur ve gönder |
| | `/playvoice` | Gelen ses mesajlarını oyna |
| **files** | `/listdir [yol]` | Dizin listele |
| | `/getfile <yol>` | Dosya indir |
| | `/hide` / `/show` | Gizli özelliği değiştir |
| | `/file copy/move/delete` | Dosya işlemleri |
| **processes** | `/tasklist` | Çalışan süreçleri listele |
| | `/killtask <exe>` | Süreci sonlandır |
| | `/run` / `/cmd` / `/script` | Komutları çalıştır |
| **monitoring** | `/monitor <cpu\|ram\|disk\|temp>` | Periyodik uyarılar |
| | `/stopmonitor` | Uyarıları durdur |
| **network** | `/netcheck` | İnternet bağlantısını kontrol et |
| | `/wifiscan` | Wi-Fi ağlarını tara |
| | `/clipboard get\|set` | Panoya oku/yaz |
| **ffmpeg** | `/ffmpeg` | FFmpeg durumunu kontrol et |
| | `/ffmpeg_install` | FFmpeg'i indir ve kur |
| **ip** | `/myip` | Genel + yerel IP adresleri |
| | `/iplookup [ip]` | Coğrafi/ISP sorgulama (kendi veya verilen IP) |
| | `/vpncheck` | VPN/proxy/hosting IP'sini algıla |
| | `/location` | IP tabanlı konum pimi gönder |
| | `/gps` | Gerçek GPS (Windows), IP yedekleme |
| | `/locationlive <sec>` | N saniye canlı konum |

---

## 📂 Proje Yapısı

```
owlbot/
├── __init__.py           # Paket exportları ve versiyon
├── config/               # BotConfig dataclass
├── core/
│   ├── bot.py            # Ana OwlBot motoru
│   ├── decorators.py     # @authorized_only / @safe_reply
│   └── utils.py          # Paylaşılan yardımcı fonksiyonlar
├── modules/
│   ├── base.py           # BaseModule arayüzü
│   ├── system.py         # Sistem kontrolü
│   ├── screen.py         # Ekran/webcam/yayın
│   ├── files.py          # Dosya işlemleri
│   ├── processes.py      # Süreç yönetimi
│   ├── input.py          # Klavye/fare (Windows)
│   ├── audio.py          # Ses kontrolü (Windows)
│   ├── monitoring.py     # Resource monitoring
│   ├── network.py        # Wi‑Fi / clipboard
│   └── ip.py             # IP lookup, VPN check, GPS/IP location
└── platform/
    └── telegram.py       # Telegram adaptörü
```

---

## 🧪 Testler

Test paketi `pytest` kullanır ve gerçek ağ/Telegram çağrıları yapmaz.

```bash
pip install -e .[dev]
pytest -v
```

Lint (CI ile eşleşir, yapılandırma `.flake8` içinde):

```bash
flake8 src tests
```

---

## 🔧 Kurulum Ekstraları

| Ekstra | İçerir |
|--------|---------|
| `owlbot-remote[ui]` | `pyautogui`, `opencv‑python`, `numpy` |
| `owlbot-remote[windows]` | `wmi`, `pycaw`, `keyboard`, `pywifi`, `pyaudio` |
| `owlbot-remote[all]` | Yukarıdakilerin tümü |
| `owlbot-remote[dev]` | Geliştirme/CI araçları (`build`, `flake8`, `pytest`) |

---

## 📄 Lisans

**MIT Lisansı** altında dağıtılmaktadır. Detaylar için `LICENSE` dosyasına bakın.

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

* **Sepehr H.I** tarafından sürdürülmektedir 🦉*
# 🦉 OwlBot — Telegram経由でWindowsをモジュール式リモート制御するエージェント

**OwlBot** は **Windows** 向けのプロダクションレディなモジュール式リモート制御エージェントで、**Telegram** 経由で操作します。システムリソースの監視、ファイル管理、周辺機器の制御、画面/ウェブカメラのキャプチャなどをスマートフォンから実行できます。

---

## ✨ 特徴

- 🧩 **100% モジュール式** — 必要なモジュールのみをロード
- 💉 **依存性注入コア** — 追加プラットフォーム (Discord, SSH, …) に対応可能
- 🛡️ **ユーザーIDホワイトリスト** と一元化されたエラーハンドリング
- 📊 **リアルタイムリソース監視** (CPU, RAM, ディスク, 温度)
- 🎹 **周辺機器制御** — キーボード, マウス, ホットキー, 音量
- 📸 **画面キャプチャ, ウェブカメラ, タイムラプス, 画面ストリーミング**
- 🔊 **音声録音, 音量制御, 着信ボイスメッセージの再生**
- 🌍 **IP lookup, VPN/proxy detection, and GPS/IP-based location** (Telegram map pin)

---

## 🚀 クイックスタート

### 前提条件

- Python **3.11+**
- Windows (一部モジュールは Win32 API を必要)
- `ffmpeg` を `PATH` に配置 (音声再生用, [ffmpeg.org](https://ffmpeg.org/) からダウンロード)
- [Telegram Bot Token](https://t.me/BotFather)

### PyPIからインストール

```bash
# 全機能付き完全インストール (Windows + クロスプラットフォーム)
pip install owlbot-remote[all]

# クロスプラットフォームのみ (オーディオなし, キーボードなし, WMIなし)
pip install owlbot-remote
```

### 最小デプロイスクリプト

```python
from owlbot import OwlBot

bot = OwlBot(
    token="あなたの_BOT_TOKEN",
    authorized_users=[123456789],       # あなたのTelegramユーザーID
    modules=["system", "screen", "files", "input", "processes", "monitoring"],
)
bot.run()
```

またはCLIエントリーポイント経由:

```bash
owlbot --token あなたの_BOT_TOKEN --users 123456789,987654321
```

---

## 📝 ログ記録

デフォルトではOwlBotはコンソール **と** ローテーションフリーのログファイル (`owlbot.log`, カレントディレクトリ) の両方にログを記録します。全て設定可能です:

```python
from owlbot import OwlBot

bot = OwlBot(
    token="あなたの_BOT_TOKEN",
    authorized_users=[123456789],
    log_level="DEBUG",       # DEBUG | INFO | WARNING | ERROR | CRITICAL
    log_file="owlbot.log",   # None または "" でログファイルのみ無効化
    enable_logging=True,     # False でログ記録を完全無効化
)
```

| 目的 | 設定 |
|------|--------|
| コンソール + ファイル (デフォルト) | デフォルトのまま |
| コンソールのみ, ディスク上にログファイルなし | `log_file=None` |
| 完全サイレント (コンソールなし, ファイルなし) | `enable_logging=False` |

同じオプションがCLIからも利用可能:

```bash
owlbot --token TOKEN --users 123 --log-level DEBUG   # 詳細ログ
owlbot --token TOKEN --users 123 --no-log-file        # コンソールのみ, ファイルなし
owlbot --token TOKEN --users 123 --disable-logging    # 完全サイレント
```

---

## 🕹️ 利用可能なモジュールとコマンド

| モジュール | コマンド | 説明 |
|----------|---------|-------------|
| **system** | `/status` | CPU, RAM, ディスク, ネットワーク, バッテリー |
| | `/uptime` | システム稼働時間 |
| | `/ping` | ヘルスチェック |
| | `/lock` | ワークステーションロック |
| | `/shutdown` | PCシャットダウン |
| | `/restart` | PC再起動 |
| **screen** | `/screenshot` | デスクトップキャプチャ |
| | `/webcam` | ウェブカメラ撮影 |
| | `/timelapse <s> <n>` | 定期スクリーンショット |
| | `/startstream` | 画面ストリーミング開始 |
| | `/stopstream` | 停止して動画送信 |
| **input** | `/type <テキスト>` | テキスト入力 |
| | `/move <x> <y>` | マウス移動 |
| | `/mousepos` | マウス位置取得 |
| | `/mouse <アクション>` | クリック/スクロール/ドラッグ |
| | `/hotkey <k1+k2>` | ホットキー送信 |
| | `/msg <テキスト>` | メッセージボックス表示 |
| **audio** | `/mute` / `/unmute` | ミュート切替 |
| | `/volume <0‑100>` | 音量設定 |
| | `/startrec [秒]` | マイク録音 |
| | `/stoprec` | 停止して送信 |
| | `/playvoice` | 着信ボイス再生切替 |
| **files** | `/listdir [パス]` | ディレクトリ一覧 |
| | `/getfile <パス>` | ファイルダウンロード |
| | `/hide` / `/show` | 隠し属性切替 |
| | `/file copy/move/delete` | ファイル操作 |
| **processes** | `/tasklist` | 実行中プロセス一覧 |
| | `/killtask <exe>` | プロセス終了 |
| | `/run` / `/cmd` / `/script` | コマンド実行 |
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

## 📂 プロジェクト構造

```
owlbot/
├── __init__.py           # パッケージエクスポート & バージョン
├── config/               # BotConfigデータクラス
├── core/
│   ├── bot.py            # メインOwlBotエンジン
│   ├── decorators.py     # @authorized_only / @safe_reply
│   └── utils.py          # 共有ユーティリティ
├── modules/
│   ├── base.py           # BaseModuleインターフェース
│   ├── system.py         # システム制御
│   ├── screen.py         # 画面/ウェブカメラ/ストリーム
│   ├── files.py          # ファイル操作
│   ├── processes.py      # プロセス管理
│   ├── input.py          # キーボード/マウス (Windows)
│   ├── audio.py          # オーディオ制御 (Windows)
│   ├── monitoring.py     # Resource monitoring
│   ├── network.py        # Wi‑Fi / clipboard
│   └── ip.py             # IP lookup, VPN check, GPS/IP location
└── platform/
    └── telegram.py       # Telegramアダプター
```

---

## 🧪 テスト

テストスイートは `pytest` を使用し、実際のネットワーク/Telegram呼び出しは行いません。

```bash
pip install -e .[dev]
pytest -v
```

Lint (CIと一致, 設定は `.flake8`):

```bash
flake8 src tests
```

---

## 🔧 インストールエクストラ

| Extra | 含まれるもの |
|-------|---------|
| `owlbot-remote[ui]` | `pyautogui`, `opencv‑python`, `numpy` |
| `owlbot-remote[windows]` | `wmi`, `pycaw`, `keyboard`, `pywifi`, `pyaudio` |
| `owlbot-remote[all]` | 上記全て |
| `owlbot-remote[dev]` | 開発/CIツール (`build`, `flake8`, `pytest`) |

---

## 📄 ライセンス

**MITライセンス** で配布。詳細は `LICENSE` 参照。

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

*メンテナー: **Sepehr H.I** 🦉*
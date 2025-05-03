# AutoTranscriber

Whisper + FFmpeg で **動画をドラッグ＆ドロップするだけで日本語字幕（.srt）を生成** できる  
Apple Silicon (arm64) macOS 専用デスクトップアプリ。

---

## 特長

- 🤖 ローカル Whisper モデルで高精度文字起こし（通信不要）
- 🖱️ GUI (PySimpleGUI) と 🚀 CLI の両方を提供
- 📊 進捗バー & 経過時間を GUI / CLI 共通で表示
- 🐳 VS Code devcontainer + Docker で開発環境を汚さない
- 📦 PyInstaller ワンコマンドで `.app / .dmg` 作成

---

## ディレクトリ構成

```text
AutoTranscriber/
├── src/                  # アプリ本体
│   ├── main.py           # エントリポイント (CLI ↔ GUI 切替)
│   ├── gui.py            # PySimpleGUI UI
│   ├── transcriber.py    # Whisper 推論 & SRT 生成
│   └── utils/            # ffmpeg ラッパ / パス管理
├── packaging/            # ビルド関連
│   ├── AutoTranscriber.spec   # ← 修正案A: 絶対パス対応
│   ├── build_mac.sh           # ← 修正案B: 直接ビルド
│   └── ffmpeg/ffmpeg          # 静的 arm64 バイナリ
├── .devcontainer/        # VS Code Remote‑Containers 設定
├── assets/               # アプリアイコン・画像
├── requirements.txt
└── README.md
```

# 開発環境セットアップ
# クローン
```
git clone https://github.com/yourname/AutoTranscriber.git
cd AutoTranscriber

# VS Code ➜ 「Reopen in Container」で devcontainer 起動
# 初回ビルド後、依存パッケージが自動インストールされます
```

## テスト & 静的解析
```
pytest                     # 単体テスト
ruff check .               # Lint
mypy src/                  # 型チェック
```

# 使い方
## GUI
```bash
python -m src.main
```
1. ウィンドウに動画ファイルをドロップ
2. 出力先フォルダを選択
3. 文字起こし実行 → movie.srt が生成

## CLI
```bash
python -m src.main --cli path/to/video.mp4 out_dir

```
進捗バー（0–100 %）と経過秒数が表示されます。

# ビルド(macOS)
```bash
brew install pyinstaller        # 初回のみ
./packaging/build_mac.sh         # .app / .dmg が dist/ に出力
```
> このスクリプトはコード署名・公証を行いません。
> Gatekeeper 警告が出たら「右クリック → 開く」で 1 回だけ許可してください。

# ライセンス
```
MIT License © 2025 Hideki Shibata
```
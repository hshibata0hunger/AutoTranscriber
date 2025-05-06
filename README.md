# AutoTranscriber

Flet + Whisper で動画から日本語字幕 **`.srt`** を生成する Apple Silicon (arm64) macOS 用デスクトップアプリです。

---

## 特長

- 🎞️ ドラッグ＆ドロップで `.mp4 / .mov / .mkv` を一発文字起こし  
- 🧠 OpenAI Whisper (openai‑whisper) + PyTorch‐CPU で高精度・無料  
- 🖥️ Flutter ベースのモダン UI (Flet)  
- 🐳 VS Code devcontainer でローカル環境を汚さず開発  
- 📦 `flet pack` + `.venv_build` でワンクリック `.app/.dmg` 生成

---

## ディレクトリ構成

```
AutoTranscriber/
├─ .devcontainer/         # Dockerfile / devcontainer.json
├─ assets/                # アイコンなど
├─ packaging/             # macOS ビルドスクリプト
│   └─ build_mac.sh
├─ src/
│   ├─ main.py            # Flet UI
│   └─ transcriber.py     # Whisper ラッパ
├─ requirements.txt
└─ README.md
```

---

## バージョン構成

| 項目               | バージョン / 備考                     |
| ------------------ | ------------------------------------- |
| **Python (dev)**   | 3.11 (Docker)                         |
| **Python (build)** | 3.12 (Homebrew)                       |
| **Flet**           | 0.17.*                                |
| **Whisper**        | openai‑whisper 2024‑02‑18             |
| **Torch**          | 2.2.1 + cpu (`+cpu` wheel)            |
| **Flutter SDK**    | 3.19 (Homebrew)                       |
| **Xcode CLT**      | 必須（clang / codesign / notarytool） |

---

## 開発（devcontainer）

1. VS Code で本リポジトリを開き **「Reopen in Container」**  
2. コンテナ内で

   ```
   flet run src/main.py   # ホットリロード
   pytest                 # テスト
   ```

   ブラウザ <http://localhost:8550> もしくはネイティブウィンドウで UI を確認できます。

---

## macOS でのビルド

1. 依存インストール（初回のみ）

   ```
   brew install python@3.12 flutter create-dmg
   xcode-select --install
   ```

2. `.app` 生成

   ```
   chmod +x packaging/build_mac.sh
   ./packaging/build_mac.sh
   ```

   成果物： `dist/AutoTranscriber.app`  
   自己利用なら Gatekeeper を解除して起動：

   ```
   xattr -dr com.apple.quarantine dist/AutoTranscriber.app
   open dist/AutoTranscriber.app
   ```

---

## 主要スクリプト

- **`src/transcriber.py`**   Whisper 文字起こし & `.srt` 出力  
- **`packaging/build_mac.sh`**    
  `.venv_build/` を作成 → 依存インストール → `flet pack` → `.app/.dmg` 作成

---

## 今後の拡張アイデア

- `faster-whisper` に切替えて推論高速化  
- YouTube / Vimeo URL 直接入力対応  
- Apple 公証・署名を自動化（`pack_settings.json` に証明書指定）

---

## ライセンス

MIT © 2025 Hideki Shibata

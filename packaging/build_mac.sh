#!/usr/bin/env bash
set -eu

APP_NAME="AutoTranscriber"
SPEC_FILE="packaging/AutoTranscriber.spec"
PY_BUILD_VENV=".venv_build"

# ── 0) プロジェクトルートを環境変数に ─────────────────────────
PROJECT_ROOT="$(cd "$(dirname "$0")/.."; pwd)"
export AUTO_TRANSCRIBER_ROOT="$PROJECT_ROOT"

FFMPEG_BIN="$PROJECT_ROOT/packaging/ffmpeg/ffmpeg"

echo "▶︎ Local macOS build (no codesign / no notarize)"
echo "Project root: $PROJECT_ROOT"
echo "---------------------------------------------"

# ── 1) ffmpeg を用意 ──────────────────────────────────────────
if [ ! -x "$FFMPEG_BIN" ]; then
  echo "⚠️  ffmpeg が無いので取得します..."
  mkdir -p "$(dirname "$FFMPEG_BIN")"
  curl -L -o "$FFMPEG_BIN" \
       https://github.com/yt-dlp/ffmpeg-binaries/releases/latest/download/ffmpeg-mac-arm64
  chmod +x "$FFMPEG_BIN"
fi

# ── 2) PyInstaller venv ─────────────────────────────────────
if [ ! -x "$PY_BUILD_VENV/bin/pyinstaller" ]; then
  python3 -m venv "$PY_BUILD_VENV"
  "$PY_BUILD_VENV/bin/pip" install --quiet pyinstaller
fi
PYI="$PY_BUILD_VENV/bin/pyinstaller"

# ── 3) ビルド実行 ───────────────────────────────────────────
"$PYI" "$SPEC_FILE" --noconfirm

echo "✅ Build completed → $PROJECT_ROOT/dist/${APP_NAME}.app"

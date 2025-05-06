#!/usr/bin/env bash
set -eu
ROOT="$(cd "$(dirname "$0")/.."; pwd)"
VENV="$ROOT/.venv_build"
PY="$(brew --prefix)/opt/python@3.12/bin/python3"
export FLUTTER_ROOT="$(brew --prefix)/opt/flutter"

if [ ! -x "$VENV/bin/python" ]; then
  "$PY" -m venv "$VENV"
fi

"$VENV/bin/pip" install --upgrade pip
"$VENV/bin/pip" install --upgrade \
    flet \
    openai-whisper \
    "torch==2.3.0+cpu" -f https://download.pytorch.org/whl/cpu \
    ffmpeg-python

cd "$ROOT"
"$VENV/bin/flet" pack src/main.py \
    --name AutoTranscriber \
    --icon assets/icon.icns \
    --output dist \
    --target-arch arm64

echo "▶ dist/AutoTranscriber.app 完成"

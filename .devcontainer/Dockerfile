# arm64 イメージは Apple Silicon 上なら自動選択される
FROM python:3.11-slim

ARG DEBIAN_FRONTEND=noninteractive

# OS 依存ライブラリをインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential git ffmpeg tcl tk python3-tk wget curl ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# VS Code の既定ユーザー
RUN useradd -m vscode
USER vscode
WORKDIR /workspace

# ローカルの requirements.txt をイメージにコピー
COPY --chown=vscode:vscode requirements.txt ./

# pip (すでにアップグレード済み) で依存関係をインストール
RUN python3 -m pip install --upgrade pip && pip install setuptools && pip install wheel \
  && python3 -m pip install --no-cache-dir -r requirements.txt \
  && pip uninstall -y PySimpleGUI \
  && pip cache purge \
  && pip install --no-cache-dir --extra-index-url https://PySimpleGUI.net/install PySimpleGUI

ENV PYTHONUNBUFFERED=1 \
  PIP_NO_CACHE_DIR=1 \
  TK_SILENCE_DEPRECATION=1

# .devcontainer/Dockerfile
FROM python:3.11-bookworm

# ---------- system deps (GTK+Flutter runtime) ----------
RUN apt-get update && apt-get install -y --no-install-recommends \
  git unzip xz-utils clang \
  libgtk-3-0 libglib2.0-0 libnss3 libx11-xcb1 libxcomposite1 \
  libxcursor1 libxdamage1 libxext6 libxi6 libxrandr2 libxss1 libxtst6 \
  libatk1.0-0 libatk-bridge2.0-0 libcups2 libdbus-1-3 libdrm2 libgbm1 \
  libpango-1.0-0 libpangocairo-1.0-0 libasound2 && \
  rm -rf /var/lib/apt/lists/*

# ---------- Flutter SDK ----------
ENV FLUTTER_ROOT=/opt/flutter
RUN git clone --depth 1 https://github.com/flutter/flutter.git "$FLUTTER_ROOT" \
  && "$FLUTTER_ROOT/bin/flutter" config --no-analytics
ENV PATH="$FLUTTER_ROOT/bin:$FLUTTER_ROOT/bin/cache/dart-sdk/bin:${PATH}"

# ---------- workspace ----------
WORKDIR /workspace
COPY .. /workspace

# ---------- Python deps (latest) ----------
ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install -U pip && pip install --no-cache-dir -r requirements.txt
#   && pip install --no-cache-dir \
#   flet \
#   openai-whisper \
#   ffmpeg-python
# RUN pip install --no-cache-dir torch==2.3.0 --index-url https://download.pytorch.org/whl/cpu

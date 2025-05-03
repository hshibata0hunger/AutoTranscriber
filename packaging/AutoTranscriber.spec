# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path
block_cipher = None

ROOT = Path(os.environ.get(
    "AUTO_TRANSCRIBER_ROOT",
    "/Users/hideki_mac/開発/プロジェクト/AutoTranscriber",   # デフォルト
)).resolve()

a = Analysis(
    [str(ROOT / "src" / "main.py")],
    pathex=[str(ROOT)],
    binaries=[(str(ROOT / "packaging" / "ffmpeg" / "ffmpeg"), "ffmpeg")],
    datas=[(str(ROOT / "assets" / "icon.icns"), ".")],
    hiddenimports=["tkinterdnd2", "PIL"],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    name='AutoTranscriber',
    icon='assets/icon.icns',
    windowed=True,
    target_arch='arm64',
    console=False,
)

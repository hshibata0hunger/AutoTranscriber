# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path
block_cipher = None

ROOT = Path(os.environ["AUTO_TRANSCRIBER_ROOT"]).resolve()
SRC = ROOT / "src"

a = Analysis(
    [str(SRC / "main.py")],
    pathex=[str(ROOT), str(SRC)],
    binaries=[(str(ROOT / "packaging" / "ffmpeg" / "ffmpeg"), "ffmpeg")],
    datas=[(str(ROOT / "assets" / "icon.icns"), ".")],
    hiddenimports=["tkinterdnd2", "PIL", "tqdm", "whisper"],
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

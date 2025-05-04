# -*- mode: python ; coding: utf-8 -*-
import os, sys
from pathlib import Path

project_root = os.environ['AUTO_TRANSCRIBER_ROOT']

a = Analysis(
    [os.path.join(project_root, 'src', 'main.py')],
    pathex=[project_root],
    binaries=[],
    datas=[
        # ffmpegバイナリを含める
        (os.path.join(project_root, 'packaging', 'ffmpeg', 'ffmpeg'), 'packaging/ffmpeg'),
        # 必要に応じて他のデータファイルを追加
    ],
    hiddenimports=["tkinter", "tkinterdnd2", "PIL", "tqdm", "whisper", "torch"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AutoTranscriber',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(project_root, 'assets', 'icon.icns'),  # アイコンファイルがあれば指定
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AutoTranscriber',
)

app = BUNDLE(
    coll,
    name='AutoTranscriber.app',
    icon=os.path.join(project_root, 'assets', 'icon.icns'),  # アイコンファイルがあれば指定
    bundle_identifier='com.hshibata0hunger.autotranscriber',
    info_plist={
        'NSHighResolutionCapable': 'True',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
    },
)

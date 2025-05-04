from __future__ import annotations
import subprocess
import shutil
from pathlib import Path
from src.utils.paths import project_root


def _find_ffmpeg() -> Path:
    """Homebrew の ffmpeg or 同梱バイナリを返す"""
    hb = shutil.which("ffmpeg")
    if hb:
        return Path(hb)
    bundled = project_root() / "packaging" / "ffmpeg" / "ffmpeg"
    if bundled.exists():
        return bundled
    raise RuntimeError(
        "ffmpeg が見つかりません。Homebrew で `brew install ffmpeg` するか、バンドルしてください。")


def extract_audio(video: Path, out_dir: Path) -> Path:
    wav = out_dir / f"{video.stem}.wav"
    ff = _find_ffmpeg()
    cmd = [str(ff), "-i", str(video), "-ar",
           "16000", "-ac", "1", "-y", str(wav)]
    subprocess.run(cmd, check=True, capture_output=True)
    return wav

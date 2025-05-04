from __future__ import annotations
import time, whisper
from pathlib import Path
from typing import Any, Dict, Callable, cast
from tqdm import tqdm
from utils.ffmpeg import extract_audio
from utils.paths import tmpdir


def _format_ts(sec: float) -> str:
    h, m = divmod(sec, 3600)
    m, s = divmod(m,   60)
    ms = int((s - int(s)) * 1000)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{ms:03d}"


def transcribe(
        video_path: Path, 
        output_dir: Path, 
        model_name: str = "base", 
        progress_cb: Callable[[int, int], None] | None = None
    ) -> Path:
    if progress_cb:
        progress_cb(0, 100)
    wav = extract_audio(video_path, tmpdir())          # → .wav
    if progress_cb:
        progress_cb(10, 100)
    model = whisper.load_model(model_name)
    result = model.transcribe(str(wav), language="ja", fp16=False)
    if progress_cb:
        progress_cb(90, 100)

    srt_lines: list[str] = []
    for i, raw in enumerate(result["segments"], 1):
        seg: Dict[str, Any] = cast(Dict[str, Any], raw)   # 型ヒントを与える
        start = float(seg["start"])
        end   = float(seg["end"])
        text  = str(seg["text"]).strip()
        srt_lines.append(f"{i}\n{_format_ts(start)} --> {_format_ts(end)}\n{text}\n")

    out_path = output_dir / f"{video_path.stem}.srt"
    out_path.write_text("\n".join(srt_lines), encoding="utf-8")
    if progress_cb:
        progress_cb(100, 100)
    return out_path

# CLI から直接呼ぶときのラッパー
# def transcribe_cli(video_path: Path, output_dir: Path, model_name: str) -> None:
#     out = transcribe(video_path, output_dir, model_name)
#     print(f"[OK] SRT: {out}")

def transcribe_cli(video_path: Path, output_dir: Path, model_name: str) -> None:
    bar = tqdm(total=100, desc="Processing", unit="%")
    start = time.perf_counter()

    def _cb(current: int, total: int) -> None:
        bar.n = current
        bar.refresh()

    out = transcribe(video_path, output_dir, model_name, progress_cb=_cb)
    bar.close()

    elapsed = time.perf_counter() - start
    print(f"\n✅  Done in {elapsed:,.1f} seconds — SRT: {out}")
from pathlib import Path
import whisper
import ffmpeg


def transcribe(video: str | Path, out_dir: str | Path, model="base",
               progress_cb=lambda v: None) -> Path:
    video, out_dir = Path(video), Path(out_dir)
    wav = out_dir / (video.stem + ".wav")

    # 音声抽出
    if not wav.exists():
        (ffmpeg
         .input(str(video))
         .output(str(wav), ac=1, ar="16k")
         .overwrite_output()
         .run(quiet=True))
    model = whisper.load_model(model)
    result = model.transcribe(str(wav), language="ja",
                              progress_callback=lambda p: progress_cb(p*100))
    srt = out_dir / (video.stem + ".srt")
    srt.write_text(whisper.utils.write_srt(
        result["segments"]), encoding="utf-8")
    return srt

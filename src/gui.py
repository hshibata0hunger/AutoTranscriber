from __future__ import annotations
import threading
import queue
import os

from src.transcriber import transcribe
from pathlib import Path

# GUI でメインスレッドとやり取りするメッセージキュー
Q: "queue.Queue[tuple[str,object]]" = queue.Queue()


def _worker(video: Path, out_dir: Path, model: str):
    try:
        srt_path = transcribe(video, out_dir, model)
        Q.put(("SUCCESS", srt_path))
    except Exception as exc:
        Q.put(("ERROR", str(exc)))


def run_gui(default_model: str = "base") -> None:
    import tkeasyGUI as teg
    
    window = teg.Window("AutoTranscriber", theme="dark")
    
    # Create widgets
    window.add_label("動画をドロップ or 参照")
    input_field = window.add_entry()
    browse_btn = window.add_file_button("参照", filetypes=[("Movie", "*.mp4 *.mov *.mkv")])
    
    window.add_label("出力先フォルダ")
    output_field = window.add_entry()
    output_browse = window.add_folder_button("参照")
    
    window.add_label("モデル")
    model_combo = window.add_combobox(["tiny", "base", "small", "medium", "large"], default=default_model)
    
    progress_bar = window.add_progress_bar(length=400)
    
    run_btn = window.add_button("実行")
    exit_btn = window.add_button("終了")
    
    # Enable drag and drop
    input_field.enable_drop()
    
    running = False
    
    def on_drop(data):
        input_field.set_text(data)
    
    def on_run():
        nonlocal running
        if running:
            return
            
        video = Path(input_field.get_text()).expanduser()
        outd = Path(output_field.get_text()).expanduser()
        
        if not video.is_file() or not outd.is_dir():
            teg.show_error("入力または出力先が不正です。")
            return
            
        running = True
        progress_bar.set(10)
        
        threading.Thread(
            target=_worker,
            args=(video, outd, model_combo.get_value()),
            daemon=True
        ).start()
    
    def check_queue():
        nonlocal running
        try:
            msg, payload = Q.get_nowait()
            if msg == "SUCCESS":
                running = False
                progress_bar.set(100)
                teg.show_info(f"SRT 生成完了:\n{payload}")
                os.system(f"open -R '{payload}'")
                progress_bar.set(0)
            elif msg == "ERROR":
                running = False
                progress_bar.set(0)
                teg.show_error(f"エラー: {payload}")
        except queue.Empty:
            pass
        finally:
            if not window.is_closed():
                window.after(100, check_queue)
    
    input_field.on_drop(on_drop)
    run_btn.on_click(on_run)
    exit_btn.on_click(window.close)
    
    check_queue()
    window.run()

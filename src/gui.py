from __future__ import annotations
import threading
import queue
import os
import PySimpleGUI as sg

from transcriber import transcribe
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
    sg.theme("DarkBlue3")
    progress = sg.ProgressBar(100, orientation="h", size=(40,15), key="-PROG-")
    input_elem   = sg.Input("", key="-IN-", enable_events=True)
    browse_btn   = sg.FileBrowse(file_types=(("Movie", "*.mp4 *.mov *.mkv"),))
    
    layout = [
        [sg.Text("動画をドロップ or 参照")],
        [input_elem, browse_btn],
        [sg.Text("出力先フォルダ"), sg.Input("", key="-OUT-"), sg.FolderBrowse()],
        [sg.Text("モデル"), sg.Combo(("tiny", "base", "small", "medium",
                                   "large"), default_value=default_model, key="-MODEL-")],
        [progress],
        [sg.Button("実行", key="-RUN-"), sg.Exit("終了")],
    ]
    win = sg.Window("AutoTranscriber", layout, finalize=True)
    # win["-IN-"].Widget.drop_target_register("*")  # macOS でも D&D OK
    tk_widget = cast(tk.Widget, input_elem.Widget)   # type: ignore[attr-defined]
    tk_widget.drop_target_register("*")              # type: ignore[attr-defined]
    tk_widget.dnd_bind(
        "<<Drop>>",
        lambda e: win.write_event_value("FILE_DROP", e.data)
    )
    
    

    running = False

    while True:
        event, values = win.read(timeout=100)
        if event in (sg.WIN_CLOSED, "終了"):
            break

        if event == "-RUN-" and not running:
            video = Path(values["-IN-"]).expanduser()
            outd = Path(values["-OUT-"]).expanduser()
            if not video.is_file() or not outd.is_dir():
                sg.popup_error("入力または出力先が不正です。")
                continue
            running = True
            progress.update_bar(10)
            threading.Thread(
                target=_worker,
                args=(video, outd, values["-MODEL-"]),
                daemon=True
            ).start()

        # ワーカー → メインへの通知
        try:
            msg, payload = Q.get_nowait()
        except queue.Empty:
            continue
        if msg == "SUCCESS":
            running = False
            progress.update_bar(100)
            sg.popup_ok(f"SRT 生成完了:\n{payload}")
            os.system(f"open -R '{payload}'")          # Finder でハイライト
            progress.update_bar(0)
        elif msg == "ERROR":
            running = False
            progress.update_bar(0)
            sg.popup_error(f"エラー: {payload}")

    win.close()

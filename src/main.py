import flet as ft
from pathlib import Path
from src.transcriber import transcribe


def main(page: ft.Page):
    page.title = "AutoTranscriber"
    page.window_width, page.window_height = 560, 420
    page.theme_mode = ft.ThemeMode.DARK

    in_tf = ft.TextField(label="動画ファイル", expand=True)
    out_tf = ft.TextField(label="出力フォルダ", expand=True)
    model = ft.Dropdown(label="モデル",
                        options=[ft.dropdown.Option(x) for x in
                                 ("tiny", "base", "small", "medium", "large")],
                        value="base", width=150)
    pb = ft.ProgressBar(width=520)
    log = ft.Text()

    async def browse_file(_):
        r = await page.dialog_open_file(file_types=[("Movie", "*.mp4;*.mov;*.mkv")])
        if r:
            in_tf.value = r.files[0].path
            await page.update_async()

    async def browse_dir(_):
        r = await page.dialog_open_directory()
        if r:
            out_tf.value = r.path
            await page.update_async()

    async def run(_):
        pb.value, log.value = 0.01, ""
        await page.update_async()

        def cb(p):
            pb.value = p/100
            page.update()

        try:
            srt = transcribe(in_tf.value, out_tf.value, model.value, cb)
            pb.value = 1
            log.value = f"✅ 完了: {srt}"
        except Exception as e:
            log.value = f"❌ {e}"

        await page.update_async()

    page.add(
        ft.Column([
            ft.Row([in_tf, ft.ElevatedButton("参照", on_click=browse_file)]),
            ft.Row([out_tf, ft.ElevatedButton("参照", on_click=browse_dir)]),
            model,
            ft.ElevatedButton("文字起こし実行", on_click=run),
            pb, log
        ], expand=True, spacing=10)
    )


ft.app(target=main)

import argparse
from pathlib import Path
from src.transcriber import transcribe_cli


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="AutoTranscriber", description="Video → SRT 自動書き起こしツール")
    p.add_argument("--cli", action="store_true", help="GUI を起動せず CLI で実行")
    p.add_argument("input_video", nargs="?", help=".mp4 / .mov など入力ファイル")
    p.add_argument("output_dir",  nargs="?", help="SRT 出力先ディレクトリ")
    p.add_argument("--model", default="base",
                   choices=["tiny", "base", "small", "medium", "large"], help="Whisper モデル")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    if args.cli:
        if not args.input_video or not args.output_dir:
            raise SystemExit("CLI モードでは input_video と output_dir を指定してください。")
        transcribe_cli(
            video_path=Path(args.input_video).expanduser().resolve(),
            output_dir=Path(args.output_dir).expanduser().resolve(),
            model_name=args.model,
        )
    else:
        from src.gui import run_gui
        run_gui(default_model=args.model)


if __name__ == "__main__":
    main()

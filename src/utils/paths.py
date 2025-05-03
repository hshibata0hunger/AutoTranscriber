from pathlib import Path
import tempfile
import os


def project_root() -> Path:
    # return Path(__file__).resolve().parents[2]
    return Path(
        os.environ.get(
            "AUTO_TRANSCRIBER_ROOT",
            Path(__file__).resolve().parents[2]
        )
    ).resolve()


def tmpdir() -> Path:
    p = Path(tempfile.gettempdir()) / "autotranscriber"
    p.mkdir(parents=True, exist_ok=True)
    return p

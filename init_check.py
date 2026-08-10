import argparse
from pathlib import Path

QUOTES_DIR = Path("~/.local/share/quotes/").expanduser()


def init_files() -> None:
    (QUOTES_DIR / "last_shown.jsonl").touch(exist_ok=True)
    (QUOTES_DIR / "cache.jsonl").touch(exist_ok=True)
    (QUOTES_DIR / "storage.jsonl").touch(exist_ok=True)
    (QUOTES_DIR / ".initialized").touch(exist_ok=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="This tool is to get quotes")
    parser.add_argument("--save", action="store_true", help="To save last quote")
    parser.add_argument("--add", action="store_true", help="To add your own quote")
    parser.add_argument("--random", action="store_true", help="To choose a random quote from personal list")
    parser.add_argument("--remove", action="store_true", help="To remove a quote from personal list")
    parser.add_argument("--filter", action="store_true", help="To remove a quote from a filtered personal list")
    parser.add_argument("--where", action="store_true", help="To show the location of the saved quotes")
    return parser.parse_args()

def init_check():
    if not QUOTES_DIR.exists():
        QUOTES_DIR.mkdir(parents=True, exist_ok=True)
        init_files()
    if not (QUOTES_DIR / ".initialized").exists():
        init_files()

    return [parse_args(), QUOTES_DIR]

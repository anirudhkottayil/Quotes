import requests
import os
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
    return parser.parse_args()


def main() -> None:
    url = "https://zenquotes.io/api/quotes"

    if not QUOTES_DIR.exists():
        QUOTES_DIR.mkdir(parents=True, exist_ok=True)
        init_files()
    if not (QUOTES_DIR / ".initialized").exists():
        init_files()

    args = parse_args()


if __name__ == "__main__":
    main()

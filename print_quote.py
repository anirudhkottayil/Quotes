import requests
import json
import os

def get_quotes(QUOTES_DIR, url) -> int:
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Get request failed: {e}")
        return 1

    quotes = r.json()
    try:
        with open((QUOTES_DIR / "cache.jsonl"), "w") as file:
            for line in quotes:
                file.write(json.dumps(line) + '\n')
    except OSError as e:
        print(f"Cache write failed: {e}")
        return 1
    else:
        return 0


def check_cache(QUOTES_DIR) -> int:
    with open(QUOTES_DIR / "cache.jsonl"), "r+b") as file:
        file.seek(0, os.SEEK_END)
        pos = file.tell()

        if pos == 0:
            return 1

        file.seek(pos - 1)
        if file.read(1) == b'\n':
            pos -= 1

        while (pos > 0):
            file.seek(pos - 1)
            if file.read(1) == '\n':
                break
            pos -= 1

        file.seek(pos)
        line = file.readline()
        file.seek(pos)
        file.truncate()

        content = json.loads(line)
        print(f"{content["q"]} - {content["a"]}")
        return 0

def print_quote(QUOTES_DIR, url):
    if check_cache(QUOTES_DIR) == 1:
        if get_quotes(QUOTES_DIR, url) == 1:
            print("Failed")
            return 1
        if check_cache(QUOTES_DIR) == 1:
            print("Failed")
            return 1
    return 0

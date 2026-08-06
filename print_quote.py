import requests
import json
import os
from requests.exceptions import RequestException

def get_quotes(QUOTES_DIR, url) -> int:
    try:
        r = requests.get(url, timeout=7)
        r.raise_for_status()
    except RequestException as e:
        print(f"Get request failed: {e}")
        return 1

    try:
        quotes = r.json()
    except ValueError as e:
        quotes = None
        print(f"Response not JSON: {e}")
        return 1

    if not isinstance(quotes, list):
        print("Response not enclosed in list")
        return 1
    if quotes == []:
        print("Response is empty")
        return 1

    if not (isinstance(quotes[0], dict) and isinstance(quotes[0].get("q"), str) and isinstance(quotes[0].get("a"), str)):
        print("Response was not of the specified format")
        return 1
    try:
        with open((QUOTES_DIR / "cache.jsonl"), "w") as file:
            for line in quotes:
                file.write(json.dumps(line) + '\n')
    except OSError as e:
        print(f"Cache write failed: {e}")
        return 1
    else:
        return 0

def write_into_last_shown(QUOTES_DIR, content) -> int:
    try:
        with open((QUOTES_DIR / "last_shown.jsonl"), "w") as file:
            file.write(json.dumps(content) + '\n')
    except OSError as e:
        print(f"Write into last shown failed: {e}")
        return 1
    return 0


def check_cache(QUOTES_DIR) -> int:
    with open((QUOTES_DIR / "cache.jsonl"), "r+b") as file:
        file.seek(0, os.SEEK_END)
        pos = file.tell()

        if pos == 0:
            return 1

        file.seek(pos - 1)
        if file.read(1) == b'\n':
            pos -= 1

        while (pos > 0):
            file.seek(pos - 1)
            if file.read(1) == b'\n':
                break
            pos -= 1

        file.seek(pos)
        line = file.readline()

        content = json.loads(line)
        if write_into_last_shown(QUOTES_DIR, content):
            return -1

        file.seek(pos)
        file.truncate()

        print(f'{content["q"]} - {content["a"]}')
        return 0

def print_quote(QUOTES_DIR, url):
    ret_val = check_cache(QUOTES_DIR)
    if ret_val == 0:
        return 0
    elif ret_val == -1:
        return 1
    else:
        if get_quotes(QUOTES_DIR, url):
            print("Failed")
            return 1
        if check_cache(QUOTES_DIR) != 0:
            print("Failed")
            return 1
        return 0

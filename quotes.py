import requests
import json
from init_check import init_check

def last_quote_write(QUOTES_DIR) -> None:
    with open((QUOTES_DIR / "last_shown.jsonl"), "r+") as file:
        line = file.readline()
        if line == '':
            print("No saved last quote found")
            return

        content = json.loads(line)
        try:
            with open((QUOTES_DIR / "storage.jsonl"), "a") as f:
                f.write(json.dumps(content) + '\n')
        except OSError as e:
            print(f"Write failed: {e}")
        else:
            file.truncate(0)
            print("Quote Saved")

def user_add_quote(QUOTES_DIR) -> None:
    line = {}
    quote = input("Enter Quote: ")
    if quote == "":
        print("No input received")
        return
    author = input("Enter Author: ")
    line["q"] = quote
    line["a"] = author
    try:
        with open((QUOTES_DIR / "storage.jsonl"), "a") as file:
            file.write(json.dumps(line) + '\n')
    except OSError as e:
        print(f"Write failed: {e}")
    else:
        print("Quote Saved")



def main() -> None:
    url = "https://zenquotes.io/api/quotes"
    args, QUOTES_DIR = init_check() # File checks and input flags

    if args.save:
        last_quote_write(QUOTES_DIR)
    if args.add:
        user_add_quote(QUOTES_DIR)
    if args.save or args.add:
        return



if __name__ == "__main__":
    main()

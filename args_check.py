import json
import random
from remover import remove_quote

def quote_exists(QUOTES_DIR,quote, author) -> int:
    with open((QUOTES_DIR / "storage.jsonl"), "r") as file:
        for line in file:
            content = json.loads(line)
            if content["a"].strip().lower() == author.strip().lower():
                if content["q"].strip().lower() == quote.strip().lower():
                    return 1
    return 0

def last_quote_write(QUOTES_DIR) -> None:
    with open((QUOTES_DIR / "last_shown.jsonl"), "r+") as file:
        line = file.readline()
        if line == '':
            print("No saved last quote found")
            return

        content = json.loads(line)
        if quote_exists(QUOTES_DIR, content["q"], content["a"]) == 1:
            print("Quote already in storage")
            file.truncate(0)
            return
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
    quote = input("Enter Quote: ").strip()
    if quote == "":
        print("No input received")
        return
    author = input("Enter Author: ").strip()
    if author == "":
        author = "UNKOWN"
    if quote_exists(QUOTES_DIR, quote, author) == 1:
        print("Quote already in storage")
        return
    line["q"] = quote
    line["a"] = author
    try:
        with open((QUOTES_DIR / "storage.jsonl"), "a") as file:
            file.write(json.dumps(line) + '\n')
    except OSError as e:
        print(f"Write failed: {e}")
    else:
        print("Quote Saved")

def print_random_quote(QUOTES_DIR) -> None:
    quotes = []
    with open((QUOTES_DIR / "storage.jsonl"), "r") as file:
        for line in file:
            line = line.strip()
            if line:
                quotes.append(json.loads(line))
    if quotes == []:
        print("No saved quotes to choose from")
        return
    quote = random.choice(quotes)
    # print(f'{quote["q"]} - {quote["a"]}')
    print(f'\033[1;36m{content["q"]}\033[0m - \033[2m{content["a"]}\033[0m')


def args_run(args,QUOTES_DIR) -> int:
    if args.save:
        last_quote_write(QUOTES_DIR)
    if args.add:
        user_add_quote(QUOTES_DIR)
    if args.random:
        print_random_quote(QUOTES_DIR)
    if args.remove:
        remove_quote(QUOTES_DIR, args.filter)
    if args.filter and not args.remove:
        print("--filter requires --remove")
    if args.save or args.add or args.random or args.remove or args.filter:
        return 1
    return 0

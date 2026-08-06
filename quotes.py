from init_check import init_check
from args_check import args_run
from print_quote import print_quote


def main() -> None:
    url = "https://zenquotes.io/api/quotes"

    args, QUOTES_DIR = init_check() # File checks and input flags

    if args_run(args, QUOTES_DIR) == 1: # Checks and completes input flags functionality
        return
    if print_quote(QUOTES_DIR, url) == 1:
        return

if __name__ == "__main__":
    main()

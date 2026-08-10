import curses
import textwrap, tempfile, os
import json

def get_idx(curses, body, stdscr, width, height, end, quotes, top, curr_len):
    current = 1
    i = top
    body.addstr(current, 2, f"{quotes[i][0]}",
                curses.color_pair(1) | curses.A_REVERSE)
    if len(quotes[i]) > 1:
        end.addstr(1, 2, f"{quotes[i][0]}".ljust(width - 4),
                    curses.color_pair(1) | curses.A_REVERSE)
        end.addstr(2, 2, f"{quotes[i][1]}".ljust(width - 4),
                    curses.color_pair(1) | curses.A_REVERSE)
    else:
        end.addstr(1, 2, f"{quotes[i][0]}".ljust(width - 4),
                    curses.color_pair(1) | curses.A_REVERSE)
        end.addstr(2, 2, f"".ljust(width - 4),
                    curses.color_pair(1) | curses.A_REVERSE)

    body.refresh()
    end.refresh()
    while True:
        key = stdscr.getch() 
        if key == ord("q"):
            return -1
        if (key == 10) or (key == 13) or (key == curses.KEY_ENTER):
            return i
        if (key == curses.KEY_UP) or (key == ord("k")):
            if (i - 1) < top and (top > 0):
                return -3 #Key Up prev page
            if ((current - 1) < 1) or ((i - 1) < 0):
                continue
            body.addstr(current , 2, f"{quotes[i][0]}"[:width - 4],
                        curses.color_pair(1))
            body.addstr(current - 1, 2, f"{quotes[i-1][0]}"[:width - 4],
                        curses.color_pair(1) | curses.A_REVERSE)
            if len(quotes[i - 1]) > 1:
                end.addstr(1, 2, f"{quotes[i - 1][0]}".ljust(width - 4),
                            curses.color_pair(1) | curses.A_REVERSE)
                end.addstr(2, 2, f"{quotes[i - 1][1]}".ljust(width - 4),
                            curses.color_pair(1) | curses.A_REVERSE)
            else:
                end.addstr(1, 2, f"{quotes[i - 1][0]}".ljust(width - 4),
                            curses.color_pair(1) | curses.A_REVERSE)
                end.addstr(2, 2, f"".ljust(width - 4),
                            curses.color_pair(1) | curses.A_REVERSE)

            current -= 1
            i -= 1
            body.refresh()
            end.refresh()

        elif (key == curses.KEY_DOWN) or (key == ord("j")):
            if ((i + 1) > (len(quotes) - 1)):
                continue

            if (i + 1) >= (top + curr_len) and ((top + curr_len) < len(quotes)):
                return -2
            body.addstr(current, 2, f"{quotes[i][0]}",
                        curses.color_pair(1))
            body.addstr(current + 1, 2, f"{quotes[i + 1][0]}",
                        curses.color_pair(1) | curses.A_REVERSE)

            if len(quotes[i + 1]) > 1:
                end.addstr(1, 2, f"{quotes[i + 1][0]}".ljust(width - 4),
                            curses.color_pair(1) | curses.A_REVERSE)
                end.addstr(2, 2, f"{quotes[i + 1][1]}".ljust(width - 4),
                            curses.color_pair(1) | curses.A_REVERSE)
            else:
                end.addstr(1, 2, f"{quotes[i + 1][0]}".ljust(width - 4),
                            curses.color_pair(1) | curses.A_REVERSE)
                end.addstr(2, 2, f"".ljust(width - 4),
                            curses.color_pair(1) | curses.A_REVERSE)
            current += 1
            i += 1
            body.refresh()
            end.refresh()


def ui(stdscr, messages):
    if messages == []:
        return

    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.curs_set(0)

    height, width = stdscr.getmaxyx()
    header = stdscr.subwin(3, width, 0, 0)
    body = stdscr.subwin(height - 7, width, 3, 0)
    end = stdscr.subwin(4, width, height - 4, 0)
    visible_rows = height - 3 - 2 - 4

    quotes = []
    for i in range(len(messages)):
        quotes.append(textwrap.wrap(messages[i]['q'], width - 4))

    header.erase()
    header.bkgd(" ", curses.color_pair(1))
    title = "Remove a Quote"
    header.addstr(1, (width - len(title)) // 2, title, curses.color_pair(1) | curses.A_BOLD)
    header.refresh()

    body.erase()
    body.box()
    body.keypad(True)
    end.erase()
    end.box()

    box_length = []
    top = 0
    itr = 1
    while True:
        length = min(visible_rows, len(quotes) - top)
        body.erase()
        body.box()
        for i in range(length):
            body.addstr(i + 1, 2, f"{quotes[top + i][0]}", curses.color_pair(1)) 
        body.refresh()

        idx = get_idx(curses, body, stdscr, width, height, end, quotes, top, length)

        if idx >= -1: # either user press q or got the indx of quote
            return idx
        if idx == -2: # user went down to next screen of quotes
            top = top + length
            box_length.append(length)
        if idx == -3:
            top = top - box_length.pop()

def get_quotes_to_remove(QUOTES_DIR, search=None):
    # fiter format: [author, quote]

    quotes = []
    with open((QUOTES_DIR / "storage.jsonl"), "r") as file:
        for line in file:
            quotes.append(json.loads(line))
    if (search == None):
        return [quotes, [], []]
    if (search[0] == "") and (search[1] == ""):
        return [quotes, [], []]

    quote_indx = []
    quote_filtered = []

    if search[0] is None:
        search[0] = ""
    if search[1] is None:
        search[1] = ""

    for i, content in enumerate(quotes):
        if (content["a"].strip().lower() == search[0].strip().lower()) or (content["q"].strip().lower() == search[1].strip().lower()):
            quote_filtered.append(content)
            quote_indx.append(i)

    return [quote_filtered, quote_indx, quotes]

def get_input():
    quote = input("Enter Quote: ").strip()
    author = input("Enter Author: ").strip()
    return [author, quote]

def remove_quote(QUOTES_DIR, is_filter):
    search = None
    if is_filter:
        search = get_input() 
    quotes = get_quotes_to_remove(QUOTES_DIR, search)
    if quotes[0] == []:
        print("No Quotes to remove")
        return
    idx = curses.wrapper(ui, quotes[0])
    if idx == -1:
        return

    full_ls = 0
    if quotes[1] != []:
        idx = quotes[1][idx]
        full_ls = 2

    fd, tmp = tempfile.mkstemp(dir=QUOTES_DIR)
    try:
        with open(fd, "w") as file:
            for i in range(len(quotes[full_ls])):
                if i == idx:
                    continue
                file.write(json.dumps(quotes[full_ls][i]) + '\n')
    except OSError as e:
        print(f"Write failed: {e}")
    else:
        print("Quote removed")
        os.replace(tmp, QUOTES_DIR / "storage.jsonl")
    return

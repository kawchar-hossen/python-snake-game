#!/usr/bin/env python3

try:
    import curses
except ImportError:
    from os import name as osname

    if osname == "nt":
        print(
            "Curses not installed. You can install it with: `pip install windows-curses`"
        )
    exit(1)
import random
import sys


def main(stdscr):
    # Initialize curses
    curses.curs_set(0)
    curses.use_default_colors()
    curses.noecho()
    stdscr.nodelay(True)
    stdscr.timeout(100)
    if len(sys.argv) > 1 and "--color" in sys.argv:
        curses.init_pair(1, curses.COLOR_WHITE, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, curses.COLOR_YELLOW, -1)
    else:
        curses.init_pair(1, -1, -1)
        curses.init_pair(2, -1, -1)
        curses.init_pair(3, -1, -1)


    # Set constant variables
    ROWS = stdscr.getmaxyx()[0] - 1
    COLS = stdscr.getmaxyx()[1] - 1
    CHAR_SNAKE = "#"
    CHAR_FOOD = "*"
    CHAR_BG = "."
    IS_LARGE_ENOUGH = COLS > 50

    # Initialize game variables
    snake = [[5, 5], [5, 4], [5, 3]]
    score = 0
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        for i in range(int(sys.argv[1])):
            snake.append([5, 3])
        score = int(sys.argv[1])
    food = [ROWS // 2, COLS // 2]
    direction = 100
    paused = False

    # draw board
    for x in range(ROWS):
        for y in range(COLS):
            stdscr.addstr(x, y, CHAR_BG, curses.color_pair(1))

    # draw snake
    for i, _ in enumerate(snake):
        stdscr.addstr(*snake[i], CHAR_SNAKE, curses.color_pair(2))

    # draw food
    stdscr.addstr(*food, CHAR_FOOD, curses.color_pair(3))

    stdscr.addstr(ROWS, 0, "Controls: wasd or arrow keys, q to quit | Score: 0" if IS_LARGE_ENOUGH else "Score: 0", curses.color_pair(1))

    # main loop
    while True:
        # next_direction = stdscr.getkey()
        try:
            next_direction = stdscr.getch()
        except KeyboardInterrupt:  # exit on ^C
            return "Quit"
        direction = direction if next_direction == -1 else next_direction
        new_head = snake[0].copy()
        if direction in (119, 259):  # w | ^
            new_head[0] -= 1
        elif direction in (97, 260):  # a | <
            new_head[1] -= 1
        elif direction in (115, 258):  # s | v
            new_head[0] += 1
        elif direction in (100, 261):  # d | >
            new_head[1] += 1
        elif direction in (113, 27):  # q | esc
            return f"Quit, score: {score}"
        else:
            continue
        if not paused:
            snake.insert(0, new_head)
            if snake[0][0] in (ROWS, -1):
                return f"Snake out of bounds vertically, score: {score}"
            if snake[0][1] in (COLS, -1):
                return f"Snake out of bounds horizontally, score: {score}"
            if snake[0] in snake[1:]:
                return f"Snake can't eat itself, score: {score}"
            if snake[0] == food:
                food = None
                while food is None:
                    new_food = [
                        random.randint(0, ROWS - 1),
                        random.randint(0, COLS - 1),
                    ]
                    food = new_food if new_food not in snake else None
                stdscr.addstr(*food, CHAR_FOOD, curses.color_pair(3))
                score += 1
            else:
                stdscr.addstr(*snake.pop(-1), CHAR_BG, curses.color_pair(1))
            stdscr.addstr(*snake[0], CHAR_SNAKE, curses.color_pair(2))
        stdscr.addstr(ROWS, 49 if IS_LARGE_ENOUGH else 7, str(score), curses.color_pair(1))
        stdscr.refresh()


if __name__ == "__main__":
    print(f"Game over: {curses.wrapper(main)}")

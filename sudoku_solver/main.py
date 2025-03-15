import curses

from sudoku import Sudoku


def main(stdscr):
    stdscr = curses.initscr()
    # Hide cursor
    curses.curs_set(0)
    stdscr.keypad(True)

    # Sample board
    board = [
        0, 6, 2, 4, 0, 5, 0, 0, 8,
        0, 0, 5, 0, 0, 0, 4, 2, 0,
        3, 0, 4, 9, 0, 0, 5, 6, 0,
        0, 0, 0, 6, 0, 2, 9, 8, 4,
        0, 2, 7, 0, 4, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 1, 0, 0, 0,
        4, 9, 6, 1, 5, 7, 8, 0, 0,
        2, 0, 8, 0, 0, 0, 7, 0, 5,
        7, 5, 0, 0, 0, 4, 0, 9, 6,
    ]
    sudoku = Sudoku(board)

    while True:
        sudoku.display_board(stdscr)
        key = stdscr.getch()
        # Press 'q' to quit
        if key == ord('q'):
            break
        sudoku.handle_input(key)


if __name__ == "__main__":
    curses.wrapper(main)

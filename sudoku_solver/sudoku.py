import curses


class Sudoku:
    def __init__(self, board):
        self.board = board
        # Track initial fixed numbers
        self.fixed_cells = {i for i, val in enumerate(board) if val != 0}
        self.cursor_x = 0
        self.cursor_y = 0

    def validate(self):
        # Validate rows and columns. 0's are ignored
        for i in range(9):
            row = set()
            column = set()
            for j in range(9):
                # Validate rows
                row_cell = self.board[i * 9 + j]
                if row_cell in row:
                    return False
                row.add(row_cell) if row_cell != 0 else None

                # Validate columns
                column_cell = self.board[j * 9 + i]
                if column_cell in column:
                    return False
                column.add(column_cell) if column_cell != 0 else None

        # Validate 3x3 squares
        for block_i in range(3):
            for block_j in range(3):
                square = set()
                for i in range(3):
                    for j in range(3):
                        index = (block_i * 3 + i) * 9 + (block_j * 3 + j)
                        if self.board[index] in square:
                            return False
                        square.add(
                            self.board[index]) if self.board[index] != 0 else None

        return True

    def solved(self):
        return 0 not in self.board and self.validate()

    def display_board(self, stdscr):
        stdscr.clear()

        # Top border
        stdscr.addstr(0, 0, '-' * 19)

        for y in range(9):
            # Calculate actual y position accounting for horizontal dividers
            display_y = y + 1 + (y // 3)

            # Left border
            stdscr.addstr(display_y, 0, '|')

            # Horizontal dividers
            if y % 3 == 0 and y != 0:
                stdscr.addstr(display_y - 1, 0, '------+-----+------')

            for x in range(9):
                index = y * 9 + x
                value = self.board[index]
                # Display value or empty cell
                display_char = str(value) if value != 0 else '.'

                # Set fixed cells to bold
                color = curses.A_BOLD if index in self.fixed_cells else 0

                # Determine if cell under cursor should be highlighted
                if y == self.cursor_y and x == self.cursor_x:
                    stdscr.addstr(display_y, x * 2 + 1,
                                  display_char, curses.A_REVERSE)
                else:
                    stdscr.addstr(display_y, x * 2 + 1, display_char, color)

                # Vertical dividers
                if x % 3 == 2:
                    stdscr.addstr(display_y, x * 2 + 2, '|')

        # Bottom border
        stdscr.addstr(12, 0, '-' * 19)
        stdscr.addstr(13, 0, 'Valid: ' + ('Yes' if self.validate() else 'No'))
        stdscr.addstr(
            14, 0, 'Use arrow keys and numbers to modify cells. Press q to quit')
        stdscr.refresh()

    def handle_input(self, key):
        if key == curses.KEY_UP and self.cursor_y > 0:
            self.cursor_y -= 1
        elif key == curses.KEY_DOWN and self.cursor_y < 8:
            self.cursor_y += 1
        elif key == curses.KEY_LEFT and self.cursor_x > 0:
            self.cursor_x -= 1
        elif key == curses.KEY_RIGHT and self.cursor_x < 8:
            self.cursor_x += 1
        elif ord('1') <= key <= ord('9'):
            index = self.cursor_y * 9 + self.cursor_x
            if index not in self.fixed_cells:
                # Allow changes only in empty cells
                self.board[index] = key - ord('0')

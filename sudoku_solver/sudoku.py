class Sudoku:

    # Board is a single array of 81 values with 0 for empty cells
    def __init__(self, board):
        self.board = board

    def display_board(self):
        # Top border
        print('-' * 25)

        i = 1
        for cell in self.board:
            # Left border at start of each row
            if i % 9 == 1:
                print('|', end=' ')

            # Empty cell
            if cell == 0:
                print('.', end=' ')
            else:
                print(cell, end=' ')

            # Vertical lines
            if i % 3 == 0:
                if i % 9 == 0:
                    print('|')  # Right border
                else:
                    print('|', end=' ')

            i += 1

            # Horizontal lines
            if i % 27 == 1 and i != 82:
                print('-' * 8, end='')
                print('+', end='')
                print('-' * 7, end='')
                print('+', end='')
                print('-' * 8)

        # Bottom border
        print('-' * 25)

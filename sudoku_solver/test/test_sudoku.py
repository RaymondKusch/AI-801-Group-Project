import unittest
import curses

from sudoku_solver.sudoku import Sudoku


class TestSudoku(unittest.TestCase):
    def setUp(self):
        # Valid complete board
        self.valid_board = [
            5, 3, 4, 6, 7, 8, 9, 1, 2,
            6, 7, 2, 1, 9, 5, 3, 4, 8,
            1, 9, 8, 3, 4, 2, 5, 6, 7,
            8, 5, 9, 7, 6, 1, 4, 2, 3,
            4, 2, 6, 8, 5, 3, 7, 9, 1,
            7, 1, 3, 9, 2, 4, 8, 5, 6,
            9, 6, 1, 5, 3, 7, 2, 8, 4,
            2, 8, 7, 4, 1, 9, 6, 3, 5,
            3, 4, 5, 2, 8, 6, 1, 7, 9
        ]

        # Board with duplicates in row
        self.invalid_row_board = [
            5, 5, 4, 6, 7, 8, 9, 1, 2,  # duplicate 5 in first row
            6, 7, 2, 1, 9, 5, 3, 4, 8,
            1, 9, 8, 3, 4, 2, 5, 6, 7,
            8, 0, 9, 7, 6, 1, 4, 2, 3,
            4, 2, 6, 8, 5, 3, 7, 9, 1,
            7, 1, 3, 9, 2, 4, 8, 5, 6,
            9, 6, 1, 5, 3, 7, 2, 8, 4,
            2, 8, 7, 4, 1, 9, 6, 3, 5,
            3, 4, 5, 2, 8, 6, 1, 7, 9
        ]

        self.invalid_column_board = [
            5, 3, 4, 6, 7, 8, 9, 1, 2,
            5, 7, 2, 1, 9, 0, 3, 4, 8,  # duplicate 5 in first column
            1, 9, 8, 3, 4, 2, 5, 6, 7,
            8, 5, 9, 7, 6, 1, 4, 2, 3,
            4, 2, 6, 8, 5, 3, 7, 9, 1,
            7, 1, 3, 9, 2, 4, 8, 5, 6,
            9, 6, 1, 5, 3, 7, 2, 8, 4,
            2, 8, 7, 4, 1, 9, 6, 3, 5,
            3, 4, 5, 2, 8, 6, 1, 7, 9
        ]

        self.invalid_square_board = [
            5, 3, 4, 6, 7, 8, 9, 1, 2,
            6, 7, 2, 1, 9, 5, 3, 4, 8,
            1, 9, 5, 3, 4, 2, 0, 6, 7,  # duplicate 5 in first square
            8, 5, 9, 7, 6, 1, 4, 2, 3,
            4, 2, 6, 8, 5, 3, 7, 9, 1,
            7, 1, 3, 9, 2, 4, 8, 5, 6,
            9, 6, 1, 5, 3, 7, 2, 8, 4,
            2, 8, 7, 4, 1, 9, 6, 3, 5,
            3, 4, 5, 2, 8, 6, 1, 7, 9
        ]

        # Empty board
        self.empty_board = [0] * 81

    def test_valid_board(self):
        sudoku = Sudoku(self.valid_board)
        self.assertTrue(sudoku.validate())

    def test_invalid_row(self):
        sudoku = Sudoku(self.invalid_row_board)
        self.assertFalse(sudoku.validate())

    def test_invalid_column(self):
        sudoku = Sudoku(self.invalid_column_board)
        self.assertFalse(sudoku.validate())

    def test_invalid_square(self):
        sudoku = Sudoku(self.invalid_square_board)
        self.assertFalse(sudoku.validate())

    def test_empty_board(self):
        sudoku = Sudoku(self.empty_board)
        self.assertTrue(sudoku.validate())

    def test_solved(self):
        sudoku = Sudoku(self.valid_board)
        self.assertTrue(sudoku.solved())

    def test_cursor_movement(self):
        sudoku = Sudoku(self.empty_board)
        # Test cursor up
        sudoku.cursor_y = 1
        sudoku.handle_input(curses.KEY_UP)
        self.assertEqual(sudoku.cursor_y, 0)

        # Test cursor down
        sudoku.handle_input(curses.KEY_DOWN)
        self.assertEqual(sudoku.cursor_y, 1)

        # Test cursor left
        sudoku.cursor_x = 1
        sudoku.handle_input(curses.KEY_LEFT)
        self.assertEqual(sudoku.cursor_x, 0)

        # Test cursor right
        sudoku.handle_input(curses.KEY_RIGHT)
        self.assertEqual(sudoku.cursor_x, 1)

    def test_number_input(self):
        sudoku = Sudoku(self.empty_board)
        # Test inputting number 5
        sudoku.handle_input(ord('5'))
        self.assertEqual(sudoku.board[0], 5)

    def test_fixed_cells(self):
        sudoku = Sudoku(self.valid_board)
        # Try to modify a fixed cell
        original_value = sudoku.board[0]
        sudoku.handle_input(ord('9'))
        self.assertEqual(sudoku.board[0], original_value)


if __name__ == '__main__':
    unittest.main()

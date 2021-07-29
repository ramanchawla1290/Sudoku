"""
SUDOKU GENERATOR

Creating a VALID 9x9 Sudoku Board as per the following rules:
1. In all the 9 grids (3×3 sub-grids), the elements should be 1-9, without repetition.
2. In all the rows, the elements should be between 1-9 , without repetition.
3. In all the columns, the elements should be between 1-9 , without repetition.

Constructors:
    Sudoku():
        creates an empty instance.
        To assign a grid, set the 'grid' property of the class instance
        to a valid 9x9 array
        eg:

        >> su = Sudoku()
        >> su..grid = GRID_ARRAY    # where GRID_ARRAY is a 9x9 array
                                    # a list of 9 lists containing 9 numbers each

    Sudoku(grid_array):
        where 'grid_array' is a 9x9 array representing a Sudoku grid

    Sudoku.new_grid(difficulty):
        where 'difficulty' can be : Sudoku.EASY, Sudoku.NORMAL or Sudoku.HARD
                                     (36 empty)   (45 empty)      (54 empty)
"""

from random import randint, shuffle

LEVEL_DICT = {
    "easy": 36,
    "normal": 45,
    "hard": 54
}


class SudokuError(Exception):
    """Exception class for Sudoku related errors"""

    def __init__(self, *args):
        """Constructor"""
        Exception.__init__(self, *args)


class SudokuMeta(type):
    """Metaclass for Sudoku Class"""
    def __init__(cls, *args, **kwargs):
        cls.__easy = "easy"             # 36 empty cells
        cls.__normal = "normal"         # 45 empty cells
        cls.__hard = "hard"             # 54 empty cells
        super().__init__(*args, **kwargs)

    @property
    def EASY(cls):
        """property getter for __easy"""
        return cls.__easy

    @property
    def NORMAL(cls):
        """property getter for __normal"""
        return cls.__normal

    @property
    def HARD(cls):
        """property getter for __hard"""
        return cls.__hard

    @EASY.setter
    def EASY(cls, val):
        """property setter for __easy"""
        raise SudokuError("Operation not allowed. Cannot change the internal "
                          + "value of the difficulty level")

    @NORMAL.setter
    def NORMAL(cls, val):
        """property setter for __normal"""
        raise SudokuError("Operation not allowed. Cannot change the internal "
                          + "value of the difficulty level")

    @HARD.setter
    def HARD(cls, val):
        """property setter for __hard"""
        raise SudokuError("Operation not allowed. Cannot change the internal "
                          + "value of the difficulty level")


def check_grid_for_none(func):
    """Decorator to Raise SudokuError if grid is 'None'"""

    def wrapper(self, *args, **kwargs):
        """wrapper for methods of class Sudoku"""
        if self.grid is None:
            raise SudokuError("Cannot process EMPTY grid. "
                              + "Please assign / generate a grid before processing.")
        else:
            return func(self, *args, **kwargs)
    return wrapper


class Sudoku(metaclass=SudokuMeta):
    """Class to implement Sudoku board generation and solution"""

    def __init__(self, grid=None):
        """Constructor"""
        self.__grid = None
        if grid:
            self.grid = grid

    @property
    def grid(self):
        """Returns the current Sudoku grid"""
        return self.__grid

    @grid.setter
    def grid(self, grid):
        """Handles assignment of new value to grid"""
        old_grid = self.__grid
        self.__grid = grid
        try:
            self.__is_valid_grid()
        except SudokuError as ex:
            self.__grid = old_grid
            raise SudokuError("Error in Grid Assignment : " + str(ex)) from ex

    @staticmethod
    def __get_new_grid():
        """Creates and Returns new Sudoku 9x9 Grid with populated diagonal blocks"""

        # Creating 9 blocks of size 3x3, filled with 0's
        blocks = [[[0] * 9 for i in range(3)] for j in range(3)]

        # Filling Diagaonal blocks with numbers 1-9 in random order
        for i in range(3):
            blocks[i][i] = [n for n in range(1, 10)]
            shuffle(blocks[i][i])

        # Generating 9x9 Sudoku grid from the 3x3 blocks
        grid = []

        for rows in ([blocks[x][y][z * 3:(z + 1) * 3] for y in range(3)]
                     for x in range(3) for z in range(3)):
            row_ = []
            for num_list in rows:
                row_ += num_list
            grid.append(row_)

        return grid

    def new_grid(self, level):
        """Assigns new grid of specified difficulty level to class instance"""
        if not isinstance(level, str):
            raise SudokuError(f"Invalid type '{type(level).__name__}' "
                              + "for grid difficulty level")

        elif level.lower() not in (Sudoku.EASY, Sudoku.NORMAL, Sudoku.HARD):
            raise SudokuError("Invalid value for grid difficulty level\n"
                              + "Valid options are : "
                              + "Sudoku.EASY, Sudoku.NORMAL or Sudoku.HARD")

        else:
            self.__grid = self.__get_new_grid()

            self.solve()

            count = LEVEL_DICT[level.lower()]

            while count > 0:
                row = randint(0, 8)
                col = randint(0, 8)

                if self.__grid[row][col] > 0:
                    self.__grid[row][col] = 0
                    count -= 1

    @check_grid_for_none
    def __is_valid_grid(self):
        """Validates the grid for size and values, Raises ValueError if invalid"""
        if not isinstance(self.__grid, list):
            raise SudokuError("Invalid grid type "
                              + f"'{type(self.__grid).__name__}' for Sudoku grid."
                              + " Only 'list' is allowed.")

        if len(self.__grid) != 9:      # Checking if grid doesn't have 9 rows
            raise SudokuError("Invalid grid size! "
                              + f"{len(self.__grid)} rows in grid")

        for i in range(9):        # Checking if any row doesn't have 9 values
            if len(self.__grid[i]) != 9:
                raise SudokuError("Invalid grid size! "
                                  + f"{len(self.__grid[i])} values in row {i}")

        zero_count = 0

        for row in self.__grid:
            for num in row:
                if not isinstance(num, int):
                    raise SudokuError("Invalid value type "
                                      + f"'{type(num).__name__}'. "
                                      + "Only 'int' values allowed")
                elif num < 0 or num > 9:
                    raise SudokuError(f"Invalid value {num}. Valid range 1-9."
                                      + "0 denotes 'Not Filled' Sudoku grid")
                elif num == 0:
                    zero_count += 1

        try:
            self.__check_repetition()
        except SudokuError as ex:
            raise SudokuError("REPETITION : " + str(ex)) from ex

        # After all checks
        return zero_count

    @check_grid_for_none
    def __check_repetition(self):
        """method to check repetition of values across row, column or block"""
        for i in range(9):
            row_ = tuple(n for n in self.__grid[i] if n > 0)
            col_ = tuple(row[i] for row in self.__grid if row[i] > 0)

            if len(row_) != len(set(row_)):             # Checking across Row
                raise SudokuError(f"Repetition of numbers in row {i}")

            if len(col_) != len(set(col_)):          # Checking across Column
                raise SudokuError(f"Repetition of numbers in column {i}")

        for i in range(3):                            # Checking across Block
            for j in range(3):
                block = tuple(self.__grid[x][y]
                              for x in range(i * 3, (i + 1) * 3)
                              for y in range(j * 3, (j + 1) * 3)
                              if self.__grid[x][y] > 0)
                if len(block) != len(set(block)):
                    raise SudokuError("Repetition of numbers in Block "
                                      + f"{3*i + j + 1}")

    @check_grid_for_none
    def __move_possible(self, row, col, num):
        """Returns True if move is valid, False otherwise"""
        # Checking possibility along row and column
        for i in range(9):
            if self.__grid[row][i] == num or self.__grid[i][col] == num:
                return False

        # Location of upper-left corner of the 3x3 block
        x_0 = (row // 3) * 3
        y_0 = (col // 3) * 3

        # Checking possibility in the block
        for i in range(3):
            for j in range(3):
                if self.__grid[x_0 + i][y_0 + j] == num:
                    return False
        return True

    @check_grid_for_none
    def solve(self):
        """Replaces 0's in the Sudoku grid with valid numbers"""
        for i in range(9):
            for j in range(9):
                if self.__grid[i][j] == 0:
                    for num in range(1, 10):
                        if self.__move_possible(i, j, num):
                            self.__grid[i][j] = num
                            if self.solve():
                                return True
                            self.__grid[i][j] = 0
                    return

        # When the grid is full
        return True

    @check_grid_for_none
    def print_grid(self):
        """Prints the 9x9 Sudoku Grid"""

        print()
        for row in self.__grid:
            for num in row:
                print(num, end="  ")
            print()


if __name__ == "__main__":
    grid_0 = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
              [6, 0, 0, 1, 9, 5, 0, 0, 0],
              [0, 9, 8, 0, 0, 0, 0, 6, 0],
              [8, 0, 0, 0, 6, 0, 0, 0, 3],
              [4, 0, 0, 8, 0, 3, 0, 0, 1],
              [7, 0, 0, 0, 2, 0, 0, 0, 6],
              [0, 6, 0, 0, 0, 0, 2, 8, 0],
              [0, 0, 0, 4, 1, 9, 0, 0, 5],
              [0, 0, 0, 0, 8, 0, 0, 0, 0]]

    # s = Sudoku()
    # s.grid = grid_0

    s = Sudoku(grid_0)
    s.print_grid()

    if s.solve():
        s.print_grid()

    # s.new_grid(Sudoku.EASY)

    # s.new_grid(Sudoku.NORMAL)

    s.new_grid(Sudoku.HARD)
    s.print_grid()

    if s.solve():
        s.print_grid()

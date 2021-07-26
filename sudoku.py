"""
SUDOKU GENERATOR

Creating a VALID 9x9 Sudoku Board as per the following rules:
1. In all the 9 grids (3×3 sub-grids), the elements should be 1-9, without repetition.
2. In all the rows, the elements should be between 1-9 , without repetition.
3. In all the columns, the elements should be between 1-9 , without repetition.
"""

from random import shuffle


class Sudoku:
    """Class to implement Sudoku board generation and validity check"""

    def __init__(self):
        """Constructor"""
        self.grid = Sudoku.__get_new_grid()

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

    def __is_valid_grid(self):
        """Validates the grid for size and values, Raises ValueError if invalid"""
        if not isinstance(self.grid, list):
            raise TypeError("Invalid type "
                            + f"'{type(self.grid).__name__}' for Sudoku grid")

        if len(self.grid) != 9:  # Checking if grid doesn't have 9 rows
            raise ValueError("Invalid grid size! "
                             + f"{len(self.grid)} rows in grid")

        for i in range(9):  # Checking if any row doesn't have 9 numbers
            if len(self.grid[i]) != 9:
                raise ValueError("Invalid grid size! Only"
                                 + f"{len(self.grid[i])} numbers in row {i}")

        # PENDING : Checking of values

    def __move_possible(self, row, col, num):
        """Returns True if move is valid, False otherwise"""
        # Checking possibility along row and column
        for i in range(9):
            if self.grid[row][i] == num or self.grid[i][col] == num:
                return False

        # Location of upper-left corner of the 3x3 block
        x_0 = (row // 3) * 3
        y_0 = (col // 3) * 3

        # Checking possibility in the block
        for i in range(3):
            for j in range(3):
                if self.grid[x_0 + i][y_0 + j] == num:
                    return False
        return True

    def __solve(self):
        """Replaces 0's in the Sudoku grid with valid numbers"""
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    for num in range(1, 10):
                        if self.__move_possible(i, j, num):
                            self.grid[i][j] = num
                            if self.__solve():
                                return True
                            self.grid[i][j] = 0
                    return

        # When the grid is full
        return True

    def solve(self):
        """Validates the grid, Returns the solved grid"""
        try:
            self.__is_valid_grid()
        except ValueError as ex:
            print(str(ex))
        except TypeError as ex:
            print(str(ex))
        else:
            print()
            print("Sudoku Grid:")
            self.print_grid()
            if self.__solve():
                print()
                print("Solution:")
                self.print_grid()
            else:
                print()
                print("No solution for the current grid!")

    def print_grid(self):
        """Prints the 9x9 Sudoku Grid"""
        print()
        for row in self.grid:
            for num in row:
                print(num, end="  ")
            print()


if __name__ == "__main__":
    s = Sudoku()

    s.solve()  # Solving generated grid

    s.grid = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
              [6, 0, 0, 1, 9, 5, 0, 0, 0],
              [0, 9, 8, 0, 0, 0, 0, 6, 0],
              [8, 0, 0, 0, 6, 0, 0, 0, 3],
              [4, 0, 0, 8, 0, 3, 0, 0, 1],
              [7, 0, 0, 0, 2, 0, 0, 0, 6],
              [0, 6, 0, 0, 0, 0, 2, 8, 0],
              [0, 0, 0, 4, 1, 9, 0, 0, 5],
              [0, 0, 0, 0, 8, 0, 0, 0, 0]]

    s.solve()  # Solving Custom grid

"""
SUDOKU GENERATOR

Creating a VALID 9x9 Sudoku Board as per the following rules:
1. In all the 9 grids (3×3 sub-grids), the elements should be 1-9, without repetition.
2. In all the rows, the elements should be between 1-9 , without repetition.
3. In all the columns, the elements should be between 1-9 , without repetition.
"""

from random import shuffle


class Sudoku:
    """Class to implement Sudoku board : generation and checking validity"""

    def __init__(self):
        """Constructor"""
        self.grid = self.__get_new_grid()

    @staticmethod
    def __get_new_grid():
        """Creates and Returns new Sudoku Grid (9x9)"""

        # Creating 3x3 blocks filled with 0's
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

    def generate_new_grid(self):
        """Assigns a new SUDOKU 9x9 grid to the Class instance"""
        self.grid = self.__get_new_grid()

    def print_grid(self):
        """Prints the Sudoku Grid (9x9)"""
        for row in self.grid:
            for num in row:
                print(num, end="  ")
            print()

    def get_blocks(self):
        """Converts 9x9 Sudoku grid into 9 Blocks of 3x3 and Returns it"""
        blocks = [[[self.grid[i][j] for i in range(3 * x + 0, 3 * x + 3)
                    for j in range(3 * y + 0, 3 * y + 3)]
                   for y in range(3)]
                  for x in range(3)]

        return blocks

    @staticmethod
    def print_block(block):
        """Prints the 3x3 Block"""
        for i in range(9):
            if i % 3 == 0:
                print()
            print(block[i], end=" ")


if __name__ == "__main__":
    s = Sudoku()
    print()
    print("SUDOKU Grid :\n")
    s.print_grid()
    print()

    blocks_ = s.get_blocks()

    for x in range(3):
        for y in range(3):
            print()
            print(f"Block[{x}][{y}]:")
            s.print_block(blocks_[x][y])
            print()

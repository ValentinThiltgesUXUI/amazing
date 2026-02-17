# IV.5 Output File Format
#
# The maze must be written in the output file using one hexadecimal digit per cell, where
# each digit encodes which walls are closed:
# Bit Direction
# 0 (LSB) North
# 1 East
# 2 South
# 3 West
#
# • A wall being closed sets the bit to 1, open means 0.
# Example: 3 (binary 0011) means walls are open to the south and west. Or A
# (binary 1010) means that east and west walls are closed.
# • Cells are stored row by row, one row per line.
# • After an empty line, the following 3 elements are inserted in the output file on 3
# lines:
# ◦ the entry coordinates, the exit coordinates, and the shortest valid path from
# entry to exit, using the four letters N , E , S , W .
# • All lines end with a \n .
# In conjunction with its specific configuration file, this output file could be tested automat-
# ically by a Moulinette. Also, a validation script is provided with this subject to control
# that the output file contains coherent data

from typing import cast


def direction_to_bit(string: str):
    match string:
        case "N":
            return 0
        case "E":
            return 1
        case "S":
            return 2
        case "O":
            return 3


def write_to_hex(grid: list[list[tuple | None]], entry, exit_, bfs):
    for row in grid:
        if None in row:
            return
        row_cast: list[tuple] = cast(list[tuple], row)
        for ct, color in row_cast:
            print(ct, color)

    print(f"\n{entry}\n{exit_}\n{bfs}")

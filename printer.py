from enum import Enum
import os
import time


class CellType(Enum):
    """Types de cellules pour le labyrinthe"""
    WALL = "█"
    POINT = "●"
    SPACE = " "


class Printer:
    RESET = "\033[0m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"

    def __init__(self) -> None:
        pass

    @staticmethod
    def paint(ct: CellType, color: str) -> None:
        print(f"{color}{ct.value}{Printer.RESET}", end="")

    @staticmethod
    def clear_screen() -> None:
        """Clear screen"""
        os.system('clear' if os.name == 'posix' else 'cls')

    @staticmethod
    def display_grid(grid: list[list[tuple]], delay: float = 0.05) -> None:
        """
        Display a 2D grid with animation
        grid: list of list of tuple (CellType, color)
        """
        Printer.clear_screen()
        for row in grid:
            for cell_type, color in row:
                Printer.paint(cell_type, color)
            print()
        time.sleep(delay)

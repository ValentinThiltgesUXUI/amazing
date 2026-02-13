import os
import time
from enum import Enum


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
        os.system("clear" if os.name == "posix" else "cls")

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

    def create_square_grid(self, width: int, height: int, char_ratio: int = 2) -> list:
        """
        Crée une grille carrée avec compensation du ratio d'aspect terminal.

        Args:
            width: Largeur de la grille
            height: Hauteur de la grille
            char_ratio: Ratio de compensation (défaut 2)

        Returns:
            Liste 2D représentant la grille
        """
        grid = []

        for i in range(height):
            cell_tab = []
            for y in range(width):
                # Déterminer si c'est une bordure
                is_border = i == 0 or i == (height - 1) or y == 0 or y == (width - 1)

                # Appliquer le ratio horizontal
                for _ in range(char_ratio):
                    if is_border:
                        cell_tab.append((CellType.WALL, Printer.RED))
                    else:
                        cell_tab.append((CellType.WALL, Printer.GREEN))

            grid.append(cell_tab)

        return grid

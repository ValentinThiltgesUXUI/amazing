import os
import time
from enum import Enum

CHAR_RATIO = 2


class CellType(Enum):
    """Types de cellules pour le labyrinthe"""

    WALL = "█"
    POINT = "█"
    SPACE = " "


class Printer:
    RESET = "\033[0m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLACK = "\033[0;30m"
    LIGHT_GRAY = "\033[0;37m"

    def __init__(self) -> None:
        pass

    @staticmethod
    def paint(ct: CellType, color: str) -> None:
        print(f"{color}{ct.value}{Printer.RESET}", end="")

    @staticmethod
    def clear_screen() -> None:
        """Clear screen"""
        os.system("clear" if os.name == "posix" else "cls")

    # ── Grille logique ──────────────────────────────────────────────

    @staticmethod
    def create_logical_grid(width: int, height: int) -> list[list[tuple | None]]:
        """
        Crée une grille logique (1 cellule = 1 case du labyrinthe).
        Les bordures sont des murs, l'intérieur est None (indéterminé).

        Args:
            width:  Largeur en nombre de cellules
            height: Hauteur en nombre de cellules

        Returns:
            Grille logique [height][width] de (CellType, color) | None
        """
        grid: list[list[tuple | None]] = []
        for y in range(height):
            row: list[tuple | None] = []
            for x in range(width):
                is_border = y == 0 or y == height - 1 or x == 0 or x == width - 1
                if is_border:
                    row.append((CellType.WALL, Printer.LIGHT_GRAY))
                else:
                    row.append(None)
            grid.append(row)
        return grid

    @staticmethod
    def set_cell(
        grid: list[list[tuple | None]], x: int, y: int, ct: CellType, color: str
    ) -> None:
        """
        Modifie une cellule de la grille logique en place.

        Args:
            grid:  Grille logique
            x:     Colonne (coord logique)
            y:     Ligne  (coord logique)
            ct:    Type de cellule
            color: Couleur
        """
        if 0 <= y < len(grid) and 0 <= x < len(grid[y]):
            grid[y][x] = (ct, color)

    # ── Conversion logique → graphique ──────────────────────────────

    @staticmethod
    def to_graphical_grid(
        logical: list[list[tuple | None]],
    ) -> list[list[tuple | None]]:
        """
        Convertit la grille logique en grille graphique prête à l'affichage.
        Chaque cellule logique est dupliquée CHAR_RATIO fois horizontalement.

        Args:
            logical: Grille logique [height][width]

        Returns:
            Grille graphique [height][width * CHAR_RATIO]
        """
        graphical: list[list[tuple | None]] = []
        for row in logical:
            gfx_row: list[tuple | None] = []
            for cell in row:
                for _ in range(CHAR_RATIO):
                    gfx_row.append(cell)
            graphical.append(gfx_row)
        return graphical

    # ── Affichage ───────────────────────────────────────────────────

    @staticmethod
    def display_grid(logical: list[list[tuple | None]], delay: float = 0.15) -> None:
        """
        Convertit la grille logique en graphique puis l'affiche au terminal.

        Args:
            logical: Grille logique
            delay:   Pause après affichage (secondes)
        """
        graphical = Printer.to_graphical_grid(logical)
        Printer.clear_screen()
        for row in graphical:
            for cell in row:
                if cell is None:
                    Printer.paint(CellType.SPACE, Printer.LIGHT_GRAY)
                else:
                    cell_type, color = cell
                    Printer.paint(cell_type, color)
            print()
        time.sleep(delay)

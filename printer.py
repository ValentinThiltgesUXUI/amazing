import os
import time
from enum import Enum

CHAR_RATIO = 2


class CellType(Enum):
    """Types de cellules pour le labyrinthe"""

    WALL = "█"
    POINT = "█"
    SPACE = "█"


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
        Crée une grille logique avec alternance murs / cellules jouables.
        Pour un labyrinthe de width × height cellules jouables,
        la grille fait (2*width + 1) × (2*height + 1).

        Les positions impaires (1,1), (1,3), (3,1)... sont les cellules
        jouables (None = non visitées). Tout le reste est mur.

        Args:
            width:  Nombre de cellules jouables en largeur
            height: Nombre de cellules jouables en hauteur

        Returns:
            Grille logique [(2h+1)][(2w+1)] de (CellType, color) | None
        """
        grid_w = 2 * width + 1
        grid_h = 2 * height + 1
        grid: list[list[tuple | None]] = []
        for y in range(grid_h):
            row: list[tuple | None] = []
            for x in range(grid_w):
                if x % 2 == 1 and y % 2 == 1:
                    row.append(None)
                else:
                    row.append((CellType.WALL, Printer.LIGHT_GRAY))
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
        Construit le frame entier en un seul string pour réduire le flickering.
        """
        graphical = Printer.to_graphical_grid(logical)
        lines = []
        for row in graphical:
            line = ""
            for cell in row:
                if cell is None:
                    line += f"{Printer.LIGHT_GRAY}{CellType.SPACE.value}{Printer.RESET}"
                else:
                    ct, color = cell
                    line += f"{color}{ct.value}{Printer.RESET}"
            lines.append(line)
        frame = "\n".join(lines)
        print(f"\033[H{frame}\033[J", end="", flush=True)
        time.sleep(delay)

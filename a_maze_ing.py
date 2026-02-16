import algorithm
import config_utils
from printer import CellType, Printer

file = "config.txt"

# La grille logique a une bordure de 1 cellule de large.
# Les coords config (0,0 = première case jouable) doivent être décalées.
BORDER = 1


def to_grid_coord(coord: tuple[int, int]) -> tuple[int, int]:
    """Convertit des coordonnées config en coordonnées grille logique."""
    return coord[0] + BORDER, coord[1] + BORDER


def main() -> None:
    parsing = config_utils.Parser(file)
    printer = Printer()
    parsing.init_list()
    width = int(parsing.get_value("WIDTH"))
    height = int(parsing.get_value("HEIGHT"))
    seed = int(parsing.get_value("SEED"))
    entry = to_grid_coord(parsing.extract_coord(parsing.get_value("ENTRY")))
    exit_ = to_grid_coord(parsing.extract_coord(parsing.get_value("EXIT")))

    # Créer la grille logique (coords simples, sans ratio)
    grid = printer.create_logical_grid(width, height)

    # Marquer l'entrée et la sortie (coords logiques)
    printer.set_cell(grid, entry[0], entry[1], CellType.POINT, Printer.RED)
    printer.set_cell(grid, exit_[0], exit_[1], CellType.POINT, Printer.GREEN)

    # Générer le labyrinthe
    for grid in algorithm.generate_maze(grid, seed, entry, exit_):
        printer.display_grid(grid, delay=0.10)

    printer.display_grid(grid)


if __name__ == "__main__":
    main()

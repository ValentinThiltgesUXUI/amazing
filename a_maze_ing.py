import algorithm
import config_utils
from printer import CellType, Printer
from c_error import OutOfBound, check_bounds


file = "config.txt"

# La grille logique alterne murs et cellules jouables.
# Les cellules jouables sont aux positions impaires : (2*x+1, 2*y+1).


def to_grid_coord(coord: tuple[int, int]) -> tuple[int, int]:
    """Convertit des coordonnées config (0,0 = première case jouable)
    en coordonnées grille logique (position impaire)."""
    return coord[0] * 2 + 1, coord[1] * 2 + 1


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

    # D'abord vérifier que l'entrée et la sortie dans la grille
    try:
        check_bounds(grid, entry)
        check_bounds(grid, exit_)
    except OutOfBound as coords:
        print(f"Coordinates {coords} out of bound, choose something else")
        return

    # Marquer l'entrée (avant génération, le DFS part de là)
    printer.set_cell(grid, entry[0], entry[1], CellType.POINT, Printer.RED)

    # Générer le labyrinthe (exit_ reste None pour que le DFS puisse
    display_mode = parsing.get_value("DISPLAY_MODE") or "animation"

    Printer.clear_screen()
    if display_mode == "animation":
        for updated_grid in algorithm.generate_maze(grid, seed, entry, exit_):
            printer.display_grid(updated_grid, delay=0.05)
            grid = updated_grid
    else:
        for updated_grid in algorithm.generate_maze(grid, seed, entry, exit_):
            grid = updated_grid

    # Marquer la sortie après génération
    printer.set_cell(grid, exit_[0], exit_[1], CellType.POINT, Printer.GREEN)
    printer.display_grid(grid)
    print("")


if __name__ == "__main__":
    main()

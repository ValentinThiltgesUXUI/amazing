import algorithm
import config_utils
import random_generator
from printer import CellType, Printer

file = "config.txt"


def main() -> None:
    parsing = config_utils.Parser(file)
    printer = Printer()
    parsing.init_list()
    width = int(parsing.get_value("WIDTH"))
    height = int(parsing.get_value("HEIGHT"))
    seed = parsing.get_value("SEED")
    entry = parsing.extract_coord(parsing.get_value("ENTRY"))
    exit_ = parsing.extract_coord(parsing.get_value("EXIT"))
    generating = True

    # Créer la grille logique (coords simples, sans ratio)
    grid = printer.create_logical_grid(width, height)

    # Marquer l'entrée et la sortie (coords logiques)
    printer.set_cell(grid, entry[0], entry[1], CellType.POINT, Printer.RED)
    printer.set_cell(grid, exit_[0], exit_[1], CellType.POINT, Printer.GREEN)

    # Générer le labyrinthe
    grid = algorithm.generate_maze(
        grid, width, height, seed, entry=entry, exit_=exit_
    )

    while generating:
        printer.display_grid(grid)
    print("\n=== END ===\n")


if __name__ == "__main__":
    main()

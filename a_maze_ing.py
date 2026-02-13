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

    print("=== CONFIG FILE ===")
    print(f"Width: {width}\nHeight: {height}\nSeed: {seed}\n")

    tab1 = random_generator.generate_random_s(seed, 100)

    # Créer la grille avec ratio automatique
    grid = printer.create_square_grid(width, height)

    printer.display_grid(grid)
    print("\n")


if __name__ == "__main__":
    main()

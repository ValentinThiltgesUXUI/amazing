import config_utils
from printer import Printer, CellType
import random_generator

file = "config.txt"


def main() -> None:
    parsing = config_utils.Parser(file)
    printer = Printer()
    parsing.init_list()
    width = parsing.get_value("WIDTH")
    height = parsing.get_value("HEIGHT")
    seed = parsing.get_value("SEED")
    print("=== CONFIG FILE ===")
    print(f"Width: {width}\nHeight: {height}\nSeed: {seed}\n")
    tab1 = random_generator.generate_random_s(seed, 100)
    grid = []
    cell_tab = []
    while tab1:
        while tab1:
            cell_tab.append((CellType.WALL, Printer.RED))
        grid.append(cell_tab)
    printer.display_grid(grid)
    print("\n")


if __name__ == "__main__":
    main()

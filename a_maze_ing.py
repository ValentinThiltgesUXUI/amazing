import config_utils
import random_generator

file = "config.txt"


def main():
    parsing = config_utils.Parser(file)
    parsing.init_list()
    width = parsing.get_value("WIDTH")
    height = parsing.get_value("HEIGHT")
    seed = parsing.get_value("SEED")
    print("=== CONFIG FILE ===")
    print(f"Width: {width}\nHeight: {height}\nSeed: {seed}\n")
    tab1 = random_generator.generate_random_s(seed)
    tab2 = random_generator.generate_random_s(seed)
    print(tab1, tab2)


if __name__ == "__main__":
    main()

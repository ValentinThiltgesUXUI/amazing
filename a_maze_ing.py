import config_utils

file = "config.txt"


def main():
    parsing = config_utils.Parser(file)
    parsing.init_list()
    parsing.get_value("WIDTH")


if __name__ == "__main__":
    main()

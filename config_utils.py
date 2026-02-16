# import typing


class Parser:
    def __init__(self, file: str = "config.txt") -> None:
        self.file = file

    @staticmethod
    def verify_first(str: str) -> bool:
        # First caracter is not a commentary / newline
        # -> return True
        # else -> return False
        caracters_list = ["#", "\n"]
        if str[0] not in caracters_list:
            return True
        return False

    @staticmethod
    def separate(string: str) -> tuple[list[str], list[str]]:
        # Separate key from content
        # Return a organised tuple
        index = 0
        for i, char in enumerate(string):
            if char == "=":
                index = i
        keys = []
        keys.append(string[:index])
        contents = []
        contents.append(string[index + 1 :])
        return (keys, contents)

    @staticmethod
    def extract_coord(string: str):
        temp = string.split(",")
        result: tuple[int, int] = int(temp[0])+1, int(temp[1])+1
        return result

    def get_list_from_file(self) -> list[str]:
        # Get the raw list (key=content)
        fd = open(self.file, "r")
        line = fd.readline()
        lines = []
        while line:
            if self.verify_first(line[0]):
                lines.append(line.strip())
            line = fd.readline()
        fd.close()
        return lines

    def init_list(self) -> None:
        # Set the list of tuple as self.separated
        # 0 : key
        # 1 : content
        lst = self.get_list_from_file()
        separated = []
        for i in lst:
            separated.append(self.separate(i))
        self.separated = separated

    def get_value(self, key: str) -> str:
        # Search the key in list and return the value
        lst = self.separated
        for i in lst:
            if i[0][0] == key:
                return i[1][0]
        return ""

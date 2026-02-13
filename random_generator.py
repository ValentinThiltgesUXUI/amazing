import random


def generate_random_s(s: str, num: int = 6) -> list[int]:
    random.seed(s)
    num_mult = num * 10
    return random.sample(range(1, num_mult), num)

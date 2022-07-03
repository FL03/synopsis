import random
import string

from synopsis.data.models.users import Slip


def create_random_string(n: int = 12) -> str:
    options = string.ascii_uppercase
    return ''.join([random.choice(options) for _ in range(n)])


def rand_option(*args):
    return args[random.randint(0, len(args) - 1)]


def rand_float(a: int, b: int, precision=2) -> float:
    return round(random.randint(a, b) + random.random(), precision)


def generate_entries(m: int = 100):
    classifications = ["Server", "Server Assistant", "Host", "Bartender"]
    contexts = ["AM", "MID", "PM"]
    data = [
        Slip(
            id=i,
            account=create_random_string(random.randint(8, 16)),
            classification=rand_option(*classifications),
            duration=rand_float(4, 12, 2),
            context=rand_option(*contexts),
            sales=rand_float(400, 1200, 2)
        )
        for i in range(1, m+1)
    ]
    return data[:]

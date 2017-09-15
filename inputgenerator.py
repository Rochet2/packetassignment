import random
import string

lostindicator = "_"

assert isinstance(lostindicator, str), "lostindicator must be a string"
assert len(lostindicator) == 1, "lostindicator length must be 1"


def randomstring(length):
    rand = random.Random()
    rand.seed(1)
    letters = string.ascii_letters.replace(lostindicator, "")
    return ''.join(rand.choice(letters) for i in range(length))

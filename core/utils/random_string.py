import random
import string


def get_random_string(length):
    """
    Generate a random string with the given length
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def get_random_hash():
    """
    Generate a random string hash
    """
    hashstring = random.getrandbits(32)
    return "%08x" % (hashstring,)

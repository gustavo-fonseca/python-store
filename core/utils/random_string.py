import random
import string


def get_random_string(length):
    """
    Generate a random string with the given length
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

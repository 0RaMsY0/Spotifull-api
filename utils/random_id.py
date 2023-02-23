import random
import string


def random_id() -> str:
    """
        return a random string id
    """
    ID = ""
    
    ALPHABET = string.ascii_lowercase + string.ascii_uppercase
    for i in range(10):
        ID += random.choice(ALPHABET)
    
    return ID

import random
import string

def random_id(length: int) -> str:
    """
        return a random string id
    """
    from main import DATABASE

    ID = ""
    USED_IDS = [_id[0] for _id in DATABASE.get_sessions()]
    ALPHABET = string.ascii_lowercase + string.ascii_uppercase

    while True:
        for i in range(length):
            ID += random.choice(ALPHABET)
        if ID not in USED_IDS:
            break
        else:
            ID = ""
 
    return ID

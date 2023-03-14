
def iter_file(file_path: str):
    """
        Iterate thro a given file
    """
    with open(file_path, "rb") as _file:
        yield from _file

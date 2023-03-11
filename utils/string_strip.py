import re

def string_strip(text: str):
    """
        Clean text from colors and other
        ANSI escape sequences.
    """
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', text).strip()

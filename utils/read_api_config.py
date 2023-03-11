import json

def read_api_config() -> dict:
    """
        Returns the api config
    """
    api_config = None

    with open("conf/api-conf.json", "r") as conf:
        api_config = json.load(conf)

    return api_config

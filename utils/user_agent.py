import random

def ran_user_agent():
    """
        Returns a random user-agent
    """
    USER_AGENT = ""
    USER_AGENT_FILES = ["chrome.txt", "firefox.txt", "opera.txt", "safari.txt"]

    with open(f"./user-agents/{random.choice(USER_AGENT_FILES)}", "r") as user_agents:
        USER_AGENT = random.choice(user_agents.readlines())
    
    return USER_AGENT

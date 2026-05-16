import json
import os

MEMORY_FILE = "brain_memory.json"


DEFAULT_MEMORY = {
    "adaptation": {
        "successful_actions": 0,
        "failed_actions": 0,
        "adaptation_score": 0
    },
    "goals": [],
    "experiences": []
}


def load_persistent_memory():

    if not os.path.exists(MEMORY_FILE):

        save_persistent_memory(DEFAULT_MEMORY)

        return DEFAULT_MEMORY

    try:

        with open(MEMORY_FILE, "r") as f:

            return json.load(f)

    except:

        return DEFAULT_MEMORY


def save_persistent_memory(data):

    with open(MEMORY_FILE, "w") as f:

        json.dump(data, f, indent=4)


def add_experience(exp):

    data = load_persistent_memory()

    data["experiences"].append(exp)

    save_persistent_memory(data)

    return data


def update_adaptation_memory(memory):

    data = load_persistent_memory()

    data["adaptation"] = memory

    save_persistent_memory(data)


def add_goal(goal):

    data = load_persistent_memory()

    data["goals"].append(goal)

    save_persistent_memory(data)

import json
import os

MEMORY_FILE = "core/right_lob/memory.json"

memory = {
    "usage": {},
    "score": {},
    "history": []
}


def load_memory():
    global memory
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                memory.update(json.load(f))
        except:
            memory = {"usage": {}, "score": {}, "history": []}


def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def log_usage(cmd):
    cmd = cmd.lower().strip()

    memory["usage"][cmd] = memory["usage"].get(cmd, 0) + 1
    memory["score"][cmd] = memory["score"].get(cmd, 0) + 1

    memory["history"].append(cmd)

    if len(memory["history"]) > 200:
        memory["history"] = memory["history"][-200:]

    save_memory()


def is_hot_command(cmd):
    cmd = cmd.lower().strip()
    return memory["usage"].get(cmd, 0) >= 3


def get_score(cmd):
    return memory["score"].get(cmd, 0)


def decay_scores():
    """
    Low usage commands slowly lose value
    """
    for k in list(memory["score"].keys()):
        memory["score"][k] *= 0.95


def get_top_commands(limit=5):
    return sorted(memory["score"].items(), key=lambda x: x[1], reverse=True)[:limit]

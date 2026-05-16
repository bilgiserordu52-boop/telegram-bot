# core/core_v2/loader.py

from core.core_v2.brain import register


def load_features():

    def ping():
        return "pong-v2"

    def echo(text=""):
        return text

    def system():
        return {"status": "v2 active"}

    register("ping", ping)
    register("echo", echo)
    register("system", system)

    return True


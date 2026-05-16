# core/core_v2/engine.py

from core.core_v2.brain import execute

def run(cmd, *args, **kwargs):
    return execute(cmd, *args, **kwargs)

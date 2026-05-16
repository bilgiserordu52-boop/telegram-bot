# deploy/engine.py

import subprocess
import json
from datetime import datetime

DEPLOY_LOG = "storage/deploy_history.json"


def _load_log():
    try:
        with open(DEPLOY_LOG, "r") as f:
            return json.load(f)
    except:
        return []


def _save_log(data):
    with open(DEPLOY_LOG, "w") as f:
        json.dump(data, f, indent=2)


def log_deploy(name, result):
    data = _load_log()

    data.append({
        "name": name,
        "result": str(result),
        "time": str(datetime.now())
    })

    _save_log(data)


async def deploy_module(name="full", message=None):
    """
    SADECE GİT PULL YAPAR
    ASLA BOT MESSAGE BASMAZ
    """

    try:
        result = subprocess.check_output(
            ["git", "pull"],
            stderr=subprocess.STDOUT
        ).decode()

        log_deploy(name, result)

        # SADECE RETURN
        return result

    except Exception as e:
        error = str(e)

        log_deploy(name, error)

        return error

# =========================
# PATCH API LAYER
# =========================

from core.patch.engine import patch


# =========================
# SIMPLE COMMAND INTERFACE
# =========================
def run_patch(command):

    """
    command format:

    {
        "file": "run.py",
        "search": "old code",
        "replace": "new code"
    }
    """

    file = command.get("file")
    search = command.get("search")
    replace = command.get("replace")

    anchor = command.get("anchor")
    code = command.get("code")

    return patch(
        file_path=file,
        search=search,
        replace=replace,
        anchor=anchor,
        code=code
    )

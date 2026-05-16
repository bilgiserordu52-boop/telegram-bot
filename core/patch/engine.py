# =========================
# PATCH ENGINE v1 FINAL SAFE
# =========================

import os
from datetime import datetime


def apply_patch(file_path, search=None, replace=None, anchor=None, code=None):

    if not os.path.exists(file_path):
        return {"status": "error", "msg": "file not found"}

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # -------------------------
    # SEARCH & REPLACE MODE
    # -------------------------
    if search and replace:

        if search not in content:
            return {"status": "error", "msg": "search not found"}

        content = content.replace(search, replace)

    # -------------------------
    # INJECT MODE
    # -------------------------
    if anchor and code:

        lines = content.split("\n")
        new_lines = []
        inserted = False

        for line in lines:

            new_lines.append(line)

            if anchor in line and not inserted:
                new_lines.append(code)
                inserted = True

        content = "\n".join(new_lines)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return {
        "status": "ok",
        "file": file_path,
        "time": str(datetime.now())
    }

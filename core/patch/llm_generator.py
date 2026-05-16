# =========================
# LLM AI PATCH GENERATOR v2
# =========================

import os
import json
import requests

from core.patch.engine import patch


# =========================
# SIMPLE LLM CALL (OPENAI / LOCAL COMPATIBLE)
# =========================
def call_llm(prompt):

    api_key = os.getenv("LLM_API_KEY")

    if not api_key:
        return "ERROR: LLM_API_KEY not set"

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "You are a Python system engineer. Output ONLY JSON patch instructions."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        return None

    return response.json()["choices"][0]["message"]["content"]


# =========================
# PARSE AI OUTPUT
# =========================
def parse_patch(ai_output):

    try:
        return json.loads(ai_output)
    except:
        return None


# =========================
# MAIN AI PATCH FUNCTION
# =========================
def apply_llm_patch(user_request):

    prompt = f"""
    Convert this request into a PATCH instruction:

    "{user_request}"

    Return ONLY JSON in this format:

    {{
        "file": "path/to/file.py",
        "search": "old_code_optional",
        "replace": "new_code_optional",
        "anchor": "optional_anchor",
        "code": "optional_code_block"
    }}
    """

    ai_output = call_llm(prompt)

    if not ai_output:
        return {"status": "error", "message": "LLM failed"}

    command = parse_patch(ai_output)

    if not command:
        return {"status": "error", "message": "Invalid AI output"}

    return patch(
        file_path=command.get("file"),
        search=command.get("search"),
        replace=command.get("replace"),
        anchor=command.get("anchor"),
        code=command.get("code")
    )

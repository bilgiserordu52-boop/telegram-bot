import base64
import requests

def headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

def push_to_github(repo, branch, token, file_path, code, message, version):
    # 1) dosya bilgisini çek (SHA gerekli)
    url = f"https://api.github.com/repos/{repo}/contents/{file_path}?ref={branch}"

    try:
        r = requests.get(url, headers=headers(token), timeout=10)
        data = r.json()

        if "sha" not in data:
            return False, f"SHA ERROR: {data}"

        sha = data["sha"]

        # 2) encode
        encoded = base64.b64encode(code.encode()).decode()

        # 3) push payload
        payload = {
            "message": f"{message} | v:{version}",
            "content": encoded,
            "sha": sha,
            "branch": branch
        }

        put_url = f"https://api.github.com/repos/{repo}/contents/{file_path}"

        res = requests.put(put_url, json=payload, headers=headers(token), timeout=10)

        if res.status_code not in [200, 201]:
            return False, res.json()

        return True, "OK"

    except Exception as e:
        return False, str(e)

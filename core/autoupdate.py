import subprocess

def run_update():

    result = subprocess.run(
        ["git", "pull"],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    return result.stdout

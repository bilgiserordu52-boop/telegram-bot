import time

START_TIME = time.time()


def uptime():

    seconds = int(time.time() - START_TIME)

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    sec = seconds % 60

    return f"{hours}h {minutes}m {sec}s"

from core.right_lob.actions import execute_action
from core.right_lob.persistent import add_goal

GOALS = []

TASK_QUEUE = []


def create_goal(goal):

    GOALS.append(goal)

    # 🧠 SAVE GOAL
    add_goal(goal)

    TASK_QUEUE.append({
        "goal": goal,
        "status": "pending"
    })

    return {
        "goal_created": goal,
        "queue_size": len(TASK_QUEUE)
    }


def get_goals():
    return GOALS


def get_tasks():
    return TASK_QUEUE


def process_next_task():

    if not TASK_QUEUE:

        return {
            "status": "empty",
            "message": "No tasks remaining"
        }

    task = TASK_QUEUE.pop(0)

    task["status"] = "processing"

    action_result = execute_action(task)

    task["status"] = "completed"

    return {
        "processed_task": task,
        "action_result": action_result,
        "remaining_tasks": len(TASK_QUEUE)
    }

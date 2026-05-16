from core.features.loader import load_features
from core.features.registry import get_features

from core.right_lob.evolve import evolve_feature
from core.right_lob.memory import load_memory, log_usage
from core.right_lob.semantic import semantic_brain
from core.right_lob.context import add_context
from core.right_lob.self_improve import evaluate_response
from core.right_lob.recursive import recursive_reflection
from core.right_lob.planner import planner
from core.right_lob.goals import process_next_task
from core.right_lob.adaptation import adapt_from_result
from core.right_lob.strategy import strategic_decision

from core.right_lob.cognition import (
    remember_short,
    remember_long,
    get_memory_state,
    cognitive_priority
)

from core.brain import Brain

brain = Brain()

def execute(input_text):
    return brain.think(input_text)

from core.right_lob.executive import executive_control

from core.right_lob.agent import agent

load_features()
load_memory()


def finalize_response(response):

    response["self_improve"] = evaluate_response(response)

    reflection = recursive_reflection(response)
    response["reflection"] = reflection

    if reflection["needs_retry"]:

        improved = reflection["improved_response"]
        improved["self_improve"] = evaluate_response(improved)
        improved["recursive_upgrade"] = True

        return improved

    return response


def execute(cmd):

    cmd = cmd.strip().lower()

    if cmd.startswith("/"):
        cmd = cmd[1:]

    remember_short(cmd)
    remember_long(cmd)

    memory_state = get_memory_state()
    cognition = cognitive_priority(cmd)
    executive = executive_control(cmd, cognition)

    add_context("user", cmd)
    log_usage(cmd)

    strategy = strategic_decision(cmd)

    # 🧠 PHASE 20 TOOL AGENT LAYER
    agent_result = agent.execute(cmd)

    if agent_result:

        return finalize_response({
            "status": "agent_execution",
            "response": "🧠 Real tool agent executed",
            "agent": agent_result,
            "strategy": strategy,
            "cognition": cognition,
            "executive": executive,
            "memory": memory_state
        })

    # 🧠 autonomous planner
    autonomous = planner.analyze(cmd)

    if autonomous:

        return finalize_response({
            "status": "autonomous",
            "response": "🧠 Autonomous planning active",
            "goal_system": autonomous,
            "strategy": strategy,
            "cognition": cognition,
            "executive": executive,
            "memory": memory_state
        })

    # task system
    if cmd == "process_tasks":

        result = process_next_task()

        adaptation = None

        if result.get("action_result"):
            adaptation = adapt_from_result(result["action_result"])

        return finalize_response({
            "status": "task_processing",
            "result": result,
            "adaptation": adaptation,
            "strategy": strategy,
            "cognition": cognition,
            "executive": executive,
            "memory": memory_state
        })

    thought = semantic_brain.think(cmd)

    decision = thought["decision"]
    analysis = thought["analysis"]

    features = get_features()

    if executive["mode"] == "deep":

        return finalize_response({
            "status": "deep_reasoning",
            "response": f"🧠 Deep cognition active: {cmd}",
            "depth": executive["depth"],
            "strategy": strategy,
            "cognition": cognition,
            "executive": executive,
            "memory": memory_state
        })

    if decision == "EXPLAIN_MODE":

        return finalize_response({
            "status": "ok",
            "mode": "explain",
            "response": f"📖 Açıklama: {cmd}",
            "analysis": analysis,
            "strategy": strategy,
            "cognition": cognition,
            "executive": executive,
            "memory": memory_state
        })

    if decision == "TEACH_MODE":

        return finalize_response({
            "status": "ok",
            "mode": "teach",
            "response": f"📘 Öğrenme: {cmd}",
            "analysis": analysis,
            "strategy": strategy,
            "cognition": cognition,
            "executive": executive,
            "memory": memory_state
        })

    if decision == "REASON_MODE":

        return finalize_response({
            "status": "ok",
            "mode": "reason",
            "response": f"🧠 Reasoning: {cmd}",
            "analysis": analysis,
            "strategy": strategy,
            "cognition": cognition,
            "executive": executive,
            "memory": memory_state
        })

    if cmd in features:

        return finalize_response({
            **features[cmd](),
            "brain": decision,
            "strategy": strategy,
            "cognition": cognition,
            "executive": executive,
            "memory": memory_state
        })

    evolve_feature(cmd)
    features = get_features()

    if cmd in features:

        return finalize_response({
            **features[cmd](),
            "brain": "AUTO_EVOLVE",
            "strategy": strategy,
            "cognition": cognition,
            "executive": executive,
            "memory": memory_state
        })

    return finalize_response({
        "status": "error",
        "message": "phase20 failed",
        "strategy": strategy,
        "cognition": cognition,
        "executive": executive,
        "memory": memory_state
    })

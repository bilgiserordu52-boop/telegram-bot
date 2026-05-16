from core.right_lob.memory import get_score
from core.right_lob.context import get_context


class SemanticBrain:

    def parse(self, cmd):
        cmd = cmd.lower().strip()
        score = get_score(cmd)

        context = get_context()

        # 🧠 CONTEXT AWARENESS
        last_user = None
        if context:
            for msg in reversed(context):
                if msg["role"] == "user":
                    last_user = msg["text"]
                    break

        # INTENT DETECTION
        if cmd.startswith("/"):
            intent = "system_command"

        elif "neden" in cmd:
            intent = "reasoning_question"

        elif "nasıl" in cmd or "how" in cmd:
            intent = "learning_question"

        elif "nedir" in cmd or "what" in cmd:
            intent = "definition"

        elif "_" in cmd:
            intent = "feature_request"

        else:
            intent = "general"

        return {
            "cmd": cmd,
            "intent": intent,
            "score": score,
            "last_user": last_user,
            "context_size": len(context)
        }

    def reason(self, data):
        intent = data["intent"]
        score = data["score"]

        # 🧠 CONTEXT-BASED DECISION

        if intent == "reasoning_question":
            return "REASON_MODE"

        if intent == "learning_question":
            return "TEACH_MODE"

        if intent == "definition":
            return "EXPLAIN_MODE"

        if intent == "system_command":
            return "EXECUTE_MODE"

        if intent == "feature_request":
            return "EVOLVE_MODE"

        if score >= 5:
            return "PRIORITY_EXECUTE"

        return "NORMAL_EXECUTE"

    def think(self, cmd):
        data = self.parse(cmd)
        decision = self.reason(data)

        return {
            "analysis": data,
            "decision": decision
        }


semantic_brain = SemanticBrain()

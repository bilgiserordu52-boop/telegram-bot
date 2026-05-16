from core.right_lob.memory import get_score


class Brain:

    def analyze(self, cmd):
        cmd = cmd.lower().strip()

        score = get_score(cmd)

        if cmd.startswith("/"):
            intent = "command"
        elif len(cmd) <= 3:
            intent = "short_query"
        elif "_" in cmd:
            intent = "feature_request"
        else:
            intent = "general"

        return {
            "cmd": cmd,
            "intent": intent,
            "score": score
        }

    def decide(self, analysis):
        intent = analysis["intent"]
        score = analysis["score"]

        if score >= 5:
            return "HOT_EXECUTE"

        if intent == "feature_request":
            return "EVOLVE_EXECUTE"

        if intent == "short_query":
            return "DIRECT_EXECUTE"

        return "SAFE_EXECUTE"

    def think(self, cmd):
        analysis = self.analyze(cmd)
        decision = self.decide(analysis)

        return {
            "analysis": analysis,
            "decision": decision
        }


brain = Brain()

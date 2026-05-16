from core.right_lob.goals import create_goal


class AutonomousPlanner:

    def analyze(self, cmd):

        cmd = cmd.lower()

        # 🧠 AUTONOMOUS GOAL DETECTION

        if "öğren" in cmd:
            return create_goal("increase_learning")

        if "geliş" in cmd:
            return create_goal("self_improvement")

        if "hızlan" in cmd:
            return create_goal("performance_optimization")

        return None


planner = AutonomousPlanner()

class Brain:
    def __init__(self):
        self.memory = []
        self.state = {
            "focus": 1,
            "curiosity": 1,
            "confidence": 1
        }

    def think(self, input_text, core_execute=None, agent=None):
        self.memory.append(input_text)

        core_result = None
        agent_result = None

        if core_execute:
            core_result = core_execute(input_text)

        if agent:
            agent_result = agent(input_text)

        return {
            "status": "brain_active",
            "input": input_text,
            "core": core_result,
            "agent": agent_result,
            "memory": self.memory[-10:],
            "state": self.state
        }

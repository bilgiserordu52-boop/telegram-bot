from core.right_lob.tools import detect_tool, execute_tool


class AgentSystem:

    def think(self, cmd):

        tool = detect_tool(cmd)

        if not tool:
            return None

        return {
            "tool": tool,
            "plan": [
                "parse_input",
                "select_tool",
                "execute_tool",
                "validate_output",
                "return_result"
            ]
        }

    def execute(self, cmd):

        thought = self.think(cmd)

        if not thought:
            return None

        tool = thought["tool"]

        result = execute_tool(tool, cmd)

        return {
            "agent_mode": True,
            "tool": tool,
            "plan": thought["plan"],
            "result": result,
            "chain_depth": 1
        }


agent = AgentSystem()

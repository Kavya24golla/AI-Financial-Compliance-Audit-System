from __future__ import annotations

class AgentController:
    def __init__(self, agents: dict):
        self.agents = agents

    def get(self, name: str):
        return self.agents[name]

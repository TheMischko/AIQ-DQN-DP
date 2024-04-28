from genetics.agents_ref.AgentReference import AgentReference


class Random(AgentReference):
    def get_test_agent_name(self):
        return "Random"

    def get_generators(self):
        return []

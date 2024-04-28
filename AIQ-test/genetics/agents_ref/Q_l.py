import random

from genetics.agents_ref.AgentReference import AgentReference


class Q_l(AgentReference):
    def get_test_agent_name(self):
        return "Q_l"

    def get_generators(self):
        return [
            lambda: random.randint(1, 100) / 100, # init_Q
            lambda: random.randint(1, 100) / 100, # Lambda
            lambda: random.randint(1, 100) / 100, # alpha
            lambda: random.randint(1, 100) / 100, # epsilon
            lambda: random.randint(1, 100) / 100, # gamma
        ]

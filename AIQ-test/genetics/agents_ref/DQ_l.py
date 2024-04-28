import random
import numpy as np

from genetics.agents_ref.AgentReference import AgentReference


class DQ_l(AgentReference):
    def get_test_agent_name(self):
        return "DQ_l"

    def get_generators(self):
        use_eligiblity_traces = random.random() > 0.95
        return [
            # Learning rate [0.01, 0.00001]
            lambda: np.random.choice(np.linspace(0.01, 0.00001, 200)),
            # Gamma value [0.01, 0.99]
            lambda: np.random.choice(np.linspace(0.01, 0.99, 100)),
            # Batch size in size of 2^n for n [2, 9] generating numbers
            # 4, 8, 16, 32, 64, 128, 256, 512
            lambda: 2 ** (random.randint(2, 9)),
            # Epsilon
            lambda: 1,
            # Epsilon decay [100, 10000]
            lambda: random.randint(1, 100) * 100,
            # Size of neural net layer 1 [16, 256]
            lambda: random.randint(1, 16) * 16,
            # Size of neural net layer 2 [16, 256]
            lambda: random.randint(1, 16) * 16,
            # Size of neural net layer 3 [16, 256] or 0
            lambda: random.randint(1, 16) * 16 if random.random() > 0.35 else 0,
            # RMSProp = 0 or ADAM = 1
            lambda: 1 if random.random() > 0.5 else 0,
            # history length
            lambda: random.randint(0, 4),
            # Lambda
            lambda: np.random.choice(np.linspace(0.01, 0.99, 100)) if use_eligiblity_traces else 0,
            # Eligibility traces handling method
            lambda: random.choice([0, 1, 2]) if use_eligiblity_traces else 0
        ]
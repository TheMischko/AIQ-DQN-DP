from genetics.context.TestContext import Context
from genetics.agents_ref.AgentReference import AgentReference
from genetics.eval_function import eval_function


class Individual:
    def __init__(self, initial_genome: [float], agent_name: str, context: Context):
        """
        Individual chromosome for genetic test that can evaluate self via Evaluation function.
        :param initial_genome: Initial genome.
        :param agent_name: AIQ agent reference.
        :param context: Settings about the testing.
        """
        self.genome = initial_genome
        self.agent = agent_name
        self.context = context
        self.value = None
        self.eval_function = eval_function

    def eval(self):
        """
        Get evaluation of chromosome of this individual.

        Value is cached if the evaluation is not running for the first time.
        """
        if self.value is None:
            self.value = self.eval_function(self.genome, self.agent, self.context.test_settings)
        return self.value

    def change_genome(self, new_genome):
        """
        Swap chromosome for a new value and reset its evaluation.
        """
        self.genome = new_genome
        self.value = None

    def get_genome(self):
        return self.genome

    def __str__(self):
        return "[{0}]".format(", ".join(str(g) for g in self.genome))

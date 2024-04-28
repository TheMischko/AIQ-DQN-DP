import copy
import random
from typing import List, Type

from genetics.Individual import Individual
from genetics.agents_ref.AgentReference import AgentReference
from genetics.context.TestContext import Context


def mutate(population: List[Type[Individual]], agent_ref: AgentReference, context: Context):
    mutated_gens = list()
    rand_gen = random.Random()
    for i in range(context.num_mutations):
        chromosome_to_mutate = copy.deepcopy(random.choice(population).get_genome())

        indices = [i for i in range(len(agent_ref.get_generators()))]
        for i in indices:
            rand_val = rand_gen.random()
            if rand_val <= context.mutation_prob:
                chromosome_to_mutate[i] = agent_ref.get_generators()[i]()

        mutated_gens.append(Individual(
            chromosome_to_mutate,
            agent_ref.get_test_agent_name(),
            context)
        )
    return mutated_gens






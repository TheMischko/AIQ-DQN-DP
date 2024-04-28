import copy
import random

from typing import List, Type

import numpy as np

from genetics.Individual import Individual
from genetics.agents_ref.AgentReference import AgentReference
from genetics.context.TestContext import Context


def crossover(best_individuals: List[Type[Individual]], agent_ref: AgentReference, context: Context):
    children = list()
    rand_gen = random.Random()
    while len(children) < context.num_crossover:
        parents_idxs = rand_gen.sample(range(len(best_individuals)), 2)
        p1 = best_individuals[parents_idxs[0]]
        p2 = best_individuals[parents_idxs[1]]

        p1_chromosome = p1.get_genome()
        p2_chromosome = p2.get_genome()
        crossover_points = sorted(rand_gen.sample(range(len(p1_chromosome)), 2))
        start, end = crossover_points

        child1 = p1_chromosome[:start] + p2_chromosome[start:end] + p1_chromosome[end:]
        child2 = p2_chromosome[:start] + p1_chromosome[start:end] + p1_chromosome[end:]

        children.append(Individual(
            child1,
            agent_ref.get_test_agent_name(),
            context
        ))
        children.append(Individual(
            child2,
            agent_ref.get_test_agent_name(),
            context
        ))
    return children[:context.num_crossover]

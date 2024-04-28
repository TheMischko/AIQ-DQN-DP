from genetics import Environment
from typing import List, Type

from genetics.Individual import Individual
from genetics.environment.crossover import crossover
from genetics.environment.mutate import mutate


def create_new_generation(environment: Environment, best_individuals: List[Type[Individual]]):
    population = list()
    population.extend(best_individuals)

    environment.debug_print("Mutating best chromosomes to create new ones.")
    mutated = mutate(
        best_individuals,
        environment.agent_ref,
        environment.context
    )
    population.extend(mutated)

    environment.debug_print("Applying crossover.")
    crossovered = crossover(
        best_individuals,
        environment.agent_ref,
        environment.context
    )
    population.extend(crossovered)

    # Remove duplicates
    for i in range(len(population)):
        contains = does_pop_contains_individual(population[i], i, population)
        if contains:
            population[i] = Individual(
                environment.agent_ref.generate_params(),
                environment.agent_ref.get_test_agent_name(),
                environment.context
            )
    return population


def does_pop_contains_individual(individual, skip_index, population):
    genome = individual.get_genome()
    for i in range(len(population)):
        if i == skip_index:
            continue
        sec_genome = population[i].get_genome()
        if genome == sec_genome:
            return True
    return False


from genetics.Individual import Individual


def initialize_population(environment, size: int, seed_population: list):
    population = get_valid_from_seed(environment, seed_population)
    num_generate = 0 if len(population) >= size else size-len(population)
    for i in range(num_generate):
        genome = environment.agent_ref.generate_params()
        population.append(Individual(
            genome,
            environment.agent_ref.get_test_agent_name(),
            environment.context
        ))
    return population


def get_valid_from_seed(environment, seed_population):
    valid = []
    for genome in seed_population:
        if len(genome) == len(environment.agent_ref.get_generators()):
            valid.append(Individual(
                genome,
                environment.agent_ref.get_test_agent_name(),
                environment.context
            ))
    return valid

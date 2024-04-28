import math
from typing import List, Type
import multiprocessing as mp

from genetics import Environment
from genetics.Individual import Individual
from genetics.environment.EvalProcess import EvalProcess


def evaluate_population(environment: Environment, population: List[Type[Individual]]):
    """
    Evaluate each chromosome from population.

    Uses multiprocessing for parallelization of the process.
    Number threads is set in self.num_agents attribute and each thread uses self.threads threads for AIQ test.
    """
    allowed_threads = environment.context.num_agents

    iterations = math.floor(environment.context.population / allowed_threads)

    population_queue = mp.Queue()
    evaluated_queue = mp.Queue()


    for individual in population:
        population_queue.put(individual)

    for i in range(iterations):
        environment.debug_print(
            "Evaluating genomes %d-%d." % ((i * allowed_threads), (i * allowed_threads) + allowed_threads - 1))
        processes = list()
        for t in range(allowed_threads):
            processes.append(EvalProcess(evaluated_queue, population_queue))
        for process in processes:
            process.start()
        for process in processes:
            process.join()

    environment.debug_print("Evaluating rest of the genomes.")
    processes = list()
    num_rest = environment.context.population - (iterations * allowed_threads)
    for t in range(num_rest):
        processes.append(EvalProcess(evaluated_queue, population_queue))
    for process in processes:
        process.start()
    for process in processes:
        process.join()

    pop = list()
    values = list()
    for i in range(environment.context.population):
        individual = evaluated_queue.get()
        pop.append(individual)
        values.append(individual.eval())

    return pop, values

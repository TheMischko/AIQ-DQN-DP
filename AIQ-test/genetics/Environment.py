import math
import os.path
import time
from datetime import datetime

import numpy as np

from genetics import environment
from genetics.Individual import Individual
from genetics.agents_ref.AgentReference import AgentReference
from genetics.context.TestContext import Context
from genetics.environment import log_results, create_new_generation
from genetics.environment.select_parents import select_parents, SelectionStrategy


def select_top_scores(scores: [float], count: int):
    partition = np.argpartition(scores, -count)
    return partition[-count:].tolist()


class Environment:
    def __init__(self, agent_ref: AgentReference, context: Context, seed_population: list):
        """
        :param agent_ref: Instance of reference class for an AIQ agent.
        :param context: Settings for current testing.
        :param seed_population: Initial genomes for first generation.
        """
        # Genetic test setting
        self.agent_ref: AgentReference = agent_ref
        self.context = context
        self.seed_population = seed_population

        self.results_dir = os.path.abspath("./log_gen/")
        self.file_name = self.create_result_filename()
        self.log_file = os.path.join(self.results_dir, self.file_name)
        self.prepare_log_file()

        self.starting_time = None

    def simulate(self):
        self.starting_time = time.time()

        population = environment.initialize_population(self, self.context.population, self.seed_population)

        best_individuals = None
        for i in range(self.context.epochs):
            self.debug_print(f"Starting epoch {i + 1}.")
            start_time = time.time()

            self.debug_print("Starting population evaluation.")
            population, scores = environment.evaluate_population(self, population)
            self.debug_print(f"Average fitness of the population: {(sum(scores) / len(scores))}")

            self.debug_print("Selecting best individuals.")
            best_individuals_indices = select_top_scores(scores, self.context.count_select)
            best_individuals = [population[i] for i in best_individuals_indices]

            self.debug_print("Loging best individuals.")
            # Append population to result file
            log_results(self, population, i, start_time, will_print=False, save_log=True)
            # Print best results for this epoch
            log_results(self, best_individuals, i, start_time, will_print=True, save_log=False)

            if i == self.context.epochs - 1:
                break

            parents = self.select_parents(population, scores)

            # Create new generation
            population.clear()
            population.extend(parents)

            population = environment.create_new_generation(self, population)

        value_list = [best_individuals[i].eval() for i in range(len(best_individuals))]
        best_index = np.argmax(np.array(value_list))
        best_individual = best_individuals[best_index]
        print("Best found individual is %s with value %5.2f" % (best_individual.get_genome(), best_individual.eval()))
        return best_individuals[best_index]

    def select_parents(self, population, scores):
        return select_parents(self, population, scores, SelectionStrategy(self.context.strategy))

    def debug_print(self, msg):
        if not self.context.debug:
            return
        time_from_start = time.time() - self.starting_time
        print("[%s]   %s" % (self.parse_time_to_str(time_from_start), msg))

    def parse_time_to_str(self, time_val):
        hours = math.floor(time_val / 3600)
        return "%02d:%02d:%02d" % (
            math.floor(time_val / 3600), math.floor((time_val % 3600) / 60), (time_val % 3600) % 60)

    def create_result_filename(self):
        time_str = datetime.today().strftime("%Y_%m%d_%H%M")
        return f"{self.agent_ref.get_test_agent_name()}_{time_str}_E{self.context.epochs}_P{self.context.population}_I{self.context.test_settings.iterations}.csv"

    def prepare_log_file(self):
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)
        file = open(self.log_file, "w", encoding="UTF-8")
        file.close()

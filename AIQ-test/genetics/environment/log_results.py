import time
from typing import List

from genetics import Environment
from genetics.Individual import Individual

SEPARATOR = ','


def log_results(environment: Environment, individuals, iteration, start_time, will_print=True, save_log=False):
    log_string = "\n"
    log_string += "%d. Generation \n" % (int(iteration) + 1)
    for i in range(len(individuals)):
        log_string += "  %2d:   %s   with value: %5.2f\n" % (i, individuals[i], individuals[i].eval())
    log_string += "Took time %f \n" % (time.time() - start_time)
    log_string += "___________________________________________\n"
    if save_log:
        append_results(iteration, individuals, environment.log_file)
    if will_print:
        print(log_string)


def append_results(iteration, individuals: List[Individual], file):
    with open(file, "a", encoding="UTF-8") as log:
        for individual in individuals:
            genome_str = SEPARATOR.join([str(x) for x in individual.genome])
            log.write(f"{iteration}{SEPARATOR}{individual.eval()}{SEPARATOR}{genome_str}\n")

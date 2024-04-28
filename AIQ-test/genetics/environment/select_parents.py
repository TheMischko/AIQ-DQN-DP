import random
from enum import Enum
from typing import List, Type, Tuple

import numpy as np

from genetics import Environment
from genetics.Individual import Individual


class SelectionStrategy(Enum):
    RouletteWheel = 0
    RouletteWheelRank = 1
    Tournament = 2


def normalize_fitness(scores):
    min_fitness = min(scores)
    offset = abs(min_fitness)
    return [score + offset for score in scores]


def select_parents(environment: Environment, old_population: List[Type[Individual]], scores: List[float],
                   strategy: SelectionStrategy):
    shifted_scores = normalize_fitness(scores)
    parents_count = environment.context.count_select
    strategy_function_mapping = {
        SelectionStrategy.RouletteWheel: roulette_wheel_fitness_selection,
        SelectionStrategy.RouletteWheelRank: roulette_wheel_rank_selection,
        SelectionStrategy.Tournament: tournament_selection
    }
    return strategy_function_mapping[strategy](old_population, shifted_scores, parents_count)


def roulette_wheel_fitness_selection(old_population: List[Type[Individual]], scores: List[float], parents_count: int):
    windowed_scores = apply_windowing(scores)
    scores_sum = get_sum_of_scores(windowed_scores)
    roulette_wheel = list()
    current_prob = 0

    for i in range(len(old_population)):
        prob = windowed_scores[i] / scores_sum
        roulette_wheel.append((current_prob, current_prob + prob, old_population[i]))
        current_prob += prob

    return create_from_roulette_wheel(roulette_wheel, parents_count)


def roulette_wheel_rank_selection(old_population: List[Type[Individual]], scores: List[float], parents_count: int):
    sorted_indices = sorted(range(len(scores)), key=lambda k: scores[k])
    sorted_population = [old_population[i] for i in sorted_indices]

    # Selection pressure 1 < s <= 2
    # The closer to 2 the value is there are more differences between biggest and lowest scored individuals
    s_param = 1.5

    roulette_wheel = list()
    current_prob = 0
    for i in range(len(sorted_population)):
        prob = ((2 - s_param) / len(sorted_population)) + (2 * i * (s_param - 1)) / (
                    len(sorted_population) * (len(sorted_population) - 1))
        roulette_wheel.append((current_prob, current_prob + prob, sorted_population[i]))
        current_prob += prob

    return create_from_roulette_wheel(roulette_wheel, parents_count)


def tournament_selection(old_population: List[Type[Individual]], scores: List[float], parents_count: int):
    count_competitors = 3
    if len(old_population) < (count_competitors * 2):
        raise Exception(f"Population is too small for Tournament selection, you need to have population at least with "
                        f"size of {(count_competitors * 2)}")
    parents = list()
    rand_generator = random.Random()
    while len(parents) < parents_count:
        competitors_indices = rand_generator.choices(range(len(old_population)), k=count_competitors)
        best_competitor_index = max(competitors_indices, key=lambda index: scores[index])
        best_competitor = old_population[best_competitor_index]
        parents.append(best_competitor)
    return parents


def get_sum_of_scores(scores: List[float]):
    return np.sum(scores)


def apply_windowing(scores):
    min_fitness = min(scores)
    return [(score + 1) - min_fitness for score in scores]


def create_from_roulette_wheel(roulette_wheel: List[Tuple[float, float, Type[Individual]]], parents_count):
    parents = list()
    rand_generator = random.Random()
    while len(parents) < parents_count:
        rand = rand_generator.random()
        for low, high, individual in roulette_wheel:
            if low <= rand < high:
                parents.append(individual)
                break

    return parents

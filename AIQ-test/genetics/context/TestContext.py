import math
from argparse import Namespace
from typing import NamedTuple

import yaml

from genetics.context.TestSettings import TestSettings


class Context(NamedTuple):
    """
    Provides all settings about current genetic test.
    """
    debug: bool
    population: int
    count_select: int
    epochs: int
    num_agents: int
    strategy: int
    mutation_prob: int
    num_changes: int
    num_mutations: int
    num_crossover: int
    test_settings: TestSettings

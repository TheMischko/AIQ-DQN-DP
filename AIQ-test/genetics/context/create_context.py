import math
from argparse import Namespace

from genetics.context.TestContext import Context
from genetics.context.TestSettings import TestSettings


def create_context(args: Namespace) -> Context:
    num_mutations = math.floor((args.pop_size - args.count_select)/2)
    num_crossover = args.pop_size - args.count_select - num_mutations

    return Context(
        debug=args.debug,
        population=args.pop_size,
        count_select=args.count_select,
        epochs=args.epochs,
        num_agents=args.num_agents,
        strategy=args.strategy,
        num_changes=2,
        num_crossover=num_crossover,
        num_mutations=num_mutations,
        mutation_prob=args.mutation_prob,
        test_settings=TestSettings(
            args.agent,
            args.iterations,
            args.samples,
            args.threads,
            args.log,
            args.log_el,
        )
    )

import argparse
import importlib
import json
import logging
import os
import sys

from genetics.agents_ref.AgentReference import AgentReference
from genetics.Environment import Environment
from genetics.context.create_context import create_context

AGENT_REF_FOLDER = "./genetics/agents_ref"


def get_params():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-a", "--agent", help="Set a name of the agent for testing.")
    arg_parser.add_argument("-p", "--pop_size", help="Size of population for each iteration.", type=int)
    arg_parser.add_argument("-c", "--count_select",
                            help="Set size of how many individuals will be moved to next generation.", type=int)
    arg_parser.add_argument("-r", "--strategy", help="Selects strategy for parent selection. 0 = fitness roulette, "
                                                     "1 = fitness rank, 2 = tournament", type=int)
    arg_parser.add_argument("-m", "--mutation_prob", help="Probability of mutation happening on a single part of "
                                                          "genome.", type=float)
    arg_parser.add_argument("-e", "--epochs", help="Number of epochs for genetic algorithm.", type=int)
    arg_parser.add_argument("-i", "--iterations", help="Iterations for AIQ test.", type=int)
    arg_parser.add_argument("-s", "--samples", help="Number of samples for AIQ test.", type=int)
    arg_parser.add_argument("-t", "--threads", help="Set how many threads will be used for single agents in AIQ test.",
                            type=int)
    arg_parser.add_argument("-n", "--num_agents", help="Set how many agents will be run simultaneously.", type=int)
    arg_parser.add_argument("-d", "--debug", help="Turns on the debug messages to print", action="store_true")
    arg_parser.add_argument("--log", help="Will log AIQ results for agents in log folder.", action="store_true")
    arg_parser.add_argument("--log_el", help="Will log AIQ intermediate results for agents in log-el folder.",
                            action="store_true")
    arg_parser.add_argument("--env", default="default", help="Changes what config file will be used based on "
                                                             "environment type.")
    arg_parser.add_argument("--seed_file",
                            help="Path to a file that contains a seed population as array of parameters.")
    return arg_parser.parse_args()


def get_agent(agent_name_input):
    files = os.listdir(AGENT_REF_FOLDER)
    agent_ref_module = AGENT_REF_FOLDER[2:].replace("/", ".")
    for file in files:
        file_without_py = file[:-3]
        if agent_name_input == file_without_py and file.endswith(".py") and not file.startswith("__"):
            module = f'{agent_ref_module}.{file[:-3]}'
            importlib.import_module(module)
            return agent_name_input, module
    raise Exception("No agent found. Check --agent param if corresponds to any of Agent name in agents_ref folder.")


def load_seed_population(path):
    try:
        with open(path, "r", encoding="UTF8") as file:
            data = json.load(file)
            return data
    except:
        return []

    print(path)
    return []


if __name__ == '__main__':
    args = get_params()
    print("--- Genetic algorithm based search for agent parameters in AIQ test ---")
    agent_name, module_name = get_agent(args.agent)
    agent_class = getattr(sys.modules[module_name], agent_name)
    assert issubclass(agent_class, AgentReference), f"{agent_name} is not a subclass of BaseAgent"
    agent = agent_class()

    seed_population = []
    if args.seed_file is not None:
        seed_population = load_seed_population(args.seed_file)

    context = create_context(args)

    environment = Environment(
        agent,
        context,
        seed_population
    )
    best = environment.simulate()

# Module for parameter search by using Genetic Algorithm
This module contains all the necessary code for searching the parameter space for AIQ 
agents in [FindParamsGenetic.py](../FindParamsGenetic.py) script.

## Usage
```bash
python FindParamsGenetic.py -a agent_name -p population_size -c count_selected -e epochs 
                            -i iterations -s samples -t threads -n parallel_runs 
                            -m prob -r strategy --debug --log --log_el
```
Where those arguments mean:
- `-a` is for name of agent reference file in [genetics/agents_ref](./agents_ref) directory without extension. The class name should correspond to the file name.
- `-p` is for setting population size in each epoch.
- `-c` determines how many best chromosomes will be used to create new generation.
- `-e` sets how many epochs of the genetic algorithm will be run.
- `-i` is for setting iterations of AIQ test that will be used to determine chromosome's score.
- `-m` probability of mutation happening on a single part of genome.
- `-r` sets strategy for parent selection 0 = fitness roulette, 1 = fitness rank, 2 = tournament
- `-s` is for setting number of program samples that will be used in AIQ test.
- `-t` controls how many threads will be used on one tested agent in AIQ test.
- `-n` determines how many agents will be run simultaneously. The total number of threads used for genetic algorithm is `-t` values time `-n` value.
- `--debug` toggles debug messages that are printed into standard output stream.
- `--log` toggles whenever result of each tested configuration will be saved in log directory.
- `--log_el` toggles whenever intermediate results for each thousandth interation will be save in log-el directory.

Testable command is:
```bash
python FindParamsGenetic.py -a Q_l -p 6 -c 2 -e 5 -i 5000 -s 100 -t 4 -n 2 --debug --log --log_el
```

## Files in this module:
### [Environment.py](./Environment.py)
- Contain main class of the genetic algorithm Environment.
- This class gets in constructor all the parameters from FindParamsGenetic.py script.
- Body of the `simulate` function contains all the genetic algorithm logic.
  1. It creates population 1 by random generated values from agent reference class.
  2. Then it evaluates all individuals in population.
  3. It selects `count_selected` best individuals.
  4. It creates new population via crossovers and mutation methods.
  5. Repeats from step *ii.* until number of epochs reaches `epochs` value.
- Then it contains helpful functions such as `select_best_individuals` of `debug_print`.
- Note than most of the logic from `simulate` function is divided into subfunctions from [environement module](./environment).

## [Individual](./Individual.py)
- This class is used for storing one genome (chromosome) of the current population.
- `eval` function is used to get AIQ score of current individual.
- Each individual knows how to evaluate itself.
- The class stores its score once computed to avoid multiple evaluations.

## [eval_function](./eval_function.py)
- This file contains logic for genome evaluation.
- It runs an AIQ test with parameters that are provides.
  - `genome` is the array of agents parameters
  - `agent` is the name of agent in AIQ test
  - `eval_params` is dictionary for storing other non-agent related settings for AIQ test
    - It works with this keys: `iterations`, `samples`, `threads`, `log`, `log_el`
- Final value is parsed from text output of the AIQ test that is being printed into a virtual standard output.


#
# Observation encoder for agents to be tested in the AIQ test
#
# Copyright Jan Štipl 2024
# Released under GNU GPLv3
#

import numpy as np
import torch


def encode_observations_n_hot(observations, obs_cells, obs_symbols):
    """
    Perform one hot encoding for each observation
    Order is Big-endian
        First observation is order of X^0, second X^1, ...
    e.g.:
    obs_cells = 2
    obs_symbols = 3
    e.g. first = 0, second = 2
    => observations = [0, 2]
    returned = np.array([
        [1., 0., .0],
        [0., 0., 1.],
    ]).reshape(-1)

    :return: flat tensor of shape=[observations * obs_cells, 1] with observations encoded
    """
    observations_encoding = np.zeros(shape=[obs_cells, obs_symbols], dtype=np.float32)
    for i, obs in enumerate(observations):
        # Observations are in range <0, obs_symbols -1>
        observations_encoding[i][obs] = 1

    return observations_encoding.reshape(-1)


def encode_observations_int(observations, obs_symbols):
    """
    Convert observations into a single number
    First observation is order of X^0, second X^1, ...
    e.g.:
    obs_cells = 2
    obs_symbols = 3
    e.g. first = 2, second = 1
        => observations = [2, 1]
        => encoding = 5
    e.g. [0,0] => 0, [1,0] => 1, [2,0] => 2 ...

    speed is O(1)
    :param observations:
    :param obs_symbols:
    :return:
    """
    encoded = 0
    for i, obs in enumerate(observations):
        encoded += obs * (obs_symbols ** i)

    return encoded
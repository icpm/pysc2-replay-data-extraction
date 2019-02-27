#!/usr/bin/env python

from pysc2.lib import static_data
from pysc2.lib import actions as sc_action
import math

import numpy as np
np.set_printoptions(threshold=np.nan)


class ObserverAgent(object):

    def __init__(self):
        self.states = []

    def step(self, _step, _actions, feat):
        state = list()
        state.append([
            _step.observation["feature_minimap"][1].tolist(),  # visibility
            _step.observation["feature_minimap"][2].tolist(),  # creep
            # player_id
            _step.observation["feature_minimap"][4].tolist(),
            # player_relative
            _step.observation["feature_minimap"][5].tolist(),
        ])

        state.append([
            _step.observation["feature_screen"][1].tolist(),  # visibility
            _step.observation["feature_screen"][2].tolist(),  # creep
            _step.observation["feature_screen"][3].tolist(),  # power
            _step.observation["feature_screen"][4].tolist(),  # player id
            # player_relative
            _step.observation["feature_screen"][5].tolist(),
            _step.observation["feature_screen"][6].tolist(),  # unit_type
            # unit_density
            _step.observation["feature_screen"][11].tolist(),
        ])

        state.append(_step.observation["player"])

        available_actions = np.zeros(len(sc_action.FUNCTIONS))
        for i in _step.observation["available_actions"]:
            available_actions[i] = 1.0
        state.append(available_actions)
        state.append(_actions)
        self.states.append(state)

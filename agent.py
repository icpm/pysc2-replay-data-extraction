#!/usr/bin/env python

import numpy as np
from pysc2.lib import actions as sc_action


class ObserverAgent(object):

    def __init__(self):
        self.states = []

    def step(self, _step, _actions):
        state = dict()
        state['minimap'] = [
            _step.observation["feature_minimap"][1].tolist(),  # visibility
            _step.observation["feature_minimap"][2].tolist(),  # creep
            _step.observation["feature_minimap"][4].tolist(),  # player_id
            _step.observation["feature_minimap"][5].tolist(),  # player_relative
        ]

        state['screen'] = [
            _step.observation["feature_screen"][1].tolist(),  # visibility
            _step.observation["feature_screen"][2].tolist(),  # creep
            _step.observation["feature_screen"][3].tolist(),  # power
            _step.observation["feature_screen"][4].tolist(),  # player id
            _step.observation["feature_screen"][5].tolist(),  # player_relative
            _step.observation["feature_screen"][6].tolist(),  # unit_type
            _step.observation["feature_screen"][11].tolist(),  # unit_density
        ]

        state['player'] = _step.observation["player"].tolist()

        available_actions = np.zeros(len(sc_action.FUNCTIONS))
        for i in _step.observation["available_actions"]:
            available_actions[i] = 1.0

        state['available_actions'] = available_actions.tolist()
        # state['actual_actions'] = _actions

        self.states.append(state)

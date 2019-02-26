#!/usr/bin/env python

import math

import numpy as np
from pysc2.lib import actions as sc_action
from pysc2.lib import static_data


class ObserverAgent(object):

    def __init__(self):
        self.states = []

    def step(self, time_step, actions, feat):
        state = {}
        # state["minimap"] = {
        #     time_step.observation["feature_minimap"][0],                        # height_map
        #     time_step.observation["feature_minimap"][1],                        # visibility
        #     time_step.observation["feature_minimap"][2],                        # creep
        #     time_step.observation["feature_minimap"][3],                        # camera
        #     time_step.observation["feature_minimap"][4],                        # player id
        #     time_step.observation["feature_minimap"][5],                        # player_relative
        # }

        state["screen"] = [
            time_step.observation["feature_screen"][0] / 255,               # height_map
            time_step.observation["feature_screen"][1] / 2,                 # visibility
            time_step.observation["feature_screen"][2],                     # creep
            time_step.observation["feature_screen"][3],                     # power
            time_step.observation["feature_screen"][6],                     
            time_step.observation["feature_screen"][7],                     # selected
            time_step.observation["feature_screen"][8],                     
            time_step.observation["feature_screen"][11]                     # unit_density
        ]

        state["player"] = time_step.observation["player"]

        state["available_actions"] = np.zeros(len(sc_action.FUNCTIONS))
        for i in time_step.observation["available_actions"]:
            state["available_actions"][i] = 1.0

        transformed_actions = []
        for a in actions:
            try:
                pysc2_function_call = feat.reverse_action(a)
                func_id = pysc2_function_call.function
                func_args = pysc2_function_call.arguments
                # if func_name.split('_')[0] in {'Attack', 'Scan', 'Behavior','BorrowUp', 'Effect','Hallucination',\
                #     'Harvest', 'Hold','Land','Lift', 'Load','Move','Patrol','Rally','Smart','TrainWarp',\
                #     'UnloadAll', 'UnloadAllAt''Build', 'Train', 'Research', 'Morph', 'Cancel', 'Halt', 'Stop'}:
                transformed_actions.append([func_id, func_args])
            except:
                pass

        state["actions"] = transformed_actions
        print(state)
        self.states.append(state)
        print(len(self.states))

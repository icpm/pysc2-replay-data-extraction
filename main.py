#!/usr/bin/env python

import glob
import importlib
import os
import pickle

from absl import app, flags
from google.protobuf.json_format import MessageToDict
from pysc2 import run_configs
from pysc2.env.environment import StepType, TimeStep
from pysc2.lib import features, point
from s2clientprotocol import sc2api_pb2 as sc_pb

FLAGS = flags.FLAGS
flags.DEFINE_string("replays", None, "Path to replay files dir.")
flags.DEFINE_string("agent", None, "Path to an agent.")
flags.mark_flag_as_required("replays")
flags.mark_flag_as_required("agent")


class ReplayParser:
    def __init__(self,
                 replay_file_path,
                 agent,
                 player_id=1,
                 screen_size_px=(64, 64),
                 minimap_size_px=(64, 64),
                 discount=1.,
                 step_mul=1):

        self.agent = agent
        self.discount = discount
        self.step_mul = step_mul
        self.skip = 10
        self.replay_file_name = replay_file_path.split("/")[-1].split(".")[0]

        self.run_config = run_configs.get()
        self.sc2_proc = self.run_config.start()
        self.controller = self.sc2_proc.controller

        replay_data = self.run_config.replay_data(replay_file_path)
        ping = self.controller.ping()
        self.info = self.controller.replay_info(replay_data)

        if not self._valid_replay(self.info, ping):
            raise Exception(
                "{} is not a valid replay file!".format(replay_file_path))

        screen_size_px = point.Point(*screen_size_px)
        minimap_size_px = point.Point(*minimap_size_px)
        interface = sc_pb.InterfaceOptions(
            raw=False, score=True,
            feature_layer=sc_pb.SpatialCameraSetup(width=24))
        screen_size_px.assign_to(interface.feature_layer.resolution)
        minimap_size_px.assign_to(interface.feature_layer.minimap_resolution)

        map_data = None
        if self.info.local_map_path:
            map_data = self.run_config.map_data(self.info.local_map_path)

        self._episode_length = self.info.game_duration_loops
        self._episode_steps = 0

        self.controller.start_replay(sc_pb.RequestStartReplay(
            replay_data=replay_data,
            map_data=map_data,
            options=interface,
            observed_player_id=player_id))

        self._state = StepType.FIRST

    @staticmethod
    def _valid_replay(info, ping):
        """Make sure the replay isn't corrupt, and is worth looking at."""
        if (info.HasField("error") or
                info.base_build != ping.base_build or  # different game version
                info.game_duration_loops < 1000 or
                len(info.player_info) != 2):
            return False
        return True

    def start(self):
        _features = features.features_from_game_info(
            self.controller.game_info())

        i = 0
        while i < self.info.game_duration_loops:
            i += self.skip
            self.controller.step(self.step_mul)
            obs = self.controller.observe()
            try:
                agent_obs = _features.transform_obs(obs)
            except:
                pass

            if obs.player_result:
                self._state = StepType.LAST
                discount = 0
            else:
                discount = self.discount

            self._episode_steps += self.step_mul

            step = TimeStep(step_type=self._state, reward=0,
                            discount=discount, observation=agent_obs)

            self.agent.step(step, obs.actions)

            if obs.player_result:
                break

            self._state = StepType.MID

        self.save_data()

    def save_data(self):

        print("Saving data")
        if not os.path.exists("data/"):
            os.mkdir("data/")
        saving_data = {"info": MessageToDict(self.info), "state": self.agent.states}
        pickle.dump(saving_data, open(
            "data/" + self.replay_file_name + ".data", "wb"))
        print("Data successfully saved")
        self.agent.states = []
        print("Data flushed")


def parse_replay(replay_batch, agent_cls):
    for replay in replay_batch:
        filename_without_suffix = os.path.splitext(os.path.basename(replay))[0]
        filename = filename_without_suffix + ".p"
        if os.path.exists("data_full/" + filename):
            continue

        try:
            parser = ReplayParser(replay, agent_cls())
            parser.start()
        except Exception as e:
            print(e)


def main(unused):
    _agent = FLAGS.agent
    _replays_dir = FLAGS.replays
    agent_module, agent_name = _agent.rsplit(".", 1)
    agent_cls = getattr(importlib.import_module(agent_module), agent_name)
    
    replays = glob.glob(_replays_dir + '*.SC2Replay')
    for i in replays:
        _app = ReplayParser(i, agent_cls())
        _app.start()


if __name__ == "__main__":
    app.run(main)

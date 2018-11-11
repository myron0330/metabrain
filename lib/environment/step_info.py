"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Snapshot file in training process.
# **********************************************************************************#
"""
from .. core.objects import SlottedObject


class StepInfo(SlottedObject):
    """
    One step info output during training.
    """
    __slots__ = [
        'observation',
        'reward',
        'done',
        'info'
    ]

    def __init__(self, observation=None, reward=None, done=None, info=None):
        """
        Initialize of one step info.

        Args:
            observation(object): agent's observation of the current environment
            reward(float): amount of reward returned after previous action
            done(boolean): whether the episode has ended, in which case further step() calls will return undefined results
            info(dict): contains auxiliary diagnostic information (helpful for debugging, and sometimes learning)
        """
        super(StepInfo, self).__init__()
        self.observation = observation
        self.done = done
        self.info = info
        self.reward = reward


__all__ = [
    'StepInfo'
]

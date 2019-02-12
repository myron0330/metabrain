"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Snapshot file in training process.
# **********************************************************************************#
"""
from .. core.objects import SlottedObject


class EnvSnapshot(SlottedObject):
    """
    Environment snapshot during training.
    """
    __slots__ = [
        'state',
        'action',
        'next_state',
        'reward',
    ]

    def __init__(self, state=None, action=None, next_state=None, reward=0):
        """
        Initialize of current trade_env snapshot.

        Args:
            state(object): current state
            action(object): target action
            next_state(object): next state
            reward(float): cumulative reward
        """
        super(EnvSnapshot, self).__init__()
        self.state = state
        self.action = action
        self.next_state = next_state
        self.reward = reward

    def reset(self, **kwargs):
        """
        Reset the snapshot to default value.

        Args:
            **kwargs(**dict): key-word parameters.
        """
        default_parameters = {attribute: None for attribute in self.__slots__}
        default_parameters.update(kwargs)
        for key, value in default_parameters.items():
            setattr(self, key, value)


__all__ = [
    'EnvSnapshot'
]

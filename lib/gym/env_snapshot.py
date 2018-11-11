"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Snapshot file in training process.
# **********************************************************************************#
"""
from .. core.objects import ValueObject


class EnvSnapshot(ValueObject):
    """
    Environment snapshot during training.
    """
    __slots__ = [
        'state',
        'action',
        'next_state',
        'reward'
    ]

    def __init__(self, state=None, action=None, next_state=None, reward=None):
        """
        Initialize of current environment snapshot.

        Args:
            state(int): current position holding state
            action(int): 1:LONG / -1:SHORT
            next_state(int): next position holding state
            reward(float): current reward.
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

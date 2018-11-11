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
        self.state = state or 0
        self.action = action
        self.next_state = next_state or 0
        self.reward = reward or 0

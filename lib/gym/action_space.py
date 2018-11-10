# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Action space.
# **********************************************************************************#
import random
from gym import Space
from .. core.enums import LongShort


class LongShortSpace(Space):
    """
    Long/short discrete space.
    """
    def __init__(self):
        super(LongShortSpace, self).__init__(dtype=int)

    def sample(self):
        """
        Generate random action sample.

        Returns:
            int: 1:LONG / -1:SHORT
        """
        sample_map = {
            0: LongShort.LONG,
            1: LongShort.SHORT
        }
        return sample_map[random.randint(0, 1)]

    def contains(self, target):
        """
        Contains the target input or not.

        Args:
            target(string): target action.

        Returns:
            boolean: contains or not.
        """
        return LongShort.has_value(target)

    def __repr__(self):
        return "LongShortSpace(LONG/SHORT)"


class TradingActionSpace(Space):
    """
    Trading action space.
    """
    def __init__(self):
        super(TradingActionSpace, self).__init__(dtype=str)

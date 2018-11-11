"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:
# **********************************************************************************#
"""
from . base import (
    LongShort,
    TradingAction
)


def trading_action_transition(action, state):
    """
    Trading action transition function.

    Args:
        action(string): Trading actions
        state(float): position holding

    Returns:
        float: next state position holding
    """
    raise NotImplementedError

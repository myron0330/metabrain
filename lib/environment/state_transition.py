"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:
# **********************************************************************************#
"""
from copy import copy
from . base import (
    LongShort,
    TradingAction
)


def trading_action_transition(action, state):
    """
    Trading action transition function.

    Args:
        action(string): Trading actions
        state(PortfolioState): portfolio state

    Returns:
        PortfolioState: updated portfolio state
    """
    next_state = copy(state)
    if action == TradingAction.BUY:
        pass
    if action == TradingAction.SELL:
        pass
    if action == TradingAction.SHORT:
        pass
    if action == TradingAction.COVER:
        pass
    if action == TradingAction.FAIR:
        return next_state

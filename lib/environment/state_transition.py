"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:
# **********************************************************************************#
"""
from copy import copy
from . base import (
    TradingAction
)


def trading_action_transition(action, state, price, change_percent=0.1):
    """
    Trading action transition function.

    Args:
        action(string): Trading actions
        state(PortfolioState): portfolio state
        price(float): current price
        change_percent(float): position change percent

    Returns:
        PortfolioState: updated portfolio state
    """
    next_state = copy(state)
    next_state.evaluate(price)
    reference_position_proportion = next_state.position_proportion
    reference_portfolio_value = next_state.portfolio_value
    delta_cash = reference_portfolio_value * change_percent

    if action in [TradingAction.BUY, TradingAction.SHORT]:
        if reference_position_proportion > 1 - change_percent:
            return next_state
        open_quantity = next_state.feasible_open_quantity(margin_cash=delta_cash)
        if open_quantity:
            if action == TradingAction.BUY:
                next_state.position_holding.long_amount += open_quantity
            else:
                next_state.position_holding.short_amount += open_quantity
    elif action in [TradingAction.SELL, TradingAction.COVER]:
        if action == TradingAction.SELL:
            close_quantity = next_state.feasible_close_quantity(target_cash=delta_cash, long_short='long')
            if close_quantity:
                next_state.position_holding.long_amount -= close_quantity
        else:
            close_quantity = next_state.feasible_close_quantity(target_cash=delta_cash, long_short='short')
            if close_quantity:
                next_state.position_holding.short_amount -= close_quantity
    next_state.evaluate(price)
    return next_state

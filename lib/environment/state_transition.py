"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:
# **********************************************************************************#
"""
from copy import deepcopy
from . base import (
    TradingAction
)
from .. trade.trade import Trade


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
    next_state = deepcopy(state)
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
                trade = Trade(order_id=None,
                              symbol=next_state.position_holding.symbol,
                              direction=1,
                              offset_flag='open',
                              transact_amount=open_quantity,
                              transact_price=price,
                              filled_time=None,
                              commission=0,
                              slippage=0)
                next_state.update(trade)
            else:
                trade = Trade(order_id=None,
                              symbol=next_state.position_holding.symbol,
                              direction=-1,
                              offset_flag='open',
                              transact_amount=open_quantity,
                              transact_price=price,
                              filled_time=None,
                              commission=0,
                              slippage=0)
                next_state.update(trade)
    elif action in [TradingAction.SELL, TradingAction.COVER]:
        if action == TradingAction.SELL:
            close_quantity = next_state.feasible_close_quantity(target_cash=delta_cash, long_short='long')
            if close_quantity:
                trade = Trade(order_id=None,
                              symbol=next_state.position_holding.symbol,
                              direction=-1,
                              offset_flag='close',
                              transact_amount=close_quantity,
                              transact_price=price,
                              filled_time=None,
                              commission=0,
                              slippage=0)
                next_state.update(trade)
        else:
            close_quantity = next_state.feasible_close_quantity(target_cash=delta_cash, long_short='short')
            if close_quantity:
                trade = Trade(order_id=None,
                              symbol=next_state.position_holding.symbol,
                              direction=1,
                              offset_flag='close',
                              transact_amount=close_quantity,
                              transact_price=price,
                              filled_time=None,
                              commission=0,
                              slippage=0)
                next_state.update(trade)
    next_state.evaluate(price)
    return next_state

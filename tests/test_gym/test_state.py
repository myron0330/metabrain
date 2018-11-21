"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:
# **********************************************************************************#
"""
from unittest import TestCase
from lib.environment.state import PortfolioState
from lib.environment.base import TradingAction
from lib.environment.state_transition import trading_action_transition


class TestState(TestCase):

    def test_portfolio_state(self):
        """
        Test portfolio state.
        """
        portfolio_state = PortfolioState.from_configs(symbol='ZN1902',
                                                      position_base=-1,
                                                      cost_base=21270,
                                                      multiplier=5,
                                                      margin_rate=0.15,
                                                      margin_cash=5e5
                                                      )
        print(portfolio_state)

    def test_trading_action_transition(self):
        """
        Test trading action transition.
        """
        portfolio_state = PortfolioState.from_configs(symbol='ZN1902',
                                                      multiplier=5,
                                                      margin_rate=0.15,
                                                      margin_cash=5e5)
        print(portfolio_state.margin_cash, portfolio_state.position_proportion, portfolio_state.position_holding)
        buy_state = trading_action_transition(TradingAction.BUY, portfolio_state, 21100)
        print(buy_state.margin_cash, buy_state.position_proportion, buy_state.position_holding)

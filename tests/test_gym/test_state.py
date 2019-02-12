"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:
# **********************************************************************************#
"""
from unittest import TestCase
from brain.trade_env.state import PortfolioState
from brain.trade_env.base import TradingAction
from brain.trade_env.state_transition import trading_action_transition


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
        print('original state')
        print(portfolio_state.margin_cash, portfolio_state.portfolio_value,
              portfolio_state.position_proportion, portfolio_state.position_holding)
        print('\n')
        buy_state = trading_action_transition(TradingAction.BUY, portfolio_state, 21100)
        print('buy state')
        print(buy_state.margin_cash, buy_state.portfolio_value,
              buy_state.position_proportion, buy_state.position_holding)
        print('\n')
        sell_state = trading_action_transition(TradingAction.SELL, buy_state, 21000)
        print('sell state')
        print(sell_state.margin_cash, sell_state.portfolio_value,
              sell_state.position_proportion, sell_state.position_holding)
        print('\n')
        short_state = trading_action_transition(TradingAction.SHORT, sell_state, 21000)
        print('short state')
        print(short_state.margin_cash, short_state.portfolio_value,
              short_state.position_proportion, short_state.position_holding)
        print('\n')
        cover_state = trading_action_transition(TradingAction.COVER, short_state, 20990)
        print(cover_state.margin_cash, cover_state.portfolio_value,
              cover_state.position_proportion, cover_state.position_holding)
        print('\n')

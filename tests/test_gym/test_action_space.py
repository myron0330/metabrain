# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:  Test action space.
# **********************************************************************************#
from unittest import TestCase
from brain.trade_env.action_space import (
    LongShortSpace,
    TradingActionSpace
)
from brain.trade_env.base import TradingAction


class TestActionSpace(TestCase):

    def test_long_short_space(self):
        """
        Test long short space.
        """
        action_space = LongShortSpace()
        print(action_space.sample())
        print(action_space.contains(1))
        print(action_space.contains(-1))
        print(action_space.contains(0))

    def test_trading_action_space(self):
        """
        Test trading action space.
        """
        action_space = TradingActionSpace()
        print(action_space.sample())
        print(action_space.contains(TradingAction.BUY))
        print(action_space.contains(TradingAction.SELL))
        print(action_space.contains(TradingAction.SHORT))
        print(action_space.contains(TradingAction.COVER))
        print(action_space.contains(TradingAction.FAIR))

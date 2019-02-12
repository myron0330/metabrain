"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:
# **********************************************************************************#
"""
from unittest import TestCase
from brain.trade_env.market_env import FuturesMarketEnv


class TestMarketEnv(TestCase):

    def test_instantiated_by_configs(self):
        """
        Test instantiated by configs.
        """
        market_env = FuturesMarketEnv.from_configs(margin_cash=1e6, symbol='ZN1902')
        print(market_env)

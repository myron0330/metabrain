"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:
# **********************************************************************************#
"""
from unittest import TestCase
from lib.environment.market_env import MarketEnv


class TestMarketEnv(TestCase):

    def test_instantiated_by_configs(self):
        """
        Test instantiated by configs.
        """
        market_env = MarketEnv.from_configs(margin_cash=1e6, symbol='ZN1902')
        print(market_env)

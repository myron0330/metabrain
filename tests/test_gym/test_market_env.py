"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:
# **********************************************************************************#
"""
from unittest import TestCase
from lib.environment.market_env import MarketEnv


class TestMarketEnv(TestCase):

    def setUp(self):
        """
        Set up the initialize.
        """
        self.market_env = MarketEnv()

    def test_step(self):
        """
        Test market env.
        """
        action = 'BUY'
        self.market_env.step()

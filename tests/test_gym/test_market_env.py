"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:
# **********************************************************************************#
"""
from unittest import TestCase
from lib.env.market_env import MarketEnv


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
        state_transition = None, reward_calculator = None, done_condition = None
        self.market_env.step()

# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:  Test action space.
# **********************************************************************************#
from unittest import TestCase
from brain.trade_env.action_space import LongShortSpace


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

"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: State file.
# **********************************************************************************#
"""
from .. core.objects import SlottedObject


class PortfolioState(SlottedObject):
    """
    Portfolio state, including two essential information: 1) reference margin cash; 2) position holding.
    """
    def __init__(self, margin_cash=0, position_holding=None):
        """
        Initialize the portfolio state.

        Args:
            margin_cash(float): available margin cash
            position_holding(obj):
        """
        super(PortfolioState, self).__init__()
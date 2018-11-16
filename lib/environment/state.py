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
    __slots__ = [
        'margin_cash',
        'position_holding',
        'portfolio_value',
    ]

    def __init__(self, margin_cash=0, position_holding=None, portfolio_value=None):
        """
        Initialize the portfolio state.

        Args:
            margin_cash(float): available margin cash
            position_holding(obj): position holding
        """
        super(PortfolioState, self).__init__()
        self.margin_cash = margin_cash
        self.position_holding = position_holding
        self.portfolio_value = portfolio_value or self.evaluate()

    def evaluate(self, price=None, multiplier=1, margin_rate=1.):
        """
        Evaluate portfolio value according to price input.

        Args:
            price(float): price
            multiplier(int): multiplier
            margin_rate(float): margin rate

        Returns:
            float: evaluated portfolio value
        """
        float_pnl_added = self.position_holding.evaluate(price=price,
                                                         multiplier=multiplier,
                                                         margin_rate=margin_rate)
        self.portfolio_value += float_pnl_added
        self.margin_cash = self.portfolio_value - self.position_holding.total_margin

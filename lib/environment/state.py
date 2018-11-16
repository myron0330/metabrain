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
        'multiplier',
        'margin_rate'
    ]

    def __init__(self, margin_cash=0, position_holding=None, multiplier=1, margin_rate=1.):
        """
        Initialize the portfolio state.

        Args:
            margin_cash(float): available margin cash
            position_holding(obj): position holding
            multiplier(int): contract multiplier
            margin_rate(float): contract margin rate
        """
        super(PortfolioState, self).__init__()
        self.margin_cash = margin_cash
        self.position_holding = position_holding
        self.portfolio_value = self._initiate_portfolio_value()
        self.multiplier = multiplier
        self.margin_rate = margin_rate

    def evaluate(self, price=None):
        """
        Evaluate portfolio value according to price input.

        Args:
            price(float): price

        Returns:
            float: evaluated portfolio value
        """
        float_pnl_added = self.position_holding.evaluate(price=price,
                                                         multiplier=self.multiplier,
                                                         margin_rate=self.margin_rate)
        self.portfolio_value += float_pnl_added
        self.margin_cash = self.portfolio_value - self.position_holding.total_margin

    def _initiate_portfolio_value(self):
        """
        Initiate portfolio value.
        """
        return self.margin_cash + self.position_holding.total_margin

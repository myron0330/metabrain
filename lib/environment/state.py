"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: State file.
# **********************************************************************************#
"""
from .. core.objects import SlottedObject
from .. trade.position import FuturesPosition


class PortfolioState(SlottedObject):
    """
    Portfolio state, including two essential information.
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

    @classmethod
    def from_configs(cls, symbol=None,
                     position_base=0,
                     cost_base=0,
                     margin_cash=0,
                     multiplier=1,
                     margin_rate=1.):
        """
        Generate from configs.

        Args:
            symbol(string): contract symbol
            position_base(int): initial position base amount
            cost_base(float): initial cost base price
            margin_cash(float): margin cash
            multiplier(int): contract multiplier
            margin_rate(float): contract margin rate

        Returns:
            PortfolioState: instance
        """
        position_holding = FuturesPosition.from_configs(symbol=symbol,
                                                        position_base=position_base,
                                                        cost_base=cost_base,
                                                        multiplier=multiplier,
                                                        margin_rate=margin_rate)
        return cls(margin_cash=margin_cash,
                   position_holding=position_holding,
                   multiplier=multiplier,
                   margin_rate=margin_rate)

    @property
    def position_proportion(self):
        """
        The proportion of position holding margin.
        """
        return self.position_holding.total_margin / self.portfolio_value if self.portfolio_value else 0

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

    def update(self, trade, multiplier=1, margin_rate=1.):
        """
        Update current position according to trade and other parameters.

        Args:
            trade(PMSTrade): Trade
            multiplier(int): multiplier
            margin_rate(float): margin rate

        Returns:
            float: portfolio profit and loss
        """
        portfolio_added = self.position_holding.update(trade=trade, multiplier=multiplier, margin_rate=margin_rate)
        self.portfolio_value += portfolio_added
        self.margin_cash = self.portfolio_value - self.position_holding.total_margin

    def feasible_open_quantity(self, margin_cash=None):
        """
        The reference open quantity that could be opened.

        Args:
            margin_cash(float): available margin cash

        Returns:
            int: feasible open quantity
        """
        margin_cash = margin_cash or self.margin_cash
        open_quantity = \
            int(margin_cash / self.margin_rate / self.multiplier / self.position_holding.price)\
            if self.margin_rate and self.multiplier and self.position_holding.price else 0
        return open_quantity

    def feasible_close_quantity(self, target_cash=None, long_short='long'):
        """
        The reference close quantity according to target_cash input and max_holding.

        Args:
            target_cash(float): target cash
            long_short(string): long or short

        Returns:
            int: feasible close quantity
        """
        target_cash = target_cash or self.margin_cash
        close_quantity = \
            int(target_cash / self.margin_rate / self.multiplier / self.position_holding.price)\
            if self.margin_rate and self.multiplier and self.position_holding.price else 0
        holding_quantity = \
            self.position_holding.long_amount if long_short == 'long' else self.position_holding.short_amount
        return min(close_quantity, holding_quantity)

    def _initiate_portfolio_value(self):
        """
        Initiate portfolio value.
        """
        return self.margin_cash + self.position_holding.total_margin

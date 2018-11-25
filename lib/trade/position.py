"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: position file.
#   Author: Myron
# **********************************************************************************#
"""
from __future__ import division
import numpy as np
from utils.exceptions import *
from . base import SecuritiesType


def choose_position(security_type):
    """
    Choose position by security type.
    Args:
        security_type(string): security type.

    Returns:
        obj: Position object
    """
    if security_type == SecuritiesType.futures:
        position_obj = FuturesPosition
    else:
        raise ExceptionsFormat.INVALID_SECURITY_TYPE.format(security_type)
    return position_obj


class LongShortPosition(object):
    """
    Long short position.
    """
    __slots__ = [
        'symbol',
        'price',
        'long_amount',
        'long_cost',
        'short_amount',
        'short_cost',
        'long_margin',
        'short_margin',
        'value',
        'profit',
        'today_profit',
        'offset_profit'
    ]

    def __init__(self, symbol=0, price=0., long_amount=0, short_amount=0, long_margin=0,
                 short_margin=0, long_cost=0, short_cost=0, value=0, profit=0, today_profit=0,
                 offset_profit=0):
        self.symbol = symbol
        self.price = price
        self.long_amount = long_amount
        self.short_amount = short_amount
        self.long_margin = long_margin
        self.short_margin = short_margin
        self.long_cost = long_cost
        self.short_cost = short_cost
        self.value = value
        self.profit = profit
        self.today_profit = today_profit
        self.offset_profit = offset_profit

    @property
    def total_margin(self):
        """
        Total margin.
        """
        return self.long_margin + self.short_margin

    def evaluate(self, price, multiplier=1., margin_rate=1.):
        """
        Update price, margin and profit, return the incremental floating earning.

        Args:
            price(float): reference price
            multiplier(float): contract multiplier
            margin_rate(float): contract margin rate

        Returns:
            float: portfolio profit and loss
        """
        long_market_value = price * self.long_amount * multiplier
        short_market_value = price * self.short_amount * multiplier
        if not self.value:
            self.value = multiplier * (self.long_cost * self.long_amount - self.short_cost * self.short_amount)
        float_pnl_added = long_market_value - short_market_value - self.value
        self.price = price
        self.long_margin = long_market_value * margin_rate
        self.short_margin = short_market_value * margin_rate
        self.profit = long_market_value - short_market_value - multiplier * (
            self.long_cost * self.long_amount - self.short_cost * self.short_amount)
        self.value = long_market_value - short_market_value
        return float_pnl_added

    @classmethod
    def from_request(cls, request):
        """
        Generate new FuturesPosition from request

        Args:
            request(dict): request database
        """
        return cls(**request)

    @classmethod
    def from_query(cls, query_data):
        """
        Recover existed FuturesPosition from query database

        Args:
            query_data(dict): query database
        """
        position = cls(**query_data)
        return position

    def to_database_item(self):
        """
        To redis item
        """
        redis_item = {
            'symbol': self.symbol,
            'price': self.price,
            'long_amount': self.long_amount,
            'short_amount': self.short_amount,
            'long_margin': self.long_margin,
            'short_margin': self.short_margin,
            'long_cost': self.long_cost,
            'short_cost': self.short_cost,
            'value': self.value,
            'profit': self.profit,
            'today_profit': self.today_profit,
            'offset_profit': self.offset_profit
        }
        return redis_item

    def to_dict(self):
        """
        To dict
        """
        return {
            'symbol': self.symbol,
            'price': self.price,
            'long_amount': self.long_amount,
            'long_cost': self.long_cost,
            'long_margin': self.long_margin,
            'short_amount': self.short_amount,
            'short_cost': self.short_cost,
            'short_margin': self.short_margin,
            'value': self.value,
            'profit': self.profit,
            'today_profit': self.today_profit,
            'offset_profit': self.offset_profit
        }

    def get(self, key, default=None):
        """
        Get the value of a key with it's default to be appointed.
        Args:
            key(obj): the key of the dict
            default(obj): the default value

        Returns:
            obj: the value
        """
        return self.__dict__.get(key, default)

    def __repr__(self):
        return "{}(symbol: {}, price: {}, long_amount: {}, short_amount: {}, " \
               "long_margin: {}, short_margin: {}," \
               "long_cost: {}, short_cost: {}, profit: {})".format(self.__class__.__name__,
                                                                   self.symbol,
                                                                   self.price,
                                                                   self.long_amount,
                                                                   self.short_amount,
                                                                   self.long_margin,
                                                                   self.short_margin,
                                                                   self.long_cost,
                                                                   self.short_cost,
                                                                   self.profit)


class FuturesPosition(LongShortPosition):
    """
    Futures position.
    """
    def __init__(self, symbol=None, price=None, long_amount=0, short_amount=0, long_margin=0, short_margin=0,
                 long_cost=0, short_cost=0, value=0, profit=0, today_long_open=0, today_short_open=0,
                 today_profit=0, offset_profit=0, pre_settlement_price=0, settlement_price=0,
                 margin_rate=1., multiplier=1):
        super(FuturesPosition, self).__init__(symbol, price=price, long_amount=long_amount,
                                              short_amount=short_amount,
                                              long_margin=long_margin,
                                              short_margin=short_margin,
                                              long_cost=long_cost,
                                              short_cost=short_cost,
                                              value=value,
                                              profit=profit,
                                              today_profit=today_profit,
                                              offset_profit=offset_profit)
        self.today_long_open = today_long_open
        self.today_short_open = today_short_open
        self.pre_settlement_price = pre_settlement_price
        self.settlement_price = settlement_price
        self.margin_rate = margin_rate
        self.multiplier = multiplier

    @classmethod
    def from_configs(cls, symbol=None, position_base=0, cost_base=0, multiplier=1, margin_rate=1.):
        """
        Generate from configs.
        Args:
            symbol(string): contract symbol
            position_base(int): initial position base amount
            cost_base(float): initial cost base price
            multiplier(int): contract multiplier
            margin_rate(float): contract margin rate

        Returns:
            FuturesPosition: instance
        """
        parameters = {
            'symbol': symbol,
            'price': cost_base,
            'settlement_price': cost_base,
            'pre_settlement_price': cost_base,
            'margin_rate': margin_rate,
            'value': abs(position_base * cost_base * multiplier)
        }
        if position_base > 0:
            parameters['long_amount'] = position_base
            parameters['long_margin'] = position_base * cost_base * multiplier * margin_rate
        elif position_base < 0:
            parameters['short_amount'] = abs(position_base)
            parameters['short_margin'] = abs(position_base) * cost_base * multiplier * margin_rate
        return cls(**parameters)

    def calc_close_pnl(self, trade, multiplier):
        """
        Calculate offset profit and loss without update relevant attributes.

        Args:
            trade(PMSTrade): trade record
            multiplier(float): multiplier

        Returns:
            float: offset profit and loss
        """
        amount = self.long_amount if trade.direction == 1 else self.short_amount
        if amount < trade.filled_amount:
            raise ExceptionsFormat.INVALID_FILLED_AMOUNT.format(trade.filled_amount)
        cost = self.long_cost if trade.direction == 1 else self.short_cost
        close_pnl = trade.direction * (trade.transact_price - cost) * trade.filled_amount * multiplier
        return close_pnl

    def update(self, trade, multiplier, margin_rate):
        """
        Update current position according to trade and other parameters.

        Args:
            trade(PMSTrade): Trade
            multiplier(int): multiplier
            margin_rate(float): margin rate

        Returns:
            float: portfolio profit and loss
        """
        if not trade.transact_amount or np.isnan(trade.transact_amount):
            trade.transact_amount = 0
        offset = 1 if trade.offset_flag == 'open' else -1
        trade_mv = offset * trade.direction * trade.transact_amount * multiplier
        if trade.direction == 1:
            original_amount = self.long_amount
            if trade.offset_flag == 'open':
                # 更新持仓浮动盈亏
                float_pnl = self.evaluate(trade.transact_price, multiplier, margin_rate)
                self.long_amount += trade.transact_amount
                self.long_cost = \
                    (self.long_cost * original_amount + trade.transact_amount * trade.transact_price) / \
                    self.long_amount if self.long_amount else 0
                self.value += trade.transact_price * trade_mv
                portfolio_value_added = float_pnl
            else:
                # 先处理成交的平仓盈亏, 再更新持仓浮动盈亏增量
                close_pnl = self.calc_close_pnl(trade, multiplier)
                self.short_amount -= trade.transact_amount
                self.value -= self.price * trade_mv
                float_pnl = self.evaluate(trade.transact_price, multiplier, margin_rate)
                portfolio_value_added = close_pnl + float_pnl
        else:
            original_amount = self.short_amount
            if trade.offset_flag == 'open':
                # 更新持仓浮动盈亏
                float_pnl = self.evaluate(trade.transact_price, multiplier, margin_rate)
                self.short_amount += trade.transact_amount
                self.short_cost = \
                    (self.short_cost * original_amount + trade.transact_amount * trade.transact_price) / \
                    self.short_amount if self.short_amount else 0
                self.value += trade.transact_price * trade_mv
                portfolio_value_added = float_pnl
            else:
                # 先处理成交的平仓盈亏, 再更新持仓浮动盈亏增量
                close_pnl = self.calc_close_pnl(trade, multiplier)
                self.long_amount -= trade.transact_amount
                self.value -= self.price * trade_mv
                float_pnl = self.evaluate(trade.transact_price, multiplier, margin_rate)
                portfolio_value_added = close_pnl + float_pnl
        self.evaluate(trade.transact_price, multiplier, margin_rate)
        return portfolio_value_added

    @classmethod
    def from_request(cls, request):
        """
        Generate new FuturesPosition from request

        Args:
            request(dict): request data
        """
        return cls(**request)

    @classmethod
    def from_query(cls, query_data):
        """
        Recover existed FuturesPosition from query data

        Args:
            query_data(dict): query data
        """
        position = cls(**query_data)
        return position

    @classmethod
    def from_ctp(cls, position_response):
        """
        Receive from ctp response.

        Args:
            position_response(obj): position response
        """
        item = {
            'symbol': position_response.instrument_id,
            'price': position_response.settlement_price,
            'profit': position_response.position_profit,
            'pre_settlement_price': position_response.pre_settlement_price,
            'settlement_price': position_response.settlement_price,
            'margin_rate': position_response.margin_rate_by_money,
        }
        if position_response.position_direction == '2':
            item['long_amount'] = position_response.position
            item['long_margin'] = position_response.use_margin
            item['long_cost'] = position_response.use_margin / position_response.position
        elif position_response.position_direction == '3':
            item['short_amount'] = position_response.position
            item['short_margin'] = position_response.use_margin
            item['short_cost'] = position_response.use_margin / position_response.position
        return cls(**item)

    def to_database_item(self):
        """
        To redis item
        """
        redis_item = {
            'symbol': self.symbol,
            'price': self.price,
            'long_amount': self.long_amount,
            'short_amount': self.short_amount,
            'long_margin': self.long_margin,
            'short_margin': self.short_margin,
            'long_cost': self.long_cost,
            'short_cost': self.short_cost,
            'value': self.value,
            'profit': self.profit,
            'today_long_open': self.today_long_open,
            'today_short_open': self.today_short_open,
            'today_profit': self.today_profit,
            'offset_profit': self.offset_profit,
            'margin_rate': self.margin_rate,
            'multiplier': self.multiplier
        }
        return redis_item

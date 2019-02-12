"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: trade file.
#   Author: Myron
# **********************************************************************************#
"""
import uuid


class Trade(object):

    """
    Trade item.
    """

    def __init__(self, order_id, symbol, direction, offset_flag, transact_amount, transact_price, filled_time,
                 commission, slippage):
        self.order_id = order_id
        self.symbol = symbol
        self.direction = direction
        self.offset_flag = offset_flag
        self.transact_amount = transact_amount
        self.transact_price = transact_price
        self.filled_time = filled_time
        self.commission = commission
        self.slippage = slippage

    def to_dict(self):
        """
        To dict
        """
        return self.__dict__

    def __repr__(self):
        return "Trade(symbol: {}, direction: {}, offset_flag: {}, transact_amount: {}, transact_price: {}, " \
               "filled_time: {}, commission: {}, slippage: {})"\
            .format(self.symbol, self.direction, self.offset_flag, self.transact_amount, self.transact_price,
                    self.filled_time, self.commission, self.slippage)


class MetaTrade(Trade):
    """
    Meta trade
    """

    def __init__(self, order_id=None, symbol=None, direction=None, offset_flag=None,
                 transact_amount=None, transact_price=None, filled_time=None,
                 commission=None, slippage=None, portfolio_id=str(uuid.uuid1())):
        super(MetaTrade, self).__init__(order_id, symbol, direction, offset_flag, transact_amount,
                                        transact_price, filled_time, commission, slippage)
        self.portfolio_id = portfolio_id

    @classmethod
    def from_request(cls, request):
        """
        Generate new trade from request

        Args:
            request(dict): request database
        """
        return cls(**request)

    @classmethod
    def from_query(cls, query_data):
        """
        Recover existed order from query database

        Args:
            query_data(dict): query database
        """
        return cls.from_request(query_data)

    def to_mongodb_item(self):
        """
        To mongodb item
        """
        return self.to_dict()

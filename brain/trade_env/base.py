"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:
# **********************************************************************************#
"""
from .. core.enums import BaseEnums


class LongShort(BaseEnums):
    """
    Long/short enums.
    """
    LONG = 1
    SHORT = -1


class TradingAction(BaseEnums):
    """
    Trading action enums.
    """
    BUY = 'BUY'     # long open
    SELL = 'SELL'   # long close
    SHORT = 'SHORT'     # short open
    COVER = 'COVER'     # short close
    FAIR = 'FAIR'       # hold


__all__ = [
    'LongShort',
    'TradingAction'
]

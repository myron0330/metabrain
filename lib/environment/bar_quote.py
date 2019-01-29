"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Observer.
# **********************************************************************************#
"""
from .. data.database_api import *


class BarQuote(object):
    """
    Observer who provide real-time observations.
    """
    def __init__(self, bar_dict=None):
        """
        Initialize the bar dict information.

        Args:
            bar_dict(dict): bar dict
        """
        self.bar_dict = bar_dict or dict()

    def load_history(self, **kwargs):
        """
        Load data from history data.

        Args:
            **kwargs:

        Returns:

        """
        self.bar_dict

    def push(self, **kwargs):
        """
        Push the current bar data according to condition claim from outside.

        Args:
            **kwargs(**dict): key-word arguments

        Returns:
            object: observation
        """
        raise NotImplementedError

    def reset(self, **kwargs):
        """
        Reset the observer.
        Args:
            **kwargs(**dict): key-word arguments

        Returns:
            object: observation
        """
        raise NotImplementedError


__all__ = [
    'BarQuote'
]

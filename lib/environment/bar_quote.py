"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Observer.
# **********************************************************************************#
"""


class BarQuote(object):
    """
    Observer who provide real-time observations.
    """
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

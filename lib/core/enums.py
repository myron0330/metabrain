"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Enums.
# **********************************************************************************#
"""


class BaseEnums(object):
    """
    Base enums class.
    """
    @classmethod
    def is_attribute(cls, attribute):
        """
        Judge whether the input attribute name belongs to current enum.

        Args:
            attribute(string): attribute

        Returns:
            boolean: belongs or not
        """
        return bool(getattr(cls, attribute, False))

    @classmethod
    def has_value(cls, value):
        """
        Judge whether the input value belongs to current enum's values.

        Args:
            value(object): target value

        Returns:
            boolean: belongs or not
        """
        return value in cls.__dict__.values()

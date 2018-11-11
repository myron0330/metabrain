"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:
# **********************************************************************************#
"""
import traceback


error_wrapper = (lambda code, message: {'code': code, 'data': message, 'msg': message})


def deal_with_exception(func):
    """
    Deal with exception.
    """
    def _decorator(obj, *args, **kwargs):
        try:
            response = func(obj, *args, **kwargs)
        except tuple(Exceptions.error_types()) as error_code:
            response = error_code.args[0]
        except:
            response = error_wrapper(500, 'Exception unknown.'.format(func.func_name))
        return response
    return _decorator


class EnvironmentsException(Exception):
    """
    Exception in module environments.
    """
    pass


class Exceptions(object):
    """
    Enumerate exceptions.
    """
    INVALID_INITIALIZE_PARAMETERS = EnvironmentsException(error_wrapper(500, 'You have invalid input parameters'
                                                                             ' when you initialize your environment.'))

    @classmethod
    def enumerates(cls):
        return [value for attr, value in cls.__dict__.items()]

    @classmethod
    def error_types(cls):
        return tuple([
            EnvironmentsException
        ])

"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: concurrent files.
#   Author: Myron
# **********************************************************************************#
"""
import multiprocessing


def _function_mask(func_detail):
    """
    Function mask for translate parameters.

    Args:
        func_detail(tuple): func, args

    Returns:
        object: result of functions.
    """
    func, args = func_detail
    return func(*args)


class ProcessPool(object):
    """
    Multiple process pool.
    """
    DEFAULT_PROCESSORS = multiprocessing.cpu_count()

    def __init__(self, func, args_batch):
        self.func = func
        self.args_batch = list(args_batch)

    def execute(self, processors=DEFAULT_PROCESSORS):
        """
        Pool map executor.
        Args:
            processors: processor number.

        Returns:
            object: result.
        """
        pool = multiprocessing.Pool(processes=processors)
        func_detail_batch = zip([self.func] * len(self.args_batch), self.args_batch)
        result = pool.map_async(_function_mask, func_detail_batch)
        pool.close()
        pool.join()
        return result.get()


if __name__ == '__main__':
    def test_func(a, b):
        """
        Test functions.
        """
        print('test {}, {}, {}'.format(a, b, a + b))
        return a + b

    test_args_batch = [(1, 2), (2, 3), (3, 4), (4, 5)]
    x = ProcessPool(test_func, args_batch=test_args_batch)
    data = x.execute(processors=32)
    print(data)

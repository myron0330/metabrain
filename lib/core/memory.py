# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Memory collections.
# **********************************************************************************#
import random
from collections import deque


class ReplayMemory(object):
    """
    Replay memory for collecting latest states.
    """
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = deque([], maxlen=capacity)

    def push(self, item):
        """
        Push item to memory by back-end.

        Args:
            item(object): class object instance.
        """
        self.memory.append(item)

    def push_left(self, item):
        """
        Push item to memory by front-end.

        Args:
            item(object): class object instance.
        """
        self.memory.appendleft(item)

    def extend(self, items):
        """
        Extend items to memory by back-end.

        Args:
            items(list): list of items.
        """
        self.memory.extend(items)

    def extend_left(self, items):
        """
        Extend items to memory by front-end.

        Args:
            items(list): list of items.
        """
        self.memory.extendleft(items)

    def pop(self):
        """
        Pop item by back-end.
        """
        return self.memory.pop()

    def pop_left(self):
        """
        Pop item by front-end.
        """
        return self.memory.popleft()

    def sample(self, batch_size):
        """
        Randomly generate samples according to input batch size.

        Args:
            batch_size(int): expected batch size
        """
        return random.sample(self.memory, batch_size)

    def __len__(self):
        """
        Current length of memory.
        """
        return len(self.memory)

"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Redis base.
#     Desc: define general redis base for the service.
# **********************************************************************************#
"""
import json
import redis
from lib import redis_host, redis_port
_pool = redis.ConnectionPool(host=redis_host, port=redis_port)


def get_redis_client():
    """
    Get redis client.
    """
    return redis.StrictRedis(connection_pool=_pool)


class RedisCollection(object):
    """
    Redis collections enumerate
    """
    order = 'spas.order'
    position = 'spas.position'
    trade = 'spas.trade'
    cash = 'spas.cash'
    changed_portfolio_id = 'spas.changed_portfolio_id'
    cancel_order_status = 'spas.cancel_order_status'
    reset_order_status = 'spas.reset_order_status'


class RedisSet(object):
    """
    thread safe implementation
    """
    def __init__(self, key='changed_portfolio_set'):
        # self.client = client
        self.key = key

    def add_elements_to_set(self, elements, key=None):
        key = key or self.key
        get_redis_client().sadd(key, *elements)

    def get_and_pop_all_elements(self, key=None):
        key = key or self.key
        result = []
        client = get_redis_client()
        while client.scard(key) > 0:
            item = client.spop(key)
            if item:
                result.append(item)
        return result

    def get_all_elements(self, key=None):
        key = key or self.key
        return get_redis_client().smembers(key)

    def pop_elements(self, elements, key=None):
        key = key or self.key
        get_redis_client().srem(key, *elements)

    def is_member(self, element, key=None):
        key = key or self.key
        return get_redis_client().sismember(key, element)


class RedisQueue(object):
    """
    thread safe implementation
    """

    def __init__(self, key='queue'):
        """
        Redis queue
        Args:
            client: redis client
            key(string): redis key
        """
        # self._client = None
        self.key = key

    def size(self, key=None):
        """
        Return current size of the queue

        Args:
            key(string): specific redis queue key
        """
        key = key or self.key
        return get_redis_client().llen(key)

    def empty(self, key=None):
        """
        Return True if the queue is empty, False otherwise

        Args:
            key(string): specific redis queue key
        """
        key = key or self.key
        return self.size(key) == 0

    def put(self, items, key=None):
        """
        Put item or item list into the queue

        Args:
            items(string or list): items
            key(string): specific redis queue key
        """
        key = key or self.key
        if isinstance(items, str):
            get_redis_client().rpush(key, items)
        elif isinstance(items, (tuple, list)):
            items = map(lambda x: json.dumps(x), items)
            get_redis_client().rpush(key, *items)

    def get(self, key=None, block=True, timeout=None):
        """
        Remove and return an item from the queue.
        Args:
            key(string): specific redis queue key
            block(boolean): if block is true and timeout is None (the default),
                            block if necessary until an item is available
            timeout(float): time out setting.
        """
        key = key or self.key
        if block:
            item = get_redis_client().blpop(key, timeout=timeout)
        else:
            item = (None, get_redis_client().lpop(key))
        if item:
            item = item[1]
        return json.loads(item)

    def get_nowait(self, key=None):
        """
        Equivalent to get(False)

        Args:
            key(string): specific redis queue key
        """
        key = key or self.key
        return self.get(key, False)

    def get_all(self, key=None):
        """
        Get all items from key

        Args:
            key(string): specific redis queue key
        """
        key = key or self.key
        items = list()
        while self.size(key):
            items.append(self.get_nowait(key))
        return items

    def clear(self, key=None):
        """
        Clear redis queue

        Args:
            key(string): specific redis queue key
        """
        key = key or self.key
        get_redis_client().ltrim(key, self.size(key), self.size(key))


redis_queue = RedisQueue()
redis_set = RedisSet()

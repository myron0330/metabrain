"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Redis API.
#     Desc: define general redis API for the service.
# **********************************************************************************#
"""
import json
import time
from datetime import datetime
from .redis_base import get_redis_client, RedisCollection, redis_queue, redis_set
from ..core.enum import SecuritiesType
from ..core.schema import (SchemaType, OrderSchema, PositionSchema, TradeSchema)
from ..utils.error_utils import Errors
from ..utils.dict_utils import DefaultDict


def redis_lock(name):
    try:
        result = get_redis_client().set(name, 0, ex=60, nx=True)
        if result:
            return True
        return False
    except Exception:
        return False


def redis_unlock(name, timeout=None):
    try:
        if timeout:
            time.sleep(timeout)
        get_redis_client().delete(name)
    except Exception:
        pass


def _query_from_(collection, portfolio_id=None):
    """
    Query collection data from database

    Args:
        collection(collection): mongodb collection
        portfolio_id(string or list of string): optional, portfolio_id

    Returns:
        dict: collection data
    """
    if portfolio_id is None:
        response = get_redis_client().hgetall(collection)
        response = {key: json.loads(value) for key, value in response.iteritems() if value is not None}
    elif isinstance(portfolio_id, (str, unicode)):
        value = get_redis_client().hget(collection, portfolio_id)
        if value:
            response = {portfolio_id: json.loads(value)}
        else:
            response = {}
    elif isinstance(portfolio_id, (list, tuple, set)):
        temp = get_redis_client().hmget(collection, *portfolio_id)
        response = {}
        for idx, key in enumerate(portfolio_id):
            if temp[idx]:
                response[key] = json.loads(temp[idx])
    else:
        raise Errors.INVALID_PORTFOLIO_ID

    return response


def _query_from_queue_(collection):
    """
    Query collection data from redis queue

    Args:
        collection(collection): mongodb collection

    Returns:
        dict: collection data
    """
    items = redis_queue.get_all(key=collection)
    return items


def _dump_to_(collection, mapping):
    """
    Query collection data from database

    Args:
        collection(collection): mongodb collection
        mapping(dict): data, composite dict
    Returns:
        list: collection data
    """
    for key, value in mapping.iteritems():
        mapping[key] = json.dumps(value)
    if mapping:
        get_redis_client().hmset(collection, mapping)


def query_from_redis(schema_type, portfolio_id=None, securities_type=SecuritiesType.SECURITY, **kwargs):
    """
    Query data from redis

    Args:
        schema_type(string): schema type
        portfolio_id(None, str or list): None--> all;
        securities_type(obj): securities type
    """
    normalize_object = kwargs.get('normalize_object', True)
    securities_type = kwargs.get('securities_type', securities_type)
    if schema_type == SchemaType.order:
        query_data = _query_from_(RedisCollection.order, portfolio_id)
        for key in query_data.keys():
            query_data[key] = OrderSchema.from_query(
                query_data[key], normalize_object=normalize_object, securities_type=securities_type)
        return query_data
        # return {
        #     key: OrderSchema.from_query(schema, normalize_object=normalize_object)
        #     for key, schema in query_data.iteritems()
        # }
    if schema_type == SchemaType.position:
        query_data = _query_from_(RedisCollection.position, portfolio_id)
        for key in query_data.keys():
            query_data[key] = PositionSchema.from_query(query_data[key], securities_type=securities_type)
        return query_data
        # return {
        #     key: PositionSchema.from_query(schema, securities_type=SecuritiesType.SECURITY)
        #     for key, schema in query_data.iteritems()
        # }
    if schema_type == SchemaType.futures_position:
        query_data = _query_from_(RedisCollection.position, portfolio_id)
        for key in query_data.keys():
            query_data[key] = PositionSchema.from_query(query_data[key], securities_type=SecuritiesType.FUTURES)
        return query_data
    if schema_type == SchemaType.trade:
        query_data = _query_from_queue_(RedisCollection.trade)
        current_date = datetime.today().strftime('%Y%m%d')
        schema_items = DefaultDict({'portfolio_id': None, 'date': current_date, 'trades': list()})
        for item in query_data:
            portfolio_id = item['portfolio_id']
            schema_items[portfolio_id]['portfolio_id'] = portfolio_id
            schema_items[portfolio_id]['trades'].append(item)
        return {key: TradeSchema.from_query(schema) for key, schema in schema_items.iteritems()}
    raise Errors.INVALID_SCHEMA_TYPE


def dump_schema_to_redis(schema_type, schema, **kwargs):
    """
    Dump schema to redis

    Args:
        schema_type(string): schema type
        schema(schema or dict of schema): schema object
    """
    if schema_type == SchemaType.order:
        collection = RedisCollection.order
    elif schema_type == SchemaType.position:
        collection = RedisCollection.position
    else:
        raise Errors.INVALID_SCHEMA_TYPE
    to_dict = kwargs.get('to_dict', True)
    if isinstance(schema, dict):
        data = {_id: curr_schema.to_redis_item(to_dict=to_dict) for _id, curr_schema in schema.iteritems()}
    else:
        data = {schema.portfolio_id: schema.to_redis_item(to_dict=to_dict)}
    _dump_to_(collection, data)


def delete_keys_redis(*delete_keys):
    """
    Delete one or more keys in redis

    Args:
        delete_keys(tuple): keys will be deleted in redis
    Returns:
        result(int): deleted amounts
    """
    retry_nums = 0

    while retry_nums < 3:
        result = get_redis_client().delete(*delete_keys)

        if result != len(delete_keys):
            retry_nums += 1
        else:
            return result

    not_deleted = set(delete_keys) & set(get_redis_client().keys())
    result = len(delete_keys) - len(not_deleted)

    return result


def delete_items_in_redis(schema_type, keys):
    """
    Delete items in redis

    Args:
        schema_type(string): schema type
        keys(list): keys
    """
    if schema_type == SchemaType.order:
        collection = RedisCollection.order
    elif schema_type == SchemaType.position:
        collection = RedisCollection.position
    else:
        raise Errors.INVALID_SCHEMA_TYPE
    get_redis_client().hdel(collection, *keys)


def add_items_to_redis_set(schema_type, items):
    if schema_type == SchemaType.changed_portfolio_id:
        collection = RedisCollection.changed_portfolio_id
    elif schema_type == SchemaType.cancel_order_status:
        collection = RedisCollection.cancel_order_status
    elif schema_type == SchemaType.reset_order_status:
        collection = RedisCollection.reset_order_status
    else:
        raise Errors.INVALID_SCHEMA_TYPE
    redis_set.add_elements_to_set(items, key=collection)


def get_and_pop_all_elements_from_set(schema_type):
    if schema_type == SchemaType.changed_portfolio_id:
        collection = RedisCollection.changed_portfolio_id
    elif schema_type == SchemaType.cancel_order_status:
        collection = RedisCollection.cancel_order_status
    elif schema_type == SchemaType.reset_order_status:
        collection = RedisCollection.reset_order_status
    else:
        raise Errors.INVALID_SCHEMA_TYPE
    return redis_set.get_and_pop_all_elements(collection)


def get_all_elements(schema_type):
    """
    Get all elements.

    Args:
        schema_type(string): schema type
    """
    if schema_type == SchemaType.changed_portfolio_id:
        collection = RedisCollection.changed_portfolio_id
    elif schema_type == SchemaType.cancel_order_status:
        collection = RedisCollection.cancel_order_status
    elif schema_type == SchemaType.reset_order_status:
        collection = RedisCollection.reset_order_status
    else:
        raise Errors.INVALID_SCHEMA_TYPE
    return redis_set.get_all_elements(collection)


def pop_elements(schema_type, elements):
    """
    Pop elements from current redis set.

    Args:
        schema_type(string): schema type
        elements(list): element list
    """
    if schema_type == SchemaType.changed_portfolio_id:
        collection = RedisCollection.changed_portfolio_id
    elif schema_type == SchemaType.cancel_order_status:
        collection = RedisCollection.cancel_order_status
    elif schema_type == SchemaType.reset_order_status:
        collection = RedisCollection.reset_order_status
    else:
        raise Errors.INVALID_SCHEMA_TYPE
    return redis_set.pop_elements(elements, key=collection)


def is_member(schema_type, element):
    """
    Judge the membership of element.

    Args:
        schema_type(string): schema type
        element(string): element
    """
    if schema_type == SchemaType.changed_portfolio_id:
        collection = RedisCollection.changed_portfolio_id
    elif schema_type == SchemaType.cancel_order_status:
        collection = RedisCollection.cancel_order_status
    elif schema_type == SchemaType.reset_order_status:
        collection = RedisCollection.reset_order_status
    else:
        raise Errors.INVALID_SCHEMA_TYPE
    return redis_set.is_member(element, key=collection)


def get_all_keys_in_redis_hashmap(schema_type):
    if schema_type == SchemaType.order:
        collection = RedisCollection.order
    elif schema_type == SchemaType.position:
        collection = RedisCollection.position
    else:
        raise Errors.INVALID_SCHEMA_TYPE
    return get_redis_client().hkeys(collection)


__all__ = [
    'get_redis_client',
    'query_from_redis',
    'dump_schema_to_redis',
    'delete_items_in_redis',
    'delete_keys_redis',
    'add_items_to_redis_set',
    'get_all_elements',
    'get_all_keys_in_redis_hashmap',
    'get_and_pop_all_elements_from_set',
    'pop_elements',
    'is_member',
    'redis_lock',
    'redis_unlock'
]

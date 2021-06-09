#!/usr/bin/env python3
""" 0.Writing strings to Redis  """
from typing import Callable, Optional, Union
import redis
import uuid


def count_calls(method: Callable) -> Callable:
    """
    Create and return function that increments the count
    for that key every time the method is called and returns
    the value returned by the original method.
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """
        wrapper function
        """
        self._redis.incr(key)
        return method(self, *args, **kwds)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs
    for a particular function.
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args):
        """
        wrapper function
        """
        self._redis.rpush("{}:inputs".format(key), str(args))
        result = method(self, *args)
        self._redis.rpush("{}:outputs".format(key),
                          str(result))
        return result
    return wrapper


def replay(method: Callable):
    """Displays nthe history of calls
    """
    r = method.__self__._redis
    method_name = method.__qualname__

    inputs = r.lrange("{}:inputs".format(method_name), 0, -1)
    outputs = r.lrange("{}:outputs".format(method_name), 0, -1)

    print("{} was called {} times:".format(method_name,
          r.get(method_name).decode("utf-8")))
    for i, o in tuple(zip(inputs, outputs)):
        print("{}(*('{}',)) -> {}".format(method_name, i.decode("utf-8"),
              o.decode("utf-8")))


class Cache:
    """ Cache """
    def __init__(self):
        """ constructor """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Generates a random key """
        id = str(uuid.uuid4())
        self._redis.set(id, data)
        return id

    def get_str(self, key):
        """  parametrize Cache.get with the correct conversion function """
        return self.get(key, str)

    def get_int(self, key):
        """  parametrize Cache.get with the correct conversion function """
        return self.get(key, int)

    def get(self, key: str, fn: Optional[Callable] = None):
        """ convert the data back to the desired format """
        val = self._redis.get(key)
        return val if not fn else fn(val)

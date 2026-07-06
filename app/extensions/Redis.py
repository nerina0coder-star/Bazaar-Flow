from typing import List, Dict, Any

import redis
from flask import Flask
from typeguard import typechecked


class Redis:
    @typechecked
    def __init__(self, app: Flask | None=None, less_calls: bool = False):
        self._selected = None
        self._client = None
        self.less_calls = less_calls
        if app is not None:
            self.init_app(app)

    def __del__(self):
        if self._client is not None:
            self._client.close()

    def __repr__(self):
        return '<Redis connection>'

    def __str__(self):
        return repr(self)

    @typechecked
    def __setitem__(self, key: list | str, value: list | dict | Any):
        if isinstance(key, list) and isinstance(value, list) and not len(value) == len(key):
            raise TypeError('Redis pairs must be equal in length')
        if isinstance(key, list) and isinstance(value, list):
            adding = dict(zip(key, value))
            return self[adding]
        if isinstance(key, str) and isinstance(value, dict):
            self._client.hset(value)
        return self._client.set(key, value)

    @typechecked
    def __getitem__(self, key: str | List[str] | Dict[str, Any]):
        if isinstance(key, dict):
            return self._client.mset(key)
        if isinstance(key, list):
            return self._client.mget(key)
        if isinstance(key, str) and " from " in key:
            index = key.index(" from ")
            theitem = key[:index]
            thefrom = key[index + len(" from "):]

            return self._client.hget(thefrom, theitem)

        if key in self:
            key_type = "string" if self.less_calls else self._client.type(key)
            if key_type == "string":
                returned: str = self._client.get(key)
                if returned.isdigit():
                    return int(returned)
                return returned
            elif key_type == "hash":
                return self._client.hget(key)

        return None

    @typechecked
    def __delitem__(self, key):
        if key in self:
            return self._client.unlink(key)
        return None

    @typechecked
    def __contains__(self, key: str):
        return self._client.exists(key) == 1

    @typechecked
    def __add__(self, other: int) -> int:
        if self._selected is None: raise RuntimeError("No item selected")
        return int(self._client.incr(self._selected, other))

    @typechecked
    def init_app(self, app: Flask):
        app.config.setdefault('REDIS_URL', 'redis://localhost:6379')
        self._client = redis.StrictRedis.from_url(app.config['REDIS_URL'], decode_responses=True)

        @app.teardown_appcontext
        def teardown_appcontext(_exception):
            if self._client is not None:
                self._client.close()

    @typechecked
    def set(self, key: List | str, value: List | str, pairs: Dict[str, Any] | None = None, expire: int | None =None):
        if not key or not value:
            return None
        if pairs and not (key or value):
            self._client.msetex(pairs, ex=expire) if expire else self[pairs]
        if isinstance(key, list) and isinstance(value, list):
            adding = dict(zip(key, value))
            self._client.msetex(adding, ex=expire) if expire else self._client.mset(adding)
            return None
        if isinstance(key, str):
            if expire is None:
                self[key] = value
                return
            return self._client.setex(key, expire, value)
        raise TypeError("Something went wrong when setting redis pair(s). "
                        f"Got {type(key).__name__} key(s), {type(value).__name__} value(s), "
                        f"{type(pairs).__name__} pairs and {type(expire).__name__} expire.")

    @typechecked
    def push(self, key: str, value: Any, append: bool = False):
        if not isinstance(key, str):
            raise TypeError('Redis key must be a string')
        if self.less_calls and not self._client.type(key) == 'hash':
            raise redis.DataError(f'The stored object is not a dict, but a {self._client.type(key)}')

        self._client.rpush(value) if append else self._client.lpush(value)

    @typechecked
    def pop(self, start: bool = False):
        if not isinstance(start, bool):
            raise TypeError('Redis index must be an integer')

        return self._client.rpop() if start else self._client.lpop()

    @typechecked
    def queue_get(self, start: bool = True):
        return self.pop(start)

    @typechecked
    def queue_put(self, name: str, value: Any, start: bool = False):
        return self.push(name, value, start)

    @typechecked
    def make_queue(self, name: str):
        self[name] = []

    @typechecked
    def stack_get(self, start: bool = True):
        return self.pop(start)

    @typechecked
    def stack_put(self, name: str, value: Any, start: bool = True):
        return self.push(name, value, start)

    @typechecked
    def make_stack(self, name: str):
        self[name] = []

    @typechecked
    def get(self, keys: List | str):
        return self[keys]

    @typechecked
    def __call__(self, keyname: str) -> "Redis":
        """Used to select an element from the redis Database.
        Args:
            keyname:arg The key to the item, the value must be an int."""
        self._selected = keyname
        return self

    @typechecked
    def life(self, key):
        if key not in self:
            return None
        return self._client.ttl(key)

    @typechecked
    def incr(self, key, amount=1):
        if key not in self:
            return None
        return self._client.incr(key, amount)

    @typechecked
    def decr(self, key, amount=1):
        if key not in self:
            return None
        return self._client.decr(key, amount)
from collections.abc import Iterable, Iterator, MutableSet
from typing import cast
from uuid import UUID

import redis

# https://redis.io/docs/latest/commands/sadd/

_REDIS_URI = "redis://localhost:6379/0"
_REDIS_SET_NAME = "set_name"


class RedisMutableSetAbc[T](MutableSet[T]):
    def __init__(
        self,
        iterable: Iterable[T] = (),
        clear: bool = True,
        redis_uri: str = _REDIS_URI,
        redis_set_name: str = _REDIS_SET_NAME,
    ) -> None:
        self._conn = redis.from_url(url=redis_uri)
        self.name = redis_set_name

        if clear:
            self.clear()

        if iterable:
            for value in iterable:
                self.add(value)

    # redis interface
    def _add(self, item: str) -> None:
        self._conn.sadd(self.name, item)

    def _discard(self, item: str) -> None:
        self._conn.srem(self.name, item)

    def _sismember(self, item: str) -> bool:
        if self._conn.sismember(self.name, item) == 1:
            return True

        return False

    def _all(self) -> set[bytes]:
        # 异步模式下，返回的是 collections.abc.Awaitable[set[bytes]]
        return cast("set[bytes]", self._conn.smembers(self.name))

    # set methods
    def __len__(self) -> int:
        # 异步模式下，返回的是 Awaitable[int]
        return self._conn.scard(self.name)

    def add(self, value: T) -> None:
        raise NotImplementedError  # pragma: no cover

    def clear(self) -> None:
        self._conn.delete(self.name)


class RedisSetStr(RedisMutableSetAbc[str]):
    def add(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError

        super()._add(value)

    def discard(self, value: str) -> None:
        super()._discard(value)

    def __contains__(self, item: object) -> bool:
        if not isinstance(item, str):
            return False
        return self._sismember(item)

    def __iter__(self) -> Iterator[str]:
        return iter(item.decode("utf-8") for item in self._all())

    def __repr__(self) -> str:
        return ", ".join([item.decode("utf-8") for item in self._all()])


class RedisSetInt(RedisMutableSetAbc[int]):
    def add(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError

        super()._add(str(value))

    def discard(self, value: int) -> None:
        super()._discard(str(value))

    def __contains__(self, item: object) -> bool:
        return self._sismember(str(item))

    def __iter__(self) -> Iterator[int]:
        return iter(int(item) for item in super()._all())

    def __repr__(self) -> str:
        return ", ".join([item.decode("utf-8") for item in self._all()])


class RedisSetUUID(RedisMutableSetAbc[UUID]):
    def add(self, value: UUID) -> None:
        if not isinstance(value, UUID):
            raise TypeError

        super()._add(value.hex)

    def discard(self, value: UUID) -> None:
        super()._discard(value.hex)

    def __contains__(self, value: object) -> bool:
        if not isinstance(value, UUID):
            return False
        return self._sismember(value.hex)

    def __iter__(self) -> Iterator[UUID]:
        return iter(UUID(item.decode("utf-8")) for item in super()._all())

    def __repr__(self) -> str:
        return ", ".join([str(UUID(item.decode("utf-8"))) for item in self._all()])

from uuid import UUID

import redis


class DataSetRedisAbs:
    def __init__(self, url: str, name: str):
        self.conn = redis.from_url(url=url)
        self.name = name

    def _add(self, item: bytes):
        self.conn.sadd(self.name, item)

    def pop(self):
        raise

    def _remove(self, item: bytes):
        self.conn.srem(self.name, item)

    def _all(self) -> set[bytes]:
        # 异步模式下，返回的是 collections.abc.Awaitable[set[bytes]]
        return self.conn.smembers(self.name)  # type: ignore

    def clear(self):
        return self.conn.delete(self.name)


class DataSetStr(DataSetRedisAbs):
    def add(self, item: str):

        super()._add(item.encode("utf-8"))

    def remove(self, item: str):

        super()._remove(item.encode("utf-8"))

    def all(self) -> list[str]:
        return [item.decode("utf-8") for item in super()._all()]


class DataSetInt(DataSetRedisAbs):
    """
    int.to_bytes(length, byteorder, *, signed=False)
    需要指定转换的长度，这导致通用型变差，不如统一转换成 str 再转换为 bytes
    """

    def add(self, item: int):

        super()._add(str(item).encode("utf-8"))

    def remove(self, item: int):

        super()._remove(str(item).encode("utf-8"))

    def all(self) -> list[int]:
        return [int(item.decode("utf-8")) for item in super()._all()]


class DataSetUUID(DataSetRedisAbs):
    def add(self, item: UUID | str):
        if isinstance(item, str):
            item = UUID(item)

        super()._add(item.bytes)

    def remove(self, item: UUID | str):
        if isinstance(item, str):
            item = UUID(item)

        super()._remove(item.bytes)

    def all(self) -> list[UUID]:
        return [UUID(bytes=item) for item in super()._all()]

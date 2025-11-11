from uuid import UUID

import redis


class DataSetRedisAbs:
    def __init__(self, url: str, name: str):
        self.conn = redis.from_url(url=url)
        self.name = name

    def add(self, item: bytes):
        self.conn.sadd(self.name, item)

    def pop(self):
        raise

    def remove(self, item: bytes):
        self.conn.srem(self.name, item)

    def all(self) -> set[bytes]:
        return self.conn.smembers(self.name)

    def purge(self):
        return self.conn.delete(self.name)


class DataSetInt(DataSetRedisAbs):
    """
    int.to_bytes(length, byteorder, *, signed=False)
    需要指定转换的长度，这导致通用型变差，不如统一转换成 str 再转换为 bytes
    """

    def add(self, item: int | str):
        if isinstance(item, int):
            item = str(item)

        super().add(bytes(item, "utf-8"))

    def remove(self, item: int | str):
        if isinstance(item, int):
            item = str(item)

        super().remove(bytes(item, "utf-8"))

    def all(self) -> list[str]:
        return [str(item, "utf-8") for item in super().all()]


class DataSetUUID(DataSetRedisAbs):
    def add(self, item: UUID | str):
        if isinstance(item, str):
            item = UUID(item)

        super().add(item.bytes)

    def remove(self, item: UUID | str):
        if isinstance(item, str):
            item = UUID(item)

        super().remove(item.bytes)

    def all(self) -> list[UUID]:
        return [UUID(bytes=item) for item in super().all()]


if __name__ == "__main__":
    r = DataSetInt(url="redis://localhost:6379/2", name="test")
    r.purge()
    r.add(1)
    print(r.all())
    r.add("2")
    print(r.all())
    r.remove("2")
    print(r.all())
    r.remove(1)
    print(r.all())

    from uuid import uuid4

    r = DataSetUUID(url="redis://localhost:6379/2", name="test")
    r.purge()
    r.add(uuid4())
    print(r.all())
    r.add(uuid4().hex)
    print(r.all())

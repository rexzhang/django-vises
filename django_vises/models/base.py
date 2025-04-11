from datetime import datetime
from typing import Any
from uuid import uuid4

import arrow
from django.db import models
from django.utils.timezone import now


class ModelBaseObjectNoId(models.Model):
    """基本数据库模型 - 对象型 - 无 id
    创建时间，最后更新时间, 需要继承者自行实现 __str__()
    """

    # 记录创建时间
    time_created = models.DateTimeField(
        auto_now_add=True,
    )

    # 记录最后更新时间
    time_last_updated = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True


class ModelBaseObject(ModelBaseObjectNoId):
    """基本数据库模型 - 对象型
    创建时间，最后更新时间
    """

    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.id}"


class ModelBaseRecord(models.Model):
    """基本数据库模型 - 记录／日志型
    创建时间，无更新需求
    """

    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)

    # 记录创建时间
    time_created = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.id}"


class KeyValueManager(models.Manager):
    def set_value(self, key: str, value, group: str | None = None):
        self.get_queryset().update_or_create(
            group=group, key=key, defaults={"value": value}
        )
        return

    def get_object(self, key: str, group: str | None = None):
        return super().get_queryset().filter(group=group, key=key).first()

    def get_value(self, key: str, group: str | None = None) -> Any:
        obj = self.get_object(key=key, group=group)
        if obj is None:
            raise

        return obj.value

    def get_value_and_update_time(
        self, key: str, group: str | None = None
    ) -> tuple[list, datetime | None]:
        obj = self.get_object(key=key, group=group)
        if obj is None:
            return [], None

        return obj.value, obj.time_last_updated

    def get_values_by_group(self, group: str) -> dict:
        return dict(
            self.get_queryset()
            .filter(group=group)
            .values_list("key", "value", flat=True)
        )


class ModelBaseKeyValue(ModelBaseObject):
    """基本数据库模型 - 键值对型
    创建时间，最后更新时间
    """

    # group - 可选的一级分组
    group = models.TextField(null=True)
    # key - 必须存在的二级分组
    key = models.TextField(null=False)
    # value
    value = models.JSONField()

    kv_objects = KeyValueManager()

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=["group"]),
            models.Index(fields=["group", "key"]),
        ]

    def __str__(self):
        return f"{self.group}:{self.key}:{self.value}"


class BaseAbstract(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4)

    time_created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.id}"


class BaseObjectAbstract(BaseAbstract):
    time_last_updated = models.DateTimeField(
        auto_now=True,
        db_index=True,
    )

    class Meta:
        abstract = True


class HistoryManager(models.Manager):
    def get_last_x_hour_queryset(self, hours):
        return (
            super()
            .get_queryset()
            .filter(
                datetime__gte=arrow.now()
                .replace(minute=0, second=0, microsecond=0)
                .shift(hours=-hours)
                .datetime
            )
        )

    def get_last_x_day_queryset(self, days):
        return (
            super()
            .get_queryset()
            .filter(
                datetime__gte=arrow.now()
                .replace(hour=0, minute=0, second=0, microsecond=0)
                .shift(days=-days)
                .datetime
            )
        )


class HistoryAbstract(models.Model):
    # Django 不支持多列主键
    # https://docs.djangoproject.com/zh-hans/4.0/faq/models/#do-django-models-support-multiple-column-primary-keys
    # 让 Django 自行创建用于放置 pk 的 id 字段
    # 具体创建为 AutoField/BigAutoField， 取决于 XyzConfig.default_auto_field 设置
    # id = models.BigAutoField(primary_key=True)

    datetime = models.DateTimeField(default=now)

    class Meta:
        abstract = True

#!/usr/bin/env python


from django.db import models

from .base import BaseObjectAbstract


class GeneralObjectManager(models.Manager):
    # 废弃

    def set_value(self, group, key=None, value=None):
        """set|create/update"""
        if key is None:
            key = group

        self.get_queryset().update_or_create(
            group=group,
            key=key,
            defaults={
                "value": value,
            },
        )

        return self.get_queryset().filter(group=group, key=key)

    def get_value(self, group, key=None):
        """get value"""
        if key is None:
            key = group

        obj = self.get_queryset_by_group_and_key(group=group, key=key).first()

        if obj is None:
            return None

        return obj.value

    def get_object(self, group, key=None):
        """get object"""
        return self.get_queryset_by_group_and_key(group=group, key=key).first()

    def get_queryset_by_group(self, group):
        return self.get_queryset().filter(group=group).order_by("key")

    def get_queryset_by_group_and_key(self, group, key=None):
        """get queryset"""
        if key is None:
            return self.get_queryset().filter(group=group)

        else:
            return self.get_queryset().filter(group=group, key=key)


class GeneralObjectAbstract(BaseObjectAbstract):
    """An abstract base class implementing for GeneralObject"""

    # 废弃

    group = models.CharField(
        # 分类或用途
        max_length=50,
        null=False,
    )
    key = models.CharField(
        max_length=50,
        null=False,
    )
    value = models.JSONField(
        null=True,
    )

    objects = GeneralObjectManager()

    class Meta:
        abstract = True
        unique_together = (("group", "key"),)
        db_table = "django_vises_general_object"

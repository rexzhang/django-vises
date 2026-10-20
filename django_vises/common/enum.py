from __future__ import annotations

from enum import Enum
from functools import cache
from typing import Any, Self


class EnumUpperAbc(Enum):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._init_basic_value()
        self._init_other_value(*args, **kwargs)

    def _init_basic_value(self) -> None:
        # 同上, _value_ 的赋值错误是 enum 插件误判的连带产物
        self._value_ = self._name_.upper()  # type: ignore[assignment]

    def _init_other_value(self, *args: Any, **kwargs: Any) -> None:
        label = args[0]
        if not isinstance(label, str):
            self.label = str(label)
        else:
            self.label = label

    @classmethod
    def _missing_(cls, value: object) -> Self | None:
        if not isinstance(value, str):
            raise ValueError(f"Invalid {cls.__name__} value: {value}")

        try:
            return cls[value.upper()]
        except KeyError:
            return cls[cls.default_value(value).upper()]

    @classmethod
    def default_value(cls, value: object) -> str:
        raise ValueError(f"Invalid {cls.__name__} value: {value}")

    @classmethod
    @cache
    def names(cls) -> list[str]:
        return [item.name for item in cls]

    @classmethod
    @cache
    def values(cls) -> list[str]:
        # mypy 的 enum 插件无法把 classmethod(cache(f)) 识别为描述符,
        # 会把方法误判为枚举成员并污染成员迭代与 _value_ 的类型 (mypy 2.4)
        return [item.value for item in cls]  # type: ignore[misc]


class EnumLowerAbc(EnumUpperAbc):
    def _init_basic_value(self) -> None:
        self._value_ = self._name_.lower()

    @classmethod
    def _missing_(cls, value: object) -> Self | None:
        if not isinstance(value, str):
            raise ValueError(f"Invalid {cls.__name__} value: {value}")

        try:
            return cls[value.lower()]
        except KeyError:
            return cls[cls.default_value(value).lower()]


"""
MultiValue Example:

class DAVPasswordType(EnumUpperAbc):
    INVALID = "X", -1

    RAW = ":", 0
    HASHLIB = ":", 4
    DIGEST = ":", 3
    LDAP = "#", 5

    def _init_other_value(self, *args: Any, **kwargs: Any) -> None:
        self.split_char, self.split_count = args

    @classmethod
    def default_value(cls, value: Any) -> str:
        return "INVALID"
"""

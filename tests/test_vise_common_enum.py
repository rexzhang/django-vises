from enum import auto
from typing import Any

import pytest

from django_vises.common.enum import EnumLowerAbc, EnumUpperAbc


class EnumUpper(EnumUpperAbc):
    ONE = auto()
    Two = auto()
    three = "3rD"


class TestStrEnumUpperAbc:
    def test_auto_upper_value(self):
        # _value_ 在 __init__ 中被重写, 静态类型检查器看到的是 auto()/字面量的原始类型
        assert EnumUpper.ONE.value == "ONE"  # type: ignore[comparison-overlap]
        assert EnumUpper.Two.value == "TWO"  # type: ignore[comparison-overlap]
        assert EnumUpper.three.value == "THREE"  # type: ignore[comparison-overlap]

        assert str(EnumUpper.ONE) == "EnumUpper.ONE"
        assert str(EnumUpper.Two) == "EnumUpper.Two"
        assert str(EnumUpper.three) == "EnumUpper.three"

    def test_lable(self):
        assert EnumUpper.ONE.label == "1"
        assert EnumUpper.Two.label == "2"
        assert EnumUpper.three.label == "3rD"

    def test_no_default_value(self):
        with pytest.raises(ValueError):
            EnumUpper("default")

    def test_incorrect_value_type(self):
        with pytest.raises(ValueError):
            EnumUpper(999)

    def test_enum_names_values_and_mapping(self):
        assert EnumUpper.names() == ["ONE", "Two", "three"]
        assert EnumUpper.values() == ["ONE", "TWO", "THREE"]


class EnumLower(EnumLowerAbc):
    ONE = auto()
    Two = auto()
    three = "3rD"


class TestStrEnumLowerAbc:
    def test_auto_upper_value(self):
        # _value_ 在 __init__ 中被重写, 静态类型检查器看到的是 auto()/字面量的原始类型
        assert EnumLower.ONE.value == "one"  # type: ignore[comparison-overlap]
        assert EnumLower.Two.value == "two"  # type: ignore[comparison-overlap]
        assert EnumLower.three.value == "three"  # type: ignore[comparison-overlap]

        assert str(EnumLower.ONE) == "EnumLower.ONE"
        assert str(EnumLower.Two) == "EnumLower.Two"
        assert str(EnumLower.three) == "EnumLower.three"

    def test_lable(self):
        assert EnumLower.ONE.label == "1"
        assert EnumLower.Two.label == "2"
        assert EnumLower.three.label == "3rD"

    def test_no_default_value(self):
        with pytest.raises(ValueError):
            EnumLower("default")

    def test_incorrect_value_type(self):
        with pytest.raises(ValueError):
            EnumLower(999)

    def test_enum_names_values_and_mapping(self):
        assert EnumLower.names() == ["ONE", "Two", "three"]
        assert EnumLower.values() == ["one", "two", "three"]


class StrEnumUpperDefaultValue(EnumUpperAbc):
    ONE = auto()
    Two = auto()

    @classmethod
    def default_value(cls, value) -> str:
        return "ONE"


class TestStrEnumUpperDefaultValue:
    def test(self):
        assert StrEnumUpperDefaultValue("default") == StrEnumUpperDefaultValue.ONE


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


class TestEnumUpperMultiValue:
    def test_default_value(self):
        assert DAVPasswordType("default") == DAVPasswordType.INVALID

    def test_split_value(self):
        assert DAVPasswordType.RAW.split_char == ":"
        assert DAVPasswordType.RAW.split_count == 0

        assert DAVPasswordType.LDAP.split_char == "#"
        assert DAVPasswordType.LDAP.split_count == 5

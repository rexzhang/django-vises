import pytest

from django_vises.db.redis_set import RedisSetStr

from .common import REDIS_URI


@pytest.fixture
def test_values():
    return ("apple", "banana", "cherry")


@pytest.fixture
def empty_str_set():
    return RedisSetStr(redis_uri=REDIS_URI)


@pytest.fixture
def default_str_set(test_values):
    return RedisSetStr(test_values, redis_uri=REDIS_URI)


def test_initial_set_is_empty(empty_str_set):
    """测试一个新创建的集合是否为空。"""
    assert len(empty_str_set) == 0
    assert "test" not in empty_str_set


def test_add_and_membership(empty_str_set):
    """测试添加字符串元素和成员资格。"""
    empty_str_set.add("hello")
    empty_str_set.add("world")
    assert len(empty_str_set) == 2
    assert "hello" in empty_str_set
    assert "python" not in empty_str_set


def test_add_duplicate_string(default_str_set):
    """测试添加重复字符串，长度不应改变。"""
    initial_len = len(default_str_set)
    default_str_set.add("apple")
    assert len(default_str_set) == initial_len


def test_add_empty_string(empty_str_set):
    """测试集合可以存储空字符串。"""
    empty_str_set.add("")
    assert len(empty_str_set) == 1
    assert "" in empty_str_set


def test_discard_existing_element(default_str_set):
    """测试移除一个存在的字符串元素。"""
    default_str_set.discard("banana")
    assert len(default_str_set) == 2
    assert "banana" not in default_str_set


def test_discard_non_existing_element(default_str_set):
    """测试移除一个不存在的元素，不应引发错误。"""
    initial_len = len(default_str_set)
    default_str_set.discard("grape")
    assert len(default_str_set) == initial_len


def test_iteration_and_contents(default_str_set):
    """测试集合的迭代。"""
    expected = {"apple", "banana", "cherry"}
    actual = set(default_str_set)
    assert actual == expected


def test_case_sensitivity(default_str_set):
    """测试字符串集合是大小写敏感的。"""
    # 'Apple' 和 'apple' 是两个不同的元素
    default_str_set.add("Apple")
    assert len(default_str_set) == 4
    assert "Apple" in default_str_set
    assert "apple" in default_str_set  # 保持不变


def test_contains_case_sensitivity(default_str_set):
    """测试成员资格检查是大小写敏感的。"""
    # 集合中有 'apple'
    assert "apple" in default_str_set
    # 集合中没有 'APPLE'
    assert "APPLE" not in default_str_set


def test_type_enforcement_on_add(empty_str_set):
    """测试尝试添加非字符串类型时是否引发 TypeError。"""
    # Pytest 的 pytest.raises 上下文管理器用于检查异常
    with pytest.raises(TypeError):
        empty_str_set.add(123)  # 整数

    with pytest.raises(TypeError):
        empty_str_set.add(True)  # 布尔值

    with pytest.raises(TypeError):
        empty_str_set.add(["list"])  # 列表


def test_repr(default_str_set, test_values):
    """测试 __repr__ 方法。"""
    items = repr(default_str_set).split(", ")
    assert set(items) == set(test_values)


def test_as_set(default_str_set, test_values):
    assert default_str_set == set(test_values)

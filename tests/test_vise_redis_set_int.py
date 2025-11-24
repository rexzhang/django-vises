import pytest

from django_vises.db.redis_set import RedisSetInt

from .common import REDIS_URI


@pytest.fixture
def test_values():
    return (10, 20, 30)


@pytest.fixture
def empty_set():
    return RedisSetInt(redis_uri=REDIS_URI)


@pytest.fixture
def default_int_set(test_values):
    return RedisSetInt(test_values, redis_uri=REDIS_URI)


def test_initial_empty_set_is_empty(empty_set):
    """测试一个新创建的集合是否为空。"""
    assert len(empty_set) == 0
    assert 5 not in empty_set


def test_add_element(empty_set):
    """测试添加一个元素。"""
    empty_set.add(1)
    assert len(empty_set) == 1
    assert 1 in empty_set


def test_add_duplicate_element(default_int_set):
    """测试添加重复元素，长度不应改变。"""
    initial_len = len(default_int_set)
    default_int_set.add(20)  # 20 已经存在
    assert len(default_int_set) == initial_len
    assert 20 in default_int_set


def test_discard_existing_element(default_int_set):
    """测试移除一个存在的元素。"""
    default_int_set.discard(20)
    print(len(default_int_set))
    assert len(default_int_set) == 2
    assert 20 not in default_int_set


def test_discard_non_existing_element(default_int_set):
    """测试移除一个不存在的元素，不应引发错误，长度不应改变。"""
    initial_len = len(default_int_set)
    default_int_set.discard(99)  # 99 不存在
    assert len(default_int_set) == initial_len
    assert 99 not in default_int_set


def test_iteration(default_int_set, test_values):
    """测试集合的迭代。"""
    # 将集合转换为列表并检查所有元素
    items = sorted(list(default_int_set))
    assert items == list(test_values)


def test_type_enforcement_on_add(empty_set):
    """测试尝试添加非整数类型时是否引发 TypeError。"""
    # 使用 pytest.raises 来检查期望的异常
    with pytest.raises(TypeError):
        empty_set.add("hello")

    with pytest.raises(TypeError):
        empty_set.add(3.14)


def test_initialization_with_non_int_raises_error():
    """测试用非 int 迭代器初始化时是否引发 TypeError。"""
    # 异常应在第一次调用 add() 时发生
    with pytest.raises(TypeError):
        RedisSetInt([1, 2, "a", 4])  # type: ignore


def test_repr(default_int_set, test_values):
    """测试 __repr__ 方法。"""
    items = [int(item) for item in repr(default_int_set).split(", ")]
    assert set(items) == set(test_values)


def test_iter(default_int_set):
    """测试 __iter__ 方法。"""
    for item in default_int_set:
        assert isinstance(item, int)

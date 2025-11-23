from uuid import UUID, uuid4

import pytest

from django_vises.db.redis_set import RedisSetUUID


@pytest.fixture
def test_values():
    """返回一个包含三个唯一 UUID 对象的元组。"""
    # 确保每次测试运行时 UUID 都是唯一的
    return (uuid4(), uuid4(), uuid4())


@pytest.fixture
def empty_uuid_set():
    """返回一个空的 UuidMutableSet 实例。"""
    return RedisSetUUID()


@pytest.fixture
def default_uuid_set(test_values):
    """返回一个包含三个 UUID 的实例。"""
    return RedisSetUUID(test_values)


def test_initial_set_is_empty(empty_uuid_set):
    """测试一个新创建的集合是否为空。"""
    assert len(empty_uuid_set) == 0


def test_add_and_membership(empty_uuid_set, test_values):
    """测试添加 UUID 对象和成员资格。"""
    u1, u2, _ = test_values

    empty_uuid_set.add(u1)
    empty_uuid_set.add(u2)

    assert len(empty_uuid_set) == 2
    assert u1 in empty_uuid_set
    assert u2 in empty_uuid_set


def test_add_duplicate_uuid(default_uuid_set, test_values):
    """测试添加重复 UUID,长度不应改变。"""
    initial_len = len(default_uuid_set)
    u1, _, _ = test_values

    default_uuid_set.add(u1)  # u1 已经存在
    assert len(default_uuid_set) == initial_len


def test_discard_existing_uuid(default_uuid_set, test_values):
    """测试移除一个存在的 UUID 元素。"""
    u2 = test_values[1]

    default_uuid_set.discard(u2)
    assert len(default_uuid_set) == 2
    assert u2 not in default_uuid_set


def test_discard_non_existing_uuid(default_uuid_set):
    """测试移除一个不存在的 UUID, 不应引发错误。"""
    initial_len = len(default_uuid_set)

    # 创建一个新的、不在集合中的 UUID
    new_uuid = uuid4()
    default_uuid_set.discard(new_uuid)

    assert len(default_uuid_set) == initial_len


def test_iteration_and_contents(default_uuid_set, test_values):
    """测试集合的迭代。"""
    expected = set(test_values)
    actual = set(default_uuid_set)

    # 因为 UUID 是不可变对象,它们可以被安全地用作 set 元素并进行比较
    assert actual == expected


def test_iteration(default_uuid_set, test_values):
    """测试集合的迭代。"""
    # 将集合转换为列表并检查所有元素
    items = sorted(list(default_uuid_set))
    assert items == sorted(test_values)


def test_initialization_with_non_int_raises_error():
    """测试用非 int 迭代器初始化时是否引发 TypeError。"""
    # 异常应在第一次调用 add() 时发生
    with pytest.raises(TypeError):
        RedisSetUUID([uuid4(), uuid4(), 4, "aa"])  # type: ignore


def test_repr(default_uuid_set, test_values):
    """测试 __repr__ 方法。"""
    items = [UUID(item) for item in repr(default_uuid_set).split(", ")]
    assert set(items) == set(test_values)

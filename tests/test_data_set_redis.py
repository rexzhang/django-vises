from uuid import uuid4

from django_vises.db.data_set_redis import DataSetInt, DataSetStr, DataSetUUID


def test_data_set_str():
    dsi = DataSetStr(url="redis://localhost:6379/0", name="test")
    str_1 = "test1"
    str_2 = "test2"

    dsi.clear()
    assert dsi.all() == []

    dsi.add(str_1)
    assert dsi.all() == [str_1]

    dsi.add(str_2)
    assert set(dsi.all()) == {str_1, str_2}

    dsi.remove(str_1)
    assert dsi.all() == [str_2]

    dsi.clear()


def test_data_set_int():
    dsi = DataSetInt(url="redis://localhost:6379/0", name="test")

    dsi.clear()
    assert dsi.all() == []

    dsi.add(1)
    assert dsi.all() == [1]

    dsi.add(2)
    assert set(dsi.all()) == {1, 2}

    dsi.remove(1)
    assert dsi.all() == [2]

    dsi.clear()


def test_data_set_uuid():
    dsi = DataSetUUID(url="redis://localhost:6379/0", name="test")
    uuid_1 = uuid4()
    uuid_2 = uuid4()

    dsi.clear()
    assert dsi.all() == []

    dsi.add(uuid_1)
    assert dsi.all() == [uuid_1]

    dsi.add(uuid_2)
    assert set(dsi.all()) == {uuid_1, uuid_2}

    dsi.remove(uuid_1)
    assert dsi.all() == [uuid_2]

    dsi.clear()

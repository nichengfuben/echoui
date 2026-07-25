"""File validator and data module tests."""

from echoui.data import DataTable, VirtualList
from echoui.forms import Form, field, file_size, file_type, max_files
from echoui.i18n import load_catalog, load_plural, plural, set_locale, t


def test_file_size_validator():
    f = Form().add(field("img", file_size(1024)))
    assert not f.validate({"img": {"size": 2048}})
    assert f.validate({"img": {"size": 512}})


def test_file_type_validator():
    f = Form().add(field("img", file_type("image/")))
    assert not f.validate({"img": {"type": "text/plain"}})
    assert f.validate({"img": {"type": "image/png"}})


def test_max_files_validator():
    f = Form().add(field("files", max_files(2)))
    assert not f.validate({"files": [1, 2, 3]})
    assert f.validate({"files": [1]})


def test_virtual_list_window():
    vl = VirtualList(items=list(range(100)), item_height=20, viewport_height=200)
    vl.scroll_to(10)
    visible = vl.visible_items()
    assert visible[0][0] >= 10
    assert len(visible) <= vl.visible_count


def test_data_table_sort():
    dt = DataTable(columns=[{"key": "n"}], rows=[{"n": 3}, {"n": 1}])
    dt.sort_by("n")
    assert dt.rows[0]["n"] == 1


def test_i18n_plural():
    set_locale("en")
    load_catalog("en", {"hello": "Hello {name}"})
    load_plural("en", "items", {"one": "1 item", "other": "{n} items"})
    assert t("hello", name="World") == "Hello World"
    assert plural("items", 1, one="1 item", other="{n} items") == "1 item"
    assert plural("items", 5, one="1 item", other="{n} items") == "5 items"

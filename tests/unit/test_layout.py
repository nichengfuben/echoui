"""Layout helper tests."""

from echoui.layout import center, col, grid, row, stack
from echoui.sprite import IRNode


def test_row_direction():
    node = row(col(), col())
    assert node.props["direction"] == "row"
    assert len(node.children) == 2


def test_col_direction():
    node = col(row(), row())
    assert node.props["direction"] == "col"


def test_grid_cols():
    node = grid(cols=3)
    assert node.props["cols"] == 3
    assert node.props["display"] == "grid"


def test_stack_display():
    node = stack()
    assert node.props["display"] == "stack"


def test_center_wraps_child():
    inner = IRNode("text", props={"text": "hi"})
    node = center(inner)
    assert node.props["align"] == "center"
    assert len(node.children) == 1

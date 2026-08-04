from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from echoui.core.exceptions import ConfigError
from echoui.utils.path_utils import (
    ensure_dir,
    get_project_root,
    read_text,
    write_text,
)


class TestGetProjectRoot:
    """get_project_root 测试。"""

    def test_returns_path(self) -> None:
        """应返回 Path 对象。"""
        root = get_project_root()
        assert isinstance(root, Path)

    def test_name_is_echoui(self) -> None:
        """目录名应为 echoui。"""
        root = get_project_root()
        assert root.name == "echoui"


class TestEnsureDir:
    """ensure_dir 测试。"""

    def test_creates_nested_dirs(self) -> None:
        """应创建嵌套目录。"""
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "a" / "b" / "c"
            result = ensure_dir(target)
            assert result.exists()
            assert result.is_dir()

    def test_existing_dir_no_error(self) -> None:
        """已有目录不应报错。"""
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir)
            result = ensure_dir(target)
            assert result.exists()

    def test_returns_path(self) -> None:
        """应返回传入的路径。"""
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "sub"
            result = ensure_dir(target)
            assert result == target


class TestReadWriteText:
    """read_text / write_text 测试。"""

    def test_write_and_read(self) -> None:
        """写入后读取内容应一致。"""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.txt"
            write_text(path, "hello world")
            content = read_text(path)
            assert content == "hello world"

    def test_read_nonexistent_raises(self) -> None:
        """读取不存在的文件应抛出 ConfigError。"""
        with pytest.raises(ConfigError, match="文件不存在"):
            read_text(Path("/nonexistent/file.txt"))

    def test_write_creates_parent_dir(self) -> None:
        """写入时应自动创建父目录。"""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "a" / "b" / "c.txt"
            write_text(path, "data")
            assert path.exists()

    def test_chinese_content(self) -> None:
        """中文内容应正确读写。"""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "cn.txt"
            write_text(path, "你好世界")
            content = read_text(path)
            assert content == "你好世界"

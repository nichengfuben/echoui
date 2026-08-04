from __future__ import annotations

from pathlib import Path

from echoui.core.exceptions import ConfigError


def get_project_root() -> Path:
    """获取项目根目录路径。

    Returns:
        Path: 项目根目录的 Path 对象。

    Examples:
        >>> path = get_project_root()
        >>> path.name
        'echoui'
    """
    return Path(__file__).resolve().parent.parent.parent.parent


def get_temp_dir() -> Path:
    """获取临时目录路径。

    Returns:
        Path: 临时目录路径。
    """
    return get_project_root() / "tmp"


def ensure_dir(path: Path) -> Path:
    """确保目录存在，不存在则创建。

    Args:
        path: 目标目录路径。

    Returns:
        Path: 传入的路径对象。

    Examples:
        >>> import tempfile
        >>> p = Path(tempfile.mkdtemp()) / "sub"
        >>> result = ensure_dir(p)
        >>> result.exists()
        True
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_text(path: Path) -> str:
    """读取文本文件内容（UTF-8）。

    Args:
        path: 文件路径。

    Returns:
        str: 文件内容。

    Raises:
        ConfigError: 当文件不存在时抛出。

    Examples:
        >>> import tempfile
        >>> p = Path(tempfile.mkdtemp()) / "test.txt"
        >>> _ = p.write_text("hello", encoding="utf-8")
        >>> read_text(p)
        'hello'
    """
    if not path.exists():
        raise ConfigError(f"文件不存在: {path}")
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()


def write_text(path: Path, content: str) -> None:
    """写入文本文件（UTF-8，LF 换行）。

    Args:
        path: 文件路径。
        content: 文件内容。

    Examples:
        >>> import tempfile
        >>> p = Path(tempfile.mkdtemp()) / "test.txt"
        >>> write_text(p, "hello")
        >>> p.read_text(encoding="utf-8")
        'hello'
    """
    ensure_dir(path.parent)
    with open(path, mode="w", encoding="utf-8", newline="\n") as f:
        f.write(content)

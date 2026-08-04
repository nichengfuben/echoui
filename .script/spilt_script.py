#!/usr/bin/env python
"""
分割脚本：将 upload.txt 按字符数限制分割为多个 part 并输出。

每个 part 的字符数（不含包装头尾）不超过 119913，
直接按字符数截断，不考虑行边界。
"""

import sys
from pathlib import Path
from typing import List


def read_file_content(file_path: Path) -> str:
    """读取文件的完整内容。

    Args:
        file_path: 文件路径。

    Returns:
        文件的完整字符串内容。

    Raises:
        FileNotFoundError: 文件不存在时抛出。
    """
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def split_by_chars(content: str, max_chars: int = 119913) -> List[str]:
    """将字符串按字符数限制分割为多个 part。

    直接按字符数截断，不考虑行边界。

    Args:
        content: 要分割的字符串内容。
        max_chars: 每个 part 的最大字符数限制。

    Returns:
        分割后的 part 内容列表。
    """
    if not content:
        return []

    parts: List[str] = []
    content_length: int = len(content)
    
    for i in range(0, content_length, max_chars):
        part: str = content[i:i + max_chars]
        parts.append(part)
    
    return parts


def format_and_print_parts(parts: List[str]) -> None:
    """格式化并打印所有 part。

    非最后一个 part 使用普通结束标记，
    最后一个 part 使用特殊结束标记提示开始回复。

    Args:
        parts: 分割后的 part 内容列表。
    """
    total: int = len(parts)

    for index, content in enumerate(parts, start=1):
        is_last: bool = index == total

        # 移除内容末尾多余的换行，保持输出整洁
        content_stripped: str = content.rstrip("\n")

        header: str = f"--- PART {index}/{total} START ---"

        if is_last:
            footer: str = f"---PART {index}/{total} END AND START REPLY NOW---"
        else:
            footer = (
                f"--- PART {index}/{total} END AND "
                f"YOU SHOULD READ QUIET AND DONT REPLY------"
            )

        print(f"{header}\n{content_stripped}\n{footer}")

        # 在 part 之间添加空行分隔，最后一个 part 后不加
        if not is_last:
            print()


def main() -> None:
    """主函数：读取 upload.txt 并按字符数分割输出。"""
    script_dir: Path = Path(__file__).resolve().parent
    file_path: Path = script_dir / "upload.txt"

    try:
        content: str = read_file_content(file_path)
    except FileNotFoundError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)

    if not content:
        print("文件为空，无内容可分割。", file=sys.stderr)
        sys.exit(0)

    parts: List[str] = split_by_chars(content, max_chars=119913)
    format_and_print_parts(parts)

    # 输出统计信息到 stderr，不干扰 stdout 的正式输出
    total_chars: int = sum(len(p) for p in parts)
    print(
        f"\n分割完成: 共 {len(parts)} 个 part, 总字符数 {total_chars}",
        file=sys.stderr,
    )
    print('由于受到限制，你刚刚生成的内容被截断了 --- 请你稍后回复，我会将你之前回复的内容发给你，然后你再根据之前你生成的内容继续对接，从下一行开始生成')
    print('这是你之前生成回复的第 1/2 段 --- 请你稍后回复，我会将你之前回复的内容发给你，然后你再根据之前你生成的内容继续对接，从下一行开始生成')
    print('根据之前你生成的内容继续对接，从下一行开始生成')


if __name__ == "__main__":
    main()

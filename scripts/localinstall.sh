#!/usr/bin/env bash
# EchoUI 本地开发环境安装脚本 (Linux/macOS)
# 用法: ./scripts/localinstall.sh

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "=== EchoUI 本地安装 ==="
echo "项目目录: $PROJECT_ROOT"

if [ ! -d "venv" ]; then
    echo "创建虚拟环境 venv ..."
    python3 -m venv venv
fi

# shellcheck disable=SC1091
source venv/bin/activate

echo "升级 pip ..."
python -m pip install --upgrade pip wheel build twine

echo "安装项目（可编辑模式 + 开发依赖）..."
pip install -e ".[dev]"

echo "验证导入 ..."
python -c "import echoui; print(f'echoui {echoui.__version__} OK')"

echo "运行测试 ..."
python -m pytest tests/ -q --tb=short

echo ""
echo "=== 本地安装完成 ==="
echo "激活环境: source venv/bin/activate"
echo "运行测试: pytest tests/ -v"
echo "构建包:   python -m build"

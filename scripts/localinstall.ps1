# EchoUI 本地开发环境安装脚本 (Windows PowerShell)
# 用法: .\scripts\localinstall.ps1

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $ProjectRoot

Write-Host "=== EchoUI 本地安装 ===" -ForegroundColor Cyan
Write-Host "项目目录: $ProjectRoot"

# 创建虚拟环境（如不存在）
if (-not (Test-Path "venv")) {
    Write-Host "创建虚拟环境 venv ..."
    python -m venv venv
}

# 激活虚拟环境
& ".\venv\Scripts\Activate.ps1"

Write-Host "升级 pip ..."
python -m pip install --upgrade pip wheel build twine

Write-Host "安装项目（可编辑模式 + 开发依赖）..."
pip install -e ".[dev]"

Write-Host "验证导入 ..."
python -c "import echoui; print(f'echoui {echoui.__version__} OK')"

Write-Host "运行测试 ..."
python -m pytest tests/ -q --tb=short

Write-Host ""
Write-Host "=== 本地安装完成 ===" -ForegroundColor Green
Write-Host "激活环境: .\venv\Scripts\Activate.ps1"
Write-Host "运行测试: pytest tests/ -v"
Write-Host "构建包:   python -m build"

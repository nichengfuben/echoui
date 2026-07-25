# 静态跑酷 — 无需 dev server / 7999，适合代理环境
$ErrorActionPreference = "Stop"
Set-Location "E:\Project\EchoUI"
if (-not (Test-Path "dist\static\runner\index.html")) {
    python -m echoui build examples/06_runner/main.py --target static --out dist/static/runner
}
Write-Host "Static preview: http://127.0.0.1:8080/"
python -m echoui preview --dir dist/static/runner --port 8080

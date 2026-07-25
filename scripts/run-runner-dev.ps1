# 跑酷 dev — 绕过本地代理，避免 localhost:7999 被转到 59131
$ErrorActionPreference = "Stop"
$Root = "E:\Project\EchoUI\examples\06_runner"

# 本地地址不走代理（Clash/V2Ray 等常见端口 59131/52916）
$env:NO_PROXY = "localhost,127.0.0.1,::1"
$env:no_proxy = $env:NO_PROXY
Remove-Item Env:HTTP_PROXY -ErrorAction SilentlyContinue
Remove-Item Env:HTTPS_PROXY -ErrorAction SilentlyContinue
Remove-Item Env:ALL_PROXY -ErrorAction SilentlyContinue

Set-Location $Root
Write-Host "Starting EchoUI dev on http://127.0.0.1:7999 (NO_PROXY set)"
Write-Host "Open in browser: http://127.0.0.1:7999/"
python -m echoui dev main.py --host 0.0.0.0 --port 7999

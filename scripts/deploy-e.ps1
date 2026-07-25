# EchoUI E: drive full deploy — build all runner targets
$ErrorActionPreference = "Stop"
$Root = "E:\Project\EchoUI"
$Entry = "$Root\examples\06_runner\main.py"
Set-Location $Root

Write-Host "==> install deps"
python -m pip install -e ".[web,desktop,dev]" -q

Write-Host "==> quality gate"
python -m pytest tests -q
python -m ruff check echoui tests
python achecker.py

$targets = @(
    @{ t = "web"; out = "$Root\dist\web\runner" },
    @{ t = "static"; out = "$Root\dist\static\runner" },
    @{ t = "desktop"; out = "$Root\dist\desktop\runner" },
    @{ t = "android"; out = "$Root\dist\android\runner" },
    @{ t = "ios"; out = "$Root\dist\ios\runner" }
)
foreach ($x in $targets) {
    Write-Host "==> build $($x.t)"
    python -m echoui build $Entry --target $x.t --out $x.out
}

Write-Host "==> package desktop exe"
python -m echoui build $Entry --target desktop --out "$Root\dist\desktop\runner" --package

Write-Host "==> build android gradle project + apk"
python -c "from echoui.cli import _load_app; from echoui.targets.android_gradle import build_android_gradle; build_android_gradle(_load_app(r'$Entry'), out_dir=r'$Root\dist\android\runner', sdk_root=r'E:\Android\Sdk')"
$gradleProps = @"
org.gradle.jvmargs=-Xmx2048m
android.useAndroidX=true
android.nonTransitiveRClass=true
systemProp.http.proxyHost=127.0.0.1
systemProp.http.proxyPort=52916
systemProp.https.proxyHost=127.0.0.1
systemProp.https.proxyPort=52916
"@
Set-Content -Path "$Root\dist\android\runner\gradle-project\gradle.properties" -Value $gradleProps -Encoding UTF8
Set-Content -Path "$Root\dist\android\runner\gradle-project\local.properties" -Value "sdk.dir=E:/Android/Sdk" -Encoding UTF8
$env:JAVA_HOME = "C:\Program Files\Microsoft\jdk-21.0.11.10-hotspot"
$env:ANDROID_HOME = "E:\Android\Sdk"
Set-Location "$Root\dist\android\runner\gradle-project"
& "E:\Gradle\gradle-8.7\bin\gradle.bat" assembleDebug --no-daemon
Copy-Item "$Root\dist\android\runner\gradle-project\app\build\outputs\apk\debug\app-debug.apk" "$Root\dist\android\runner\echoui-runner.apk" -Force

Write-Host "==> done"
Write-Host "Web:     $Root\dist\web\runner\index.html"
Write-Host "Static:  $Root\dist\static\runner\index.html"
Write-Host "Desktop: $Root\dist\desktop\runner\bundle\echoui-app.exe"
Write-Host "Android: $Root\dist\android\runner\echoui-runner.apk"
Write-Host "iOS:     $Root\dist\ios\runner\web\index.html"

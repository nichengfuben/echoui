# EchoUI — E 盘部署

根目录：`E:\Project\EchoUI`

## 工具链（E 盘已安装）

| 工具 | 路径 |
|------|------|
| EchoUI 源码 | `E:\Project\EchoUI` |
| OpenJDK 21 | `C:\Program Files\Microsoft\jdk-21.0.11.10-hotspot` |
| Android SDK | `E:\Android\Sdk` |
| Gradle 8.7 | `E:\Gradle\gradle-8.7` |
| PySide6 + PyInstaller | pip 全局 |

代理（Gradle/Maven 下载）：`127.0.0.1:52916`

## 一键构建

```powershell
E:\Project\EchoUI\scripts\deploy-e.ps1
```

## 产物路径

| 目标 | 路径 | 运行方式 |
|------|------|----------|
| Web | `dist\web\runner\index.html` | `python -m echoui dev examples/06_runner/main.py` |
| Static | `dist\static\runner\index.html` | 浏览器直接打开（本地 frame，无需服务器） |
| Desktop IR | `dist\desktop\runner\lowered.json` | `python dist\desktop\runner\main.py` |
| Desktop EXE | `dist\desktop\runner\bundle\echoui-app.exe` | 双击运行 |
| Android APK | `dist\android\runner\echoui-runner.apk` | 安装到手机/模拟器 |
| Android 工程 | `dist\android\runner\gradle-project\` | Gradle 源码工程 |
| iOS 壳 | `dist\ios\runner\web\` | macOS CI / Xcode WKWebView |

## 跑酷 Dev

```powershell
cd E:\Project\EchoUI\examples\06_runner
python -m echoui dev main.py --port 7999
```

浏览器：`http://127.0.0.1:7999` — Space 跳跃，R 重置。

## Static 预览

```powershell
cd E:\Project\EchoUI
python -m echoui preview --dir dist/static/runner --port 8080
```

## Android APK（需额外安装）

Windows 上需 Android Studio + SDK：

1. 安装 [Android Studio](https://developer.android.com/studio) 到 `E:\Program Files\Android\`
2. 设置 `ANDROID_HOME=E:\Android\Sdk`
3. 用 `dist\android\runner\` 模板创建 Gradle 工程并 `assembleDebug`

iOS `.ipa` 仅 macOS CI（见 `.github/workflows/ios-build.yml`）。

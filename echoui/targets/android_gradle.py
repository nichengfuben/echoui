"""Generate a Gradle Android project for WebView shell APK builds."""

from __future__ import annotations

import shutil
import textwrap
from pathlib import Path
from typing import Any


def build_android_gradle(app: Any, *, out_dir: str, sdk_root: str = "E:\\Android\\Sdk") -> str:
    from echoui.targets.mobile_android import build_android

    base = Path(build_android(app, out_dir=out_dir))
    project = base / "gradle-project"
    if project.exists():
        shutil.rmtree(project)
    project.mkdir(parents=True)

    assets = project / "app" / "src" / "main" / "assets" / "web"
    assets.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(base / "assets" / "web", assets, dirs_exist_ok=True)

    java_dir = project / "app" / "src" / "main" / "java" / "com" / "echoui" / "app"
    java_dir.mkdir(parents=True, exist_ok=True)
    (java_dir / "MainActivity.java").write_text(_MAIN_ACTIVITY, encoding="utf-8")
    (project / "app" / "src" / "main" / "AndroidManifest.xml").write_text(_MANIFEST, encoding="utf-8")
    (project / "settings.gradle").write_text(_SETTINGS_GRADLE, encoding="utf-8")
    (project / "build.gradle").write_text(_ROOT_GRADLE, encoding="utf-8")
    (project / "gradle.properties").write_text(
        textwrap.dedent(
            f"""
            org.gradle.jvmargs=-Xmx2048m
            android.useAndroidX=true
            android.nonTransitiveRClass=true
            android.sdk.dir={sdk_root.replace(chr(92), '/')}
            """
        ).strip()
        + "\n",
        encoding="utf-8",
    )
    (project / "app" / "build.gradle").write_text(_APP_GRADLE, encoding="utf-8")
    (project / "local.properties").write_text(f"sdk.dir={sdk_root}\n", encoding="utf-8")
    _write_wrapper(project)
    return str(project.resolve())


def _write_wrapper(project: Path) -> None:
    wrapper = project / "gradle" / "wrapper"
    wrapper.mkdir(parents=True, exist_ok=True)
    (wrapper / "gradle-wrapper.properties").write_text(
        "distributionBase=GRADLE_USER_HOME\n"
        "distributionPath=wrapper/dists\n"
        "distributionUrl=https\\://services.gradle.org/distributions/gradle-8.7-bin.zip\n"
        "zipStoreBase=GRADLE_USER_HOME\n"
        "zipStorePath=wrapper/dists\n",
        encoding="utf-8",
    )
    bat = project / "gradlew.bat"
    bat.write_text(_GRADLEW_BAT, encoding="utf-8")


_MAIN_ACTIVITY = """package com.echoui.app;

import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        WebView webView = new WebView(this);
        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        webView.setWebViewClient(new WebViewClient());
        webView.loadUrl("file:///android_asset/web/index.html");
        setContentView(webView);
    }
}
"""

_MANIFEST = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application
        android:allowBackup="true"
        android:label="EchoUI Runner"
        android:supportsRtl="true"
        android:theme="@style/Theme.AppCompat.Light.NoActionBar">
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""

_ROOT_GRADLE = """plugins {
    id 'com.android.application' version '8.3.2' apply false
}
"""

_SETTINGS_GRADLE = """pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = 'EchoUIRunner'
include ':app'
"""

_APP_GRADLE = """plugins {
    id 'com.android.application'
}

android {
    namespace 'com.echoui.app'
    compileSdk 34

    defaultConfig {
        applicationId "com.echoui.app"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }

    buildTypes {
        release {
            minifyEnabled false
        }
    }
}

dependencies {
    implementation 'androidx.appcompat:appcompat:1.6.1'
}
"""

_GRADLEW_BAT = r"""@rem Gradle startup script for Windows
@if "%DEBUG%"=="" @echo off

set DIRNAME=%~dp0
set APP_BASE_NAME=%~n0
set APP_HOME=%DIRNAME%

set JAVA_EXE=java.exe
if defined JAVA_HOME set JAVA_EXE=%JAVA_HOME%\bin\java.exe

set CLASSPATH=%APP_HOME%\gradle\wrapper\gradle-wrapper.jar

"%JAVA_EXE%" -classpath "%CLASSPATH%" org.gradle.wrapper.GradleWrapperMain %*

"""

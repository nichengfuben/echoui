# Getting Started

## 安装（类似 `npm install -g`）

```bash
pip install echoui[web]
echoui version
```

PyPI 暂无 1.0.0 时：

```bash
pip install "echoui[web] @ git+https://github.com/nichengfuben/echoui.git"
```

本地开发 EchoUI 本身：

```bash
git clone https://github.com/nichengfuben/echoui.git
cd echoui
pip install -e ".[web,dev]"
```

## 新建项目（类似 `npm create`）

```bash
echoui new my-app
cd my-app
pip install -e .
echoui build --target web
echoui dev --port 8765
```

打开 http://127.0.0.1:8765

## 已有 main.py

```bash
echoui build --target web
echoui dev --port 8765
echoui preview --dir dist/web --port 8765
```

## Counter 源码

见 `examples/02_counter/main.py` 或 `echoui new` 生成的 `main.py`。

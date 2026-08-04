# EchoUI

Pure Python terminal UI framework using ASCII/ANSI characters to render interfaces in the terminal. Features a chain-driven component API.

## Features

- **Pure terminal UI**: Renders interfaces using ASCII/ANSI characters
- **Chain-driven API**: All components support method chaining
- **Theme system**: 9 built-in themes with color customization
- **Multiple adapters**: Terminal, Web (aiohttp/Flask/FastAPI), Desktop (Tkinter/PyQt)
- **Database ORM**: In-memory model layer with async session support
- **Cross-version**: Python 3.8-3.14 compatible
- **Cross-platform**: Windows, macOS, Linux support

## Installation

```bash
pip install echoui
```

## Quick Start

```python
from echoui import EchoUI

ui = EchoUI(normal_mode=True)
ui.block("EchoUI").rule("=").success("Ready").print()
```

## Components

- `ConsoleUI` - Terminal console controller
- `BoxBuilder` - Content container with titles
- `TableBuilder` - Formatted table rendering
- `ProgressBar` - Progress bar visualization
- `Spinner` - Loading animation
- `Notification` - Success/warning/error/info notifications
- `BlockArt` - Block character art rendering
- `KeyValueList` - Key-value pair display
- `TreeView` - Hierarchical data display

## Adapters

| Adapter | Backend | Use Case |
|---------|---------|----------|
| TerminalAdapter | Console | Terminal UI |
| AiohttpAdapter | aiohttp | Web, WebSocket |
| FlaskAdapter | Flask | Lightweight web |
| FastAPIAdapter | FastAPI | API with docs |
| TkinterAdapter | Tkinter | Desktop (stdlib) |
| PyQtAdapter | PyQt5/6 | Professional desktop |

## Documentation

- [Architecture](docs/architecture.md)
- [Components](docs/components.md)

## Development

### Local install

```powershell
# Windows
.\scripts\localinstall.ps1
```

```bash
# Linux/macOS
chmod +x scripts/localinstall.sh
./scripts/localinstall.sh
```

Or manually:

```bash
python -m venv venv
source venv/bin/activate   # Windows: .\venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest tests/ -v
```

### Quality checks

```bash
black src/ tests/
isort src/ tests/
mypy src/ --strict
pytest tests/ --cov=src/echoui --cov-fail-under=90
```

### Build & publish

```bash
python -m build
twine check dist/*
twine upload dist/*
```

## License

MIT License

"""CLI start/run npm-parity tests."""

from __future__ import annotations

from echoui.cli import _dispatch_script, _echoui_scripts, cmd_run, main


def test_echoui_scripts_from_pyproject(tmp_path):
    (tmp_path / "pyproject.toml").write_text(
        '[tool.echoui.scripts]\nstart = "version"\n',
        encoding="utf-8",
    )
    assert _echoui_scripts(tmp_path)["start"] == "version"


def test_start_without_pyproject_calls_dev(monkeypatch, tmp_path):
    entry = tmp_path / "main.py"
    entry.write_text(
        "from echoui import App, Screen, col, text\n"
        "class H(Screen):\n"
        "    def build(self):\n"
        "        return col(text('hi'))\n"
        "app = App(screens=[H], initial='H')\n",
        encoding="utf-8",
    )
    calls: list[tuple] = []

    def fake_dev(e: str, *, host: str, port: int, target: str) -> int:
        calls.append((e, host, port, target))
        return 0

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("echoui.cli.cmd_dev", fake_dev)
    assert main(["start", str(entry), "--port", "8765"]) == 0
    assert calls == [(str(entry), "0.0.0.0", 8765, "web")]


def test_run_script(tmp_path, monkeypatch):
    (tmp_path / "pyproject.toml").write_text(
        '[tool.echoui.scripts]\nping = "version"\n',
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    assert cmd_run("ping", []) == 0
    assert cmd_run("missing", []) == 1


def test_dispatch_script_strips_echoui_prefix():
    assert _dispatch_script("version") == 0


def test_cli_start_in_help(capsys):
    import pytest

    with pytest.raises(SystemExit) as exc:
        main(["-h"])
    assert exc.value.code == 0
    out = capsys.readouterr().out
    assert "start" in out
    assert "run" in out

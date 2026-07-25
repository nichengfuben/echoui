"""CI workflow presence tests."""

from __future__ import annotations

from pathlib import Path


def test_publish_workflow_exists():
    repo = Path(__file__).resolve().parents[2]
    wf = repo / ".github" / "workflows" / "publish.yml"
    text = wf.read_text(encoding="utf-8")
    assert "PYPI_API_TOKEN" in text
    assert "echoui" in text
    assert 'tags:' in text

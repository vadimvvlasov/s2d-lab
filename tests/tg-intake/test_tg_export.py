"""Tests for scripts/tg_export_to_source.py.

Run: uv run --with pytest --with beautifulsoup4 pytest tests/tg-intake -q
"""

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).parent / "fixture"
EXPORT = FIXTURES / "ChatExport_2026-01-02"

spec = importlib.util.spec_from_file_location("tg", ROOT / "scripts" / "tg_export_to_source.py")
tg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tg)


def run(tmp_path, *args):
    tg.main([*args, "--run-id", "r1", "--out-root", str(tmp_path)])
    return (tmp_path / "r1" / "source.md").read_text(encoding="utf-8")


def test_explicit_export_dir(tmp_path):
    src = run(tmp_path, str(EXPORT))
    lines = [ln for ln in src.splitlines() if ln.startswith("[#")]
    assert len(lines) == 5
    assert "message_count: 5" in src
    assert "image_count: 1" in src
    assert lines[0] == "[#100 2026-01-01 10:00] Alice: Is BTC overbought?"
    assert "link (https://example.com/x)" in src
    assert "👍" not in src  # reactions dropped
    assert "1 January 2026" not in src  # service message dropped


def test_joined_reply_forward_media(tmp_path):
    src = run(tmp_path, str(EXPORT))
    assert "[#101 2026-01-01 10:01] Alice: chart\n    ![photo #101](images/photo_1@01-01-2026_10-01-00.jpg)" in src
    assert "[#102 2026-01-01 10:05] Bob ↪ #100: No." in src
    assert "[#103 2026-01-02 09:00] Bob (fwd from News Channel): Rates unchanged." in src
    assert "[#104 2026-01-02 09:01] Bob: [Video file (not included in export)]" in src


def test_images_copied_without_thumbs(tmp_path):
    run(tmp_path, str(EXPORT))
    assert sorted(p.name for p in (tmp_path / "r1" / "images").iterdir()) == ["photo_1@01-01-2026_10-01-00.jpg"]


def test_autodiscovery_by_chat_title(tmp_path):
    src = run(tmp_path, "--exports-root", str(FIXTURES))
    assert f'export_dir: "{EXPORT}"' in src


def test_unknown_chat_fails(tmp_path):
    with pytest.raises(SystemExit) as e:
        run(tmp_path, "--exports-root", str(FIXTURES), "--chat", "nope")
    assert e.value.code == 1

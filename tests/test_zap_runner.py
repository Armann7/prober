from __future__ import annotations

import json

import pytest
from pathlib import Path

import zap_runner


@pytest.mark.asyncio
async def test_run_zap_full_scan_returns_parsed_report(monkeypatch, tmp_path: Path) -> None:
    result = await zap_runner.zap_scan("https://google.com", scan_type='base')
    assert result['@programName'] == 'ZAP'
    assert 'insights' in result


if __name__ == "__main__":
    pytest.main([__file__])

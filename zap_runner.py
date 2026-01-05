from __future__ import annotations

import asyncio
from collections.abc import Collection, Mapping
from functools import cache
import json
import logging
from re import U
import tempfile
from pathlib import Path
from typing import Any
from typing import Literal


MessageLevel = Literal['info', 'low', 'medium', 'high']
ZapScanType = Literal['base', 'full', 'api']
_ZAP_SCRIPT = {
    'full': 'zap-full-scan.py',
    'base': 'zap-baseline.py',
    'api': 'zap-api-scan.py',
    }

class ZapScanResult:

    def __init__(self, url: str, raw: Mapping[str, Any]):
        self._scanner = 'zap'
        self._url = url
        self._raw = raw

    def write_report(self, folder: Path):
        file: Path = folder / self._filename()
        file.write_text(json.dumps(self._raw, indent=4))

    @cache
    def messages(self, levels: Collection[MessageLevel]) -> Collection[Mapping[str, Any]]:
        return [i for i in self._raw['insights'] if i['level'].lower() in levels]

    def __repr__(self) -> str:
        return f'{self._scanner} - {self._url}'

    def _filename(self) -> Path:
        unwanted_symbols = ':/\\*?+'
        translation_table = str.maketrans(unwanted_symbols, '_' * len(unwanted_symbols))
        sanitized_url = self._url.rstrip('/').translate(translation_table)
        return Path(f'{self._scanner}-{sanitized_url}.json')
    


async def zap_scan(target_url: str, scan_type: ZapScanType) -> ZapScanResult:
    if not target_url:
        raise ValueError("target_url must be a non-empty string")
    docker_image = "ghcr.io/zaproxy/zaproxy:stable"
    with tempfile.TemporaryDirectory() as workdir_str:
        workdir = Path(workdir_str)
        report_name = "zap-report.json"
        report_path = workdir / report_name
        command = [
            "docker", "run", "--rm", "-v", f"{workdir}:/zap/wrk", docker_image,
            _ZAP_SCRIPT[scan_type],
            "-t", target_url,
            "-J", report_name,
            ]
        _logger.info("Run %s", command)
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        [stdout, stderr] = await process.communicate()
        if process.returncode != 0:
            output = stderr.decode() or stdout.decode()
            # raise RuntimeError(f"ZAP scan failed (exit code {process.returncode}): {output.strip()}")
        if not report_path.exists():
            raise RuntimeError("ZAP JSON report was not produced")
        raw_data = json.loads(report_path.read_text())
        return ZapScanResult(target_url, raw_data)


_logger = logging.getLogger(__name__)

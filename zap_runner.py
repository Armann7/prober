from __future__ import annotations

import asyncio
import json
import logging
import tempfile
from pathlib import Path
from typing import Any, Literal


ZapScanType = Literal['base', 'full', 'api']
_ZAP_SCRIPT = {
    'full': 'zap-full-scan.py',
    'base': 'zap-baseline.py',
    'api': 'zap-api-scan.py',
    }


async def zap_scan(target_url: str, scan_type: ZapScanType) -> dict[str, Any]:
    if not target_url:
        raise ValueError("target_url must be a non-empty string")
    docker_image = "ghcr.io/zaproxy/zaproxy:stable"
    zap_script = 'zap-full-scan.py' if scan_type == 'full' else 'zap-full-scan.py'
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
        return json.loads(report_path.read_text())


_logger = logging.getLogger(__name__)

import asyncio
import json
import logging
import subprocess  # nosec B404
import tempfile
import time
from collections.abc import Mapping
from functools import cache
from pathlib import Path
from signal import SIGINT
from typing import Any
from typing import Final
from typing import Literal

from base_runner import AlertLevel
from base_runner import ScanError
from base_runner import ScanResult
from base_runner import make_report_filename

TIME_LIMIT = 300
ZapScanType = Literal['base', 'full', 'api']
_ZAP_DOCKER_IMAGE = 'ghcr.io/zaproxy/zaproxy:stable'
_ZAP_SCRIPT = {
    'full': 'zap-full-scan.py',
    'base': 'zap-baseline.py',
    'api': 'zap-api-scan.py',
    }


class ZapScanResult(ScanResult):

    _LEVELS_MAPPING: Final = {
        'info': '0',
        'low': '1',
        'medium': '2',
        'high': '3',
        }

    def __init__(self, url: str, raw: Mapping[str, Any], *levels: AlertLevel):
        super().__init__('zap', url, raw, *levels)
        if levels:
            zap_levels = {
                code for name, code in self._LEVELS_MAPPING.items() if name in levels}
        else:
            zap_levels = set(self._LEVELS_MAPPING.values())
        self._alerts = []
        for site in self._raw['site']:
            self._alerts.extend(
                [alert for alert in site['alerts'] if alert['riskcode'] in zap_levels])
            
    def __repr__(self) -> str:
        return (
            f"{self._scanner}: {self._url}, levels {self._levels}, {len(self._alerts)} alert(s)")
        
    def write_report(self, folder: Path):
        file: Path = folder / make_report_filename(self._scanner, self._url)
        if self._alerts:
            file.write_text(json.dumps(self._alerts, indent=4))


async def zap_scan(url: str, scan_type: ZapScanType) -> ScanResult | ScanError:
    if not url:
        raise ValueError("target_url must be a non-empty string")
    _pull_docker_image(_ZAP_DOCKER_IMAGE)
    with tempfile.TemporaryDirectory() as workdir_str:
        workdir = Path(workdir_str)
        report_name = 'zap-report.json'
        report_path = workdir / report_name
        zap_command_line = [
            _ZAP_SCRIPT[scan_type], '-m', str(TIME_LIMIT // 60), '-t', url, '-J', report_name]
        command = [
            '/usr/bin/docker',
            'run',
            '--rm',
            '--volume', f'{workdir}:/zap/wrk',
            '--memory=2g',
            '--cpus=1',
            _ZAP_DOCKER_IMAGE,
            *zap_command_line,
            ]
        _logger.info("Start scanning %r", url)
        _logger.debug("Run %s", command)
        started_at = time.monotonic()
        process = await asyncio.create_subprocess_exec(
            *command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        timeout = TIME_LIMIT + 60
        try:
            [stdout, stderr] = await asyncio.wait_for(process.communicate(), timeout)
        except TimeoutError:
            process.send_signal(SIGINT)
            _logger.warning(
                "Scanning %r hadn't finished after %d sec and it was cancelled", url, timeout)
            [stdout, stderr] = await process.communicate()
        spend_time = time.monotonic() - started_at
        spend_min = spend_time // 60
        spend_sec = spend_time % 60
        _logger.info("Finish scanning %r. It took %d min %d sec", url, spend_min, spend_sec)
        if not report_path.exists():
            stderr_str = 'stderr: None' if stderr is None else f"stderr:\n{stderr.decode('utf-8')}"
            stdout_str = 'stdout: None' if stdout is None else f"stdout:\n{stdout.decode('utf-8')}"
            return ScanError(
                'zap', url, "ZAP JSON report was not produced", f"{stderr_str}\n{stdout_str}")
        raw_data = json.loads(report_path.read_text())
        return ZapScanResult(url, raw_data, 'high')


@cache
def _pull_docker_image(image: str):
    subprocess.run(['/usr/bin/docker', 'pull', image])  # nosec B603 - image name is validated / trusted


_logger = logging.getLogger(__name__)

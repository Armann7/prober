from __future__ import annotations

import asyncio
import json
import logging
import sys
from collections.abc import Sequence
from pathlib import Path

from cli import parse_args
import cli
from loader import load_targets
import zap_runner


async def main(argv: Sequence[str]) -> None:
    cli_args = parse_args(argv[1:])
    targets = load_targets(Path(cli_args.bounty_targets_data))
    results = []
    for one_target in targets:
        scan_result = await zap_runner.zap_scan(one_target.resource, scan_type='full')
        scan_result.write_report(cli_args.outdir)
        if scan_result.messages(('medium', 'high')):
            results.append(scan_result)
    if not results:
        _logger.info("There are no errors")
    else:
        for one_result in results:
            messages = '\n'.join(map(str, scan_result.messages(('medium', 'high'))))
            _logger.info('%r\n\r', one_result, messages)



_logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main(sys.argv))

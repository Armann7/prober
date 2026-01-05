import asyncio
import datetime
import logging
import random
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import cast

import cli
from loader import load_targets
from orchestrator import NoMoreResults
from orchestrator import Orchestrator


async def main(argv: Sequence[str]):
    cli_args = cli.parse_args(argv[1:])
    run_id = datetime.datetime.now(tz=datetime.timezone.utc).strftime('%Y%m%d-%H%M%S')
    configure_logging(cli_args.outdir / f'prober_{run_id}.log')
    targets = load_targets(Path(cli_args.targets_data))
    number_targets = len(targets)
    _logger.info("Start scanning %d targets", number_targets)
    reports_dir = cli_args.outdir / run_id
    reports_dir.mkdir(parents=True, exist_ok=True)
    number_results = 0
    random.shuffle(cast(list, targets))
    async with Orchestrator() as orc:
        for one_target in targets:
            await orc.scan('zap', one_target.resource)
        while True:
            try:
                result = await orc.next_result()
            except NoMoreResults:
                break
            number_results += 1
            _logger.info("%r. (%d/%d)", result.scan_result, number_results, number_targets)
            result.scan_result.write_report(reports_dir)


def configure_logging(log_file: Path):
    log_format = '%(asctime)s %(threadName)10s %(name)s %(levelname)s %(message)s'
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(log_format))
    file_handler = logging.FileHandler(log_file, encoding='utf-8', mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(log_format))
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.handlers.clear()
    root.addHandler(console)
    root.addHandler(file_handler)


_logger = logging.getLogger('prober')


if __name__ == "__main__":
    asyncio.run(main(sys.argv))

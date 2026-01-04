from __future__ import annotations

import asyncio
import sys
from collections.abc import Sequence
from pathlib import Path

from cli import parse_args
from loader import load_targets


async def main(argv: Sequence[str]) -> None:
    cli_args = parse_args(argv[1:])
    targets = load_targets(Path(cli_args.bounty_targets_data))
    _ = targets


if __name__ == "__main__":
    asyncio.run(main(sys.argv))

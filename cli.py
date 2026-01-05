from __future__ import annotations

import argparse
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CLIOptions:
    bounty_targets_data: Path
    outdir: Path


def parse_args(argv: Sequence[str]) -> CLIOptions:
    """Parse command line arguments and return structured options."""
    parser = argparse.ArgumentParser(
        description=(
            "Automated reconnaissance and vulnerability probing tool for bounty scope data."
            ),
        )
    parser.add_argument(
        "bounty_targets_data",
        type=Path,
        help="Path to a bounty-targets-data JSON file or a directory containing JSON files.",
        )
    parser.add_argument(
        "outdir",
        type=Path,
        help="Directory where scan results and reports will be written.",
        )
    args = parser.parse_args(argv)
    cli_options = CLIOptions(
        bounty_targets_data=args.bounty_targets_data,
        outdir=args.outdir)
    if not cli_options.bounty_targets_data.exists():
        raise RuntimeError(f"{args.bounty_targets_data} is not exists")
    cli_options.outdir.mkdir(exist_ok=True)
    return cli_options

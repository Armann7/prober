from __future__ import annotations

import argparse
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CLIOptions:
    targets_data: Path
    outdir: Path


def parse_args(argv: Sequence[str]) -> CLIOptions:
    """Parse command line arguments and return structured options."""
    parser = argparse.ArgumentParser(
        description=(
            "Automated reconnaissance and vulnerability probing tool for bounty scope data."
        ),
    )
    parser.add_argument(
        "--targets_data",
        dest="targets_data",
        type=Path,
        required=True,
        help="Path to a bounty-targets-data JSON file or a directory containing JSON files.",
    )
    parser.add_argument(
        "--outdir",
        type=Path,
        required=True,
        help="Directory where scan results and reports will be written.",
    )
    args = parser.parse_args(argv)
    cli_options = CLIOptions(
        targets_data=args.targets_data,
        outdir=args.outdir,
    )
    if not cli_options.targets_data.exists():
        raise RuntimeError(f"{cli_options.targets_data} does not exist")
    cli_options.outdir.mkdir(exist_ok=True)
    return cli_options

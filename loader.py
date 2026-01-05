import json
from collections.abc import Collection
from collections.abc import Iterable
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_ALLOWED_TARGET_TYPES = {
    'api',
    'website',
    }

@dataclass(frozen=True)
class Target:
    name: str
    type: str
    resource: str


def load_targets(target_path: Path) -> Collection[Target]:
    if not target_path.exists():
        raise RuntimeError(f"Path {target_path} does not exist")
    json_paths: Iterable[Path]
    if target_path.is_dir():
        json_paths = sorted(
            path for path in target_path.iterdir() if path.is_file() and path.suffix == ".json")
    else:
        json_paths = (target_path,)
    all_targets: list[Target] = []
    for path in json_paths:
        raw_data = json.loads(path.read_text())
        if not isinstance(raw_data, list):
            raise RuntimeError("Wrong JSON format. It is expected that it contains a list")
        for program_data in raw_data:
            program_targets = _load_bugcrowd_program(program_data)
            all_targets.extend(program_targets)
    return all_targets


def _load_bugcrowd_program(raw_data: Mapping[str, Any]) -> Collection[Target]:
    result: list[Target] = []
    for target_raw in raw_data['targets']['in_scope']:
        if target_raw['type'] in _ALLOWED_TARGET_TYPES:
            if target_raw['uri']:
                target = Target(target_raw['name'], target_raw['type'], target_raw['uri'])
                result.append(target)
    return result

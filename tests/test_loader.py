from __future__ import annotations

from pathlib import Path

from loader import load_targets
from loader import Target


def test_load_targets_returns_expected_in_scope_targets() -> None:
    json_path = Path(__file__).resolve().parent.parent / "json_examples" / "bugcrowd_data.json"

    targets = set(load_targets(json_path))

    expected = {
        Target(
            name="CoinDesk Data - Data API",
            type="api",
            resource="http://data-api.coindesk.com/",
        ),
        Target(
            name="CoinDesk Data - Tools API",
            type="api",
            resource="https://tools-api.cryptocompare.com/",
        ),
        Target(
            name="*.acorns.com/",
            type="website",
            resource="https://acorns.com/",
        ),
        Target(
            name="https://graphql.acorns.com",
            type="api",
            resource="https://graphql.acorns.com",
        ),
    }
    assert targets == expected


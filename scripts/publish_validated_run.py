from __future__ import annotations

import argparse
import json
from getpass import getpass
from pathlib import Path

from airtraffic.azure import publish_run


PROJECT_ROOT = Path(
    __file__
).resolve().parents[1]


def default_run_id() -> str:
    metadata_path = (
        PROJECT_ROOT
        / "outputs"
        / "qa"
        / "run_metadata.json"
    )

    metadata = json.loads(
        metadata_path.read_text(
            encoding="utf-8"
        )
    )

    return str(
        metadata["run_id"]
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Publish one locally validated "
            "Air Traffic Analytics V2 run "
            "to Azure SQL."
        )
    )

    parser.add_argument(
        "--run-id",
        default=default_run_id(),
    )

    args = parser.parse_args()

    print(
        "Target run:",
        args.run_id,
    )

    password = getpass(
        "Azure SQL password: "
    )

    publish_run(
        project_root=PROJECT_ROOT,
        run_id=args.run_id,
        password=password,
    )


if __name__ == "__main__":
    main()

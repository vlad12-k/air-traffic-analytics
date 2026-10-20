from __future__ import annotations

from getpass import getpass
from pathlib import Path
import re

import pyodbc

from airtraffic.azure import connection_string


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VIEWS_FILE = PROJECT_ROOT / "sql" / "views.sql"


def split_sql_batches(sql: str) -> list[str]:
    return [
        batch.strip()
        for batch in re.split(
            r"(?im)^\s*GO\s*$",
            sql,
        )
        if batch.strip()
    ]


def main() -> None:
    password = getpass(
        "Azure SQL password: "
    )

    sql = VIEWS_FILE.read_text(
        encoding="utf-8"
    )
    batches = split_sql_batches(sql)

    print("===== AZURE V2 REPORTING DEPLOYMENT =====")
    print("SQL file: sql/views.sql")
    print("Batches:", len(batches))
    print(
        "\nNo analytical data will be inserted."
    )

    conn = pyodbc.connect(
        connection_string(password),
        timeout=60,
        autocommit=False,
    )

    try:
        cursor = conn.cursor()

        for number, batch in enumerate(
            batches,
            start=1,
        ):
            print(
                f"Executing batch "
                f"{number}/{len(batches)}..."
            )
            cursor.execute(batch)

        print(
            "\nAll view batches executed. "
            "Verifying..."
        )

        cursor.execute(
            """
            SELECT
                s.name AS schema_name,
                v.name AS view_name
            FROM sys.views AS v
            JOIN sys.schemas AS s
              ON s.schema_id = v.schema_id
            WHERE s.name = 'reporting'
            ORDER BY v.name;
            """
        )

        views = cursor.fetchall()

        if len(views) != 14:
            raise RuntimeError(
                "Expected 14 reporting views, "
                f"found {len(views)}"
            )

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM sys.tables AS t
            JOIN sys.schemas AS s
              ON s.schema_id = t.schema_id
            WHERE s.name = 'dbo'
              AND t.name LIKE 'GT%';
            """
        )

        legacy_count = cursor.fetchone()[0]

        if legacy_count != 10:
            raise RuntimeError(
                "Legacy dbo.GT* table count "
                f"changed unexpectedly: {legacy_count}"
            )

        conn.commit()

        print("\n===== COMMIT SUCCESS =====")
        print("reporting views:", len(views))
        print(
            "legacy dbo.GT* tables preserved:",
            legacy_count,
        )

        print("\nViews:")
        for row in views:
            print(
                f" - {row.schema_name}."
                f"{row.view_name}"
            )

    except Exception:
        conn.rollback()
        print(
            "\nVIEW DEPLOYMENT FAILED — "
            "TRANSACTION ROLLED BACK"
        )
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    main()

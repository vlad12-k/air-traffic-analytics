from __future__ import annotations

from getpass import getpass
from pathlib import Path
import re

import pyodbc

from airtraffic.azure import connection_string


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_FILE = PROJECT_ROOT / "sql" / "schema.sql"


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

    sql = SCHEMA_FILE.read_text(
        encoding="utf-8"
    )

    batches = split_sql_batches(sql)

    print("===== AZURE V2 SCHEMA DEPLOYMENT =====")
    print("SQL file: sql/schema.sql")
    print("Batches:", len(batches))
    print(
        "\nLegacy dbo.GT* tables are NOT modified."
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
            "\nAll batches executed. "
            "Running structural verification..."
        )

        cursor.execute(
            """
            SELECT name
            FROM sys.schemas
            WHERE name IN (
                'meta',
                'bi',
                'reporting'
            )
            ORDER BY name;
            """
        )

        schemas = {
            row.name
            for row in cursor.fetchall()
        }

        expected_schemas = {
            "meta",
            "bi",
            "reporting",
        }

        if schemas != expected_schemas:
            raise RuntimeError(
                "Schema verification failed: "
                f"{schemas}"
            )

        cursor.execute(
            """
            SELECT
                s.name AS schema_name,
                t.name AS table_name
            FROM sys.tables AS t
            JOIN sys.schemas AS s
              ON s.schema_id = t.schema_id
            WHERE s.name IN ('meta', 'bi')
            ORDER BY s.name, t.name;
            """
        )

        tables = cursor.fetchall()

        meta_count = sum(
            row.schema_name == "meta"
            for row in tables
        )

        bi_count = sum(
            row.schema_name == "bi"
            for row in tables
        )

        if meta_count != 2:
            raise RuntimeError(
                f"Expected 2 meta tables, "
                f"found {meta_count}"
            )

        if bi_count != 10:
            raise RuntimeError(
                f"Expected 10 BI tables, "
                f"found {bi_count}"
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
        print(
            "Schemas:",
            ", ".join(sorted(schemas)),
        )
        print("meta tables:", meta_count)
        print("bi tables:", bi_count)
        print(
            "legacy dbo.GT* tables preserved:",
            legacy_count,
        )

    except Exception:
        conn.rollback()
        print(
            "\nDEPLOYMENT FAILED — "
            "TRANSACTION ROLLED BACK"
        )
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    main()

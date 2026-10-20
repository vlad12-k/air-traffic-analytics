from __future__ import annotations

from getpass import getpass
from pathlib import Path

import pyodbc

from airtraffic.azure import connection_string


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SQL_FILE = PROJECT_ROOT / "sql" / "validation_queries.sql"


def main() -> None:
    password = getpass(
        "Azure SQL password: "
    )

    sql = SQL_FILE.read_text(
        encoding="utf-8"
    )

    conn = pyodbc.connect(
        connection_string(password),
        timeout=60,
    )

    try:
        cur = conn.cursor()

        print("===== INDEPENDENT AZURE VALIDATION =====")
        print("SQL: sql/validation_queries.sql")
        print()

        cur.execute(sql)

        result_number = 0

        while True:
            if cur.description:
                result_number += 1

                columns = [
                    column[0]
                    for column in cur.description
                ]

                rows = cur.fetchall()

                print(
                    f"===== RESULT SET {result_number} ====="
                )
                print(
                    " | ".join(columns)
                )

                if rows:
                    for row in rows:
                        print(
                            " | ".join(
                                str(value)
                                if value is not None
                                else "NULL"
                                for value in row
                            )
                        )
                else:
                    print("(no rows)")

                print()

            if not cur.nextset():
                break

        print(
            "===== VALIDATION QUERY EXECUTION COMPLETE ====="
        )

    finally:
        conn.close()


if __name__ == "__main__":
    main()

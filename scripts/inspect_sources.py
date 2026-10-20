from airtraffic.ingest import load_sources

datasets = load_sources()

for name, df in datasets.items():
    print("\n" + "=" * 90)
    print(f"DATASET: {name}")
    print("=" * 90)
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    print("\nCOLUMN NAMES:")
    for i, col in enumerate(df.columns, 1):
        print(f"{i:02d}. {col!r}")

    print("\nDTYPES:")
    print(df.dtypes.to_string())

    print("\nNULL COUNTS:")
    nulls = df.isna().sum()
    nulls = nulls[nulls > 0]
    print(nulls.to_string() if not nulls.empty else "No nulls")

    print("\nDUPLICATE ROWS:")
    print(df.duplicated().sum())

    print("\nFIRST 3 ROWS:")
    print(df.head(3).to_string(index=False))

print("\nSCHEMA INSPECTION COMPLETE")

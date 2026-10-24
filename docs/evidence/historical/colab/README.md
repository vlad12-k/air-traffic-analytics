# Historical Google Colab evidence

![Historical Google Colab ETL screenshot with restricted upload outputs masked](colab-etl-upload-redacted.png)

This is an authentic, minimally redacted screenshot of the project notebook `AirTraffic_ETL_GoldenTables.ipynb`. It shows a SQLAlchemy connection using ODBC Driver 18 with encryption enabled and certificate trust disabled, a loop over CSVs in `out/golden`, `pandas.read_csv`, and `DataFrame.to_sql(..., if_exists='replace', index=False)`. The connection-success message is visible. The upload-result block is covered in full; no AVI0301-linked/mixed-source table counts or data values are reproduced. No actual credentials are visible: the connection code uses `{username}`, `{password}`, `{server}` and `{database}` placeholders.

The screenshot is historical evidence of a local CSV-to-Azure-SQL handoff, not a current pipeline, a reproducible notebook or proof of data reconciliation. In particular, `if_exists='replace'` overwrites destination tables on a rerun; the capture does not evidence transactional staging, rollback, schema contracts or source-to-target reconciliation. No measures, filtering, relationship logic or business finding are shown.

The exact original is included separately as [the original notebook screenshot](colab-etl-upload-original.png); it is not withheld or replaced. The redacted derivative preserves the code/connection region and masks the upload-result block, with pixels outside the mask verified against the archive original. No raw CSV is included. Google's [Brand Resource Center guidance](https://about.google/brand-resource-center/guidance/) is referenced only for project context; no Google endorsement or aviation-data license is claimed.

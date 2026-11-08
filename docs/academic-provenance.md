# Academic provenance

## Origin

This project originated as an individual **Unit 19 Business Intelligence academic assessment**. The owner-provided assignment brief framed airport retail-location decision support as a scenario involving **RCO Data Services Ltd (RDS)** and **Luxury Watch Company (LWC)**. Both organisations are fictional scenario entities; neither is an employer, customer, or commercial project participant.

The brief required a business-intelligence solution and identified learning resources and aviation dataset links, including GOV.UK, the UK Civil Aviation Authority (CAA), DataSF and Pearson HN Global. The college's provision or identification of those resources describes the academic access context only. It does not establish permission to republish third-party datasets, derived tables, maps, software interfaces or screenshots.

The complete Pearson assignment brief is not reproduced here. Its publication rights were not independently established for this repository.

## Individual contribution and project evolution

The owner reports personally performing the academic analytical work and subsequent portfolio development, including:

- Python and pandas data preparation and profiling;
- Google Colab ETL and historical Azure SQL workflows;
- design and use of Golden Tables GT1–GT10;
- IBM Cognos Analytics model/report design and reporting;
- IBM watsonx AutoAI exploration;
- Microsoft Power BI dashboard design;
- later Python/SQL V2 implementation, data-quality checks, reconciliation, provenance and decision modelling.

The academic work and later V2 implementation are successive stages, not one fully reproducible historical pipeline. Current V2 code and its tests do not retroactively validate historical Colab outputs, Azure query grids, Cognos report calculations or watsonx experiments. The repository does not claim a live cloud service, commercial deployment, deployed ML model or current Cognos refresh.

No employment by RDS or LWC, commercial client relationship, production ownership, or commercial outcome is claimed.

## Dataset-period distinction

The assignment periods, local snapshots and current publisher pages are separate facts:

| Source | Assignment context (owner-provided brief) | Local V2 snapshot | Boundary |
|---|---|---|---|
| CAA Table 12.1 | May 2022 table | Source period `202205`, compared with May 2021 | Not 2020 and not a continuous annual series. The original brief and the local file do not establish an acquisition date. |
| DfT AVI0105 | 2011–2021 | 2013–2023 | The currently linked DfT ODS is a later 2014–2024 publication; it is not evidence of the historical input used. |
| DfT AVI0301 / ICAO | 2019–2020 | 2021–2022 | The originating ICAO edition, exact access product and redistribution permission for the local snapshot are not recorded. |
| SFO / DataSF | SFO passenger benchmark | Local file named `Air_Traffic_Passenger_Statistics_2005-2020.csv`; observed activity periods extend from 2005-01 through 2025-07 | The filename is retained unchanged; it does not describe the full observed local coverage. |

See [source and licensing details](data-sources-and-licensing.md) for source-specific attribution, rights scope and unresolved questions, and [reproducibility](reproducibility.md) for the local-input boundary.

## Evidence and claims

Historical screenshots are preserved as evidence of captured project stages. A screenshot documents what was visible in that capture; it does not by itself establish source rights, a reproducible refresh, correct calculations, a current service, or vendor endorsement. Owner authorship or a direction to preserve an image does not grant rights over embedded third-party data, maps or vendor assets. The [per-image screenshot inventory](evidence/screenshot-release-inventory.md) records exact paths, status of visual inspection, content, source lineage and unresolved questions.

The academic origin is context for the work, not a claim that all historical artifacts are independently reproducible or cleared for unrestricted republication. The project narrative and evidence boundaries are documented in the [business case study](business-case-study.md) and [end-to-end walkthrough](end-to-end-project-walkthrough.md).

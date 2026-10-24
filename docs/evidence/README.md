# Public evidence gallery and local-only screenshot boundary

This index distinguishes owner-authorized report captures from third-party product-interface terms and data-source conditions. Five original owner-created BI captures are included, along with two Power BI schema-only originals and one redacted historical Colab derivative. The four SVGs are separate data/chronology graphics and do not count as platform screenshots or proof of hands-on vendor use.

## Public visual evidence

- [Power BI V2 original-image gallery and technical walkthrough](power-bi-v2/technical-notes.md)
- [Historical Cognos original-image gallery and technical walkthrough](historical/cognos/technical-notes.md)
- [Historical engineering evidence gallery — all seven Colab, Azure SQL, watsonx and SIPOC images](historical/README.md)


| File | Stage / question | What it demonstrates | Provenance / limit |
|---|---|---|---|
| [Project evolution timeline](visualizations/project-evolution-timeline.svg) | Cognos → Colab → Azure SQL → Python/SQL V2 → Power BI V2 | Historical sequence and distinction between earlier tools and the current governed model/report layer | Original project summary diagram based on repository documentation and local evidence; not a technical migration claim or screenshot. |
| [UK airport market snapshot](visualizations/uk-airport-market-snapshot.svg) | UK_SITE: compare passenger-market scale | Top five airports in the represented CAA extract | Original GT3-based chart; CAA Table 12.1, May 2022; source credit and no-resale condition embedded. |
| [UK demand and connectivity](visualizations/uk-site-demand-connectivity.svg) | UK_SITE: compare Heathrow demand and route breadth | Source-period passenger comparison, destination reach, scheduled/charter passenger mix, and top five Heathrow destination-country flows | Original figure from permitted GT1/GT4/GT8 CAA-derived outputs; not annual airport totals, retail footfall, or a vendor export. Attribution and no-resale condition embedded. |
| [UK scenario stability](visualizations/uk-site-scenario-stability.svg) | UK_SITE: does the lead candidate change under policy weights? | Heathrow leads the baseline and both documented UK sensitivity scenarios | Original summary of the already documented UK-only result. Scores and global candidate results are not included. Sensitivity is not probability or profitability. |
| [Power BI UK market demand](power-bi-v2/powerbi-v2-02-uk-market-demand.png) | UK_SITE: compare passenger demand | Original report page authored by the project owner; source CAA Table 12.1, May 2022 | User-authorized original; CAA attribution/no-resale notice applies. Microsoft UI remains visible; no Microsoft permission or endorsement is claimed. |
| [Power BI UK_SITE sensitivity](power-bi-v2/powerbi-v2-05b-scenario-sensitivity-uk.png) | UK_SITE: compare policy-weight scenarios | Original owner-created report page and scenario visual | User-authorized original; CAA attribution/no-resale applies to source measures. No Microsoft permission or endorsement is claimed. |
| [Power BI Heathrow candidate detail](power-bi-v2/powerbi-v2-07b-candidate-detail-heathrow.png) | UK_SITE: explain the Heathrow candidate screen | Original owner-created candidate-detail page | User-authorized original; CAA attribution/no-resale applies. No Microsoft permission or endorsement is claimed. |
| [IBM Cognos semantic model](historical/cognos/historical-cognos-07-semantic-model.png) | Historical model design | Original schema/semantic-model screenshot; no source rows displayed | User-authorized original; IBM interface is visible; no IBM permission or endorsement is claimed. |
| [IBM Cognos UK demand filter](historical/cognos/historical-cognos-11-demand-filter.png) | Historical UK demand and filtering | Original owner-created filtered report page | User-authorized original; CAA attribution/no-resale applies. IBM interface is visible; no IBM permission or endorsement is claimed. |
| [Historical Colab ETL handoff — redacted authentic derivative](historical/colab/colab-etl-upload-redacted.png) | Historical CSV-to-Azure-SQL stage | Notebook title, connection pattern, CSV loop, `read_csv` and `to_sql` code, and successful connection; the output block is fully masked | Original output contains AVI0301/mixed-source counts and remains local. The derivative preserves the rest of the original pixels and is labeled; Google brand guidance for school projects is cited, with no endorsement or data-rights claim. |

| [Power BI semantic model screenshot](power-bi-v2/powerbi-v2-08-semantic-model-overview.png) | Current Power BI V2 | Report model structure | Schema-only vendor screenshot, included under the documented Microsoft screenshot conditions and attribution. |
| [Power BI relationships screenshot](power-bi-v2/powerbi-v2-09-relationships-overview.png) | Current Power BI V2 | Model relationship structure | Schema-only vendor screenshot, included under the documented Microsoft screenshot conditions and attribution. |

The data-bearing CAA visualizations are free-to-view portfolio documentation; CAA attribution and the no-sale/no-resale condition remain applicable. The code MIT license does not replace source-data or screenshot terms. See [data sources and licensing](../data-sources-and-licensing.md).

## Original archive accounting (26 PNGs)

The source ZIP is preserved unchanged. Five user-authorized PNGs are included above; two Power BI schema/model captures were already public. The other 19 archive images remain local-only:

| Original archive entry | Status and specific remaining issue |
|---|---|
| `Power BI, Semantik Models/01-executive-decision-summary.png` | Local only: global decision content contains results under the existing AVI0301/ICAO restriction. |
| `Power BI, Semantik Models/03-destination-connectivity.png` | Local only: this CAA-based page has map data credits visible for OpenStreetMap, Microsoft, Esri Community Maps, and the Esri map layer, but attribution alone does not establish reuse rights for the basemap. Microsoft's [published screenshot guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/copyright/permissions) prohibit screenshots containing third-party content and prohibit alteration/cropping beyond resizing under the standard website-use permission. The map and CAA content therefore remain in the untouched original; redaction is not a compliant substitute under that guidance. |
| `Power BI, Semantik Models/04-global-expansion-benchmark.png` | Local only: global benchmark results under the AVI0301/ICAO restriction. |
| `Power BI, Semantik Models/05a-scenario-global-expansion.png` | Local only: global scenario results under the AVI0301/ICAO restriction. |
| `Power BI, Semantik Models/06-data-quality-governance.png` | Local only: governance page includes global-source/AVI0301-derived counts and Microsoft UI. |
| `Power BI, Semantik Models/07a-candidate-detail-dubai.png` | Local only: global candidate analysis under the AVI0301/ICAO restriction. |
| `Cognos, Colab, Azure/08-cognos-executive-summary.png` | Local only: global airport comparisons under the AVI0301/ICAO restriction; IBM UI also remains uncleared. |
| `Cognos, Colab, Azure/09-cognos-executive-filter.png` | Local only: filtered global comparisons under the AVI0301/ICAO restriction; IBM UI also remains uncleared. |
| `Cognos, Colab, Azure/10-cognos-demand-recovery.png` | Local only: the visible dashboard is a UK-airport 2020-vs-2022 recovery view, not the global comparison previously assumed. The archive does not identify the source lineage for this multi-year series; the public CAA ROUTES input is a single comparison snapshot and cannot validate it. Do not publish the values until the historical source and rights are mapped. |
| `Cognos, Colab, Azure/12-cognos-operational-monitoring.png` | Local only: operational/global benchmark values remain under the existing AVI0301/ICAO restriction; IBM UI is separate. |
| `Cognos, Colab, Azure/13-cognos-operational-filter.png` | Local only: filtered operational/global values remain under the existing AVI0301/ICAO restriction; IBM UI is separate. |
| `Cognos, Colab, Azure/14-cognos-risk-ranking.png` | Local only: the screenshot contains populated UK airport rows and passenger, route-count, recovery and composite-score fields. The original archive does not identify the source lineage; the existing local evidence map associates the UK-labelled results with AVI0301-matching benchmark values. Keep the original unchanged and do not publish these rows/scores until source and redistribution rights are established. |
| `Cognos, Colab, Azure/01-business-process-sipoc.png` | Local only: process diagram has no visible authorship/copyright attribution; owner confirmation or a license for this exact diagram is needed. It is not a dashboard screenshot. |
| `Cognos, Colab, Azure/02-azure-sql-database.png` | Local only: original exposes Azure resource/account identifiers and Microsoft UI. Redacted copy is not the original; no altered screenshot is published. |
| `Cognos, Colab, Azure/03-colab-azure-etl.png` | Original remains local: its upload-result block contains AVI0301/GT7-derived counts with unresolved redistribution rights. The public `colab-etl-upload-redacted.png` derivative masks the entire result block; it does not replace the preserved original or imply rights to the data. |
| `Cognos, Colab, Azure/04-azure-sql-validation.png` | Local only: SQL grid includes data-bearing global/recommendation results and Azure UI. |
| `Cognos, Colab, Azure/05-watsonx-import.png` | Local only: IBM UI and account/source labels are visible; no IBM screenshot basis is documented. |
| `Cognos, Colab, Azure/06-watsonx-autoai.png` | Local only: IBM UI and CAA-derived AutoAI metrics; no IBM screenshot basis is documented. |
| `Cognos, Colab, Azure/10. Auto Ai experiment.png` | Local only: IBM UI and CAA-derived model metrics; no IBM screenshot basis is documented. |

Counts: Power BI **11 originals / 5 original PNGs published / 6 originals local**; IBM Cognos **8 / 2 / 6**; historical support **7 originals local / 1 redacted derivative published / 0 original PNGs published**. **Across the 26 originals: 7 original PNGs are published and 19 remain local; the one additional derivative brings the public gallery to 8 image assets.** The four SVG visualizations are supplementary graphics and are not included in the original-screenshot counts. Owner authorization for the five authored BI captures and the cited school-project basis for the Colab derivative do not imply Microsoft or IBM permission, endorsement, or rights in third-party data.

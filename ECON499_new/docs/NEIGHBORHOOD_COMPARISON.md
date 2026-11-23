# Neighborhood socioeconomic context: Lenox Square vs Greenbriar Mall

## Why this comparison?
The original mobility models compare reported activity, but readers need to know why the destinations are substantively different. We use a **same-vintage, same-geography ACS comparison** to describe the ZCTAs containing each destination. We then separately study the **origin ZCTAs** contributing reported device activity.

## Host ZCTA results (2024 ACS five-year)

| Destination | Host ZCTA | Median household income | 90% margin of error | Gini | Gini 90% margin of error | Population |
|---|---:|---:|---:|---:|---:|---:|
| Lenox Square | 30326 | $121,984 | ±$10,671 | 0.4959 | ±0.0568 | 8,234 |
| Greenbriar Mall | 30331 | $62,623 | ±$4,351 | 0.4835 | ±0.0240 | 62,567 |

The estimated host-ZCTA income gap is **$59,361**. These are **ZCTA-level** statistics, not a three-mile catchment or mall visitor incomes. Because 30326 and 30331 have different sizes and residential populations, this is context rather than a controlled matched-neighborhood design.

## Origin-neighborhood analysis
See `notebooks/05_neighborhood_income_context.ipynb` and `results/tables/origin_income_summary_PROVISIONAL.csv`. The weighted origin-income summary is a weighted mean of **ZCTA medians**, not a visitor-level income estimate.

## Limits and next steps
- Dewey origin CBG vintage remains unconfirmed; the origin analysis uses the **provisional 2020 crosswalk**.
- The destination CBG includes more than the mall; reported devices are not transactions or individual visitors.
- A rigorous equal-radius buffer requires a spatially consistent polygon overlay and population weights. It is **not** calculated here.
- No poverty-rate estimates are included because a comparable poverty table was not part of the inspected 25-ZCTA data.
- Never call Greenbriar visitors 'low-income' on the basis of the host ZCTA.

## Sources
- U.S. Census Bureau, ACS 2024 5-year tables B19013, B19083, B01003: https://api.census.gov/data/2024/acs/acs5
- Lenox Square official address: https://www.simon.com/mall/lenox-square/about
- Greenbriar Mall address: https://shopgreenbriar.com/locations/greenbriar-mall/

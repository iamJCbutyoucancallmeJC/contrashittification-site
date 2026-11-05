# Source data

The World series the charts draw, trimmed from Our World in Data's grapher CSVs
(fetched 2026-11-04). OWID's own charts and data are CC BY 4.0; the underlying
data keeps each provider's terms, which is why every source line on the page
names both OWID and the provider.

| file | OWID chart | provider |
|---|---|---|
| `child-mortality-world.csv` | [child-mortality](https://ourworldindata.org/grapher/child-mortality) | Gapminder, UN IGME |
| `solar-pv-prices-world.csv` | [solar-pv-prices](https://ourworldindata.org/grapher/solar-pv-prices) | IRENA, Nemet, Farmer and Lafond |
| `guinea-worm-world.csv` | [number-of-reported-guinea-worm-dracunculiasis-cases](https://ourworldindata.org/grapher/number-of-reported-guinea-worm-dracunculiasis-cases) | WHO |

Refresh a series by re-fetching with `csvType=full&useColumnShortNames=true`,
keeping the `World` rows, then running `build/make-site.py`.

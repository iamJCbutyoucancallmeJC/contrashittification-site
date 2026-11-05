#!/usr/bin/env python3
"""Build contrashittification.com from the data in build/data and the posts below.

Run: /opt/homebrew/bin/python3 build/make-site.py

Everything the page shows is here or in build/data, so a caption or a post can be
changed in one place and the page rebuilt. The charts are drawn from the Our World
in Data CSVs in build/data (CC BY 4.0; the underlying data keeps its provider's
terms, which is why each source line names both). Nothing is fetched at build time.

Design: family tokens only (paper-100 ground, ink text, ink-muted meta, pen links,
gold for the one chart annotation, radius 0, 640 measure). See the vault's
design-language-system.md. Shape (a), the scroll, JC's pick 2026-11-04.
"""
import csv
import html
import math
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "build" / "data"

SITE = "https://contrashittification.com"
WORDMARK = "contrashittification"
SUBTITLE = "the good news collection"
PROMISE = "Things that got better, and things that stayed good."
ABOUT = (
    'A collection of things that run the other way: long-run data showing the world '
    'getting better, and things that have not been enshittified, with the reason each '
    'one held. "Enshittification" is <a href="https://pluralistic.net/2023/01/21/potemkin-ai/#hey-guys">'
    "Cory Doctorow's word</a>, coined in 2022. This is the other half of the ledger."
)


def world_series(filename, column):
    """The World rows of an OWID grapher CSV as {year: value}."""
    out = {}
    with open(DATA / filename, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["entity"] == "World" and row[column].strip():
                out[int(row["year"])] = float(row[column])
    return out


def chart(series, *, log=False, fmt=lambda v: f"{v:,.0f}"):
    """One quiet line chart as inline SVG. No axes, no grid, no box.

    Start and end are labelled and the end carries the single gold mark, which is the
    one annotation the visualization style guide allows per visual unit.
    """
    width, height = 640, 170
    pad_l, pad_r, pad_t, pad_b = 4, 4, 18, 26
    years = sorted(series)
    values = [series[y] for y in years]
    scale = (lambda v: math.log10(v)) if log else (lambda v: v)
    lo, hi = min(map(scale, values)), max(map(scale, values))
    span = (hi - lo) or 1.0
    x0, x1 = years[0], years[-1]

    def px(year):
        return pad_l + (year - x0) / (x1 - x0) * (width - pad_l - pad_r)

    def py(value):
        return pad_t + (hi - scale(value)) / span * (height - pad_t - pad_b)

    points = " ".join(f"{px(y):.1f},{py(series[y]):.1f}" for y in years)
    end_x, end_y = px(x1), py(series[x1])
    # Label the high point, not the first point. They are the same on a series that only
    # falls, and on one that climbs first (guinea worm, where the early counts were thin)
    # the peak is the honest number: the body text quotes it, so the chart must show it.
    peak_year = max(years, key=lambda y: series[y])
    # Only when the peak is far above where the series starts. Guinea worm's is 24 times the
    # 1980 count, so the chart must show it; child mortality's is a 3 percent bump a few
    # decades after 1800, and labelling that would argue with a caption about 1800.
    if series[peak_year] < series[x0] * 1.25:
        peak_year = x0
    peak_x = px(peak_year)
    peak_anchor = "" if peak_x < width / 2 else " c-end"
    high_label, end_label = fmt(series[peak_year]), fmt(series[x1])
    return f"""<svg class="chart" viewBox="0 0 {width} {height}" role="img"
     aria-label="{x0} to {x1}: {html.escape(high_label)} in {peak_year}, down to {html.escape(end_label)} in {x1}">
  <polyline points="{points}" fill="none" stroke="var(--ink)" stroke-width="1.5"
            stroke-linejoin="round" vector-effect="non-scaling-stroke"/>
  <circle cx="{end_x:.1f}" cy="{end_y:.1f}" r="3.5" fill="var(--gold)"/>
  <text class="c-val{peak_anchor}" x="{peak_x:.1f}" y="{py(series[peak_year]) - 8:.1f}">{html.escape(high_label)}</text>
  <text class="c-val c-end" x="{end_x:.1f}" y="{end_y - 16:.1f}">{html.escape(end_label)}</text>
  <text class="c-yr" x="{pad_l}" y="{height - 8}">{x0}</text>
  <text class="c-yr c-end" x="{width - pad_r}" y="{height - 8}">{x1}</text>
</svg>"""


child = world_series("child-mortality-world.csv", "child_mortality_rate")
solar = world_series("solar-pv-prices-world.csv", "cost")
guinea = world_series("guinea-worm-world.csv", "guinea_worm_reported_cases")

POSTS = [
    dict(
        kind="the long line",
        body="In 1800, more than four in ten children died before their fifth birthday. "
             "Now it is fewer than four in a hundred, everywhere on earth.",
        figure=chart(child, fmt=lambda v: f"{v:.1f}%"),
        meta=f"Share of children who die before age five, world, {min(child)} to {max(child)}. "
             "Linear scale.",
        source="Our World in Data, child mortality (CC BY); Gapminder and UN IGME",
        href="https://ourworldindata.org/grapher/child-mortality",
    ),
    dict(
        kind="still good",
        body="Wikipedia has run on donations since 2001. No ads, nothing sold about you, "
             "and no shareholder to turn on the readers. That is the reason it held: the "
             "structure has nobody to enshittify for.",
        meta="Wikimedia Foundation, a nonprofit; the text is free to copy under CC BY-SA.",
        source="wikimediafoundation.org, read 2026-10-29",
        href="https://wikimediafoundation.org/about/",
    ),
    dict(
        kind="good news",
        body="Leaded petrol is gone from every country on earth. Algeria sold the last of it "
             "in July 2021, almost a century after we started putting lead in the air.",
        meta="Announced 30 August 2021.",
        source="UN Environment Programme",
        href="https://www.unep.org/news-and-stories/press-release/era-leaded-petrol-over-eliminating-major-threat-human-and",
    ),
    dict(
        kind="the long line",
        body="The price of a solar panel fell more than a thousandfold in fifty years. "
             "Nobody voted for it. It just kept happening, year after year.",
        figure=chart(solar, log=True, fmt=lambda v: f"${v:,.2f}" if v < 10 else f"${v:,.0f}"),
        meta=f"Solar photovoltaic module price per watt, {min(solar)} to {max(solar)}, "
             "constant dollars. Logarithmic scale.",
        source="Our World in Data, solar PV prices (CC BY); IRENA, Nemet, Farmer and Lafond",
        href="https://ourworldindata.org/grapher/solar-pv-prices",
    ),
    dict(
        kind="the long line",
        body="Guinea worm has no vaccine and no drug. It was driven from 892,055 reported cases "
             "a year to ten, with water filters, teaching and four decades of patience.",
        figure=chart(guinea, log=True),
        meta=f"Reported cases worldwide, {min(guinea)} to {max(guinea)}. The line climbs "
             f"before it falls because the early counts were thin: reporting improved through "
             f"the 1980s, and the high-water mark on record is "
             f"{max(guinea.values()):,.0f} in {max(guinea, key=guinea.get)}. Logarithmic scale.",
        source="Our World in Data, reported guinea worm cases (CC BY); WHO",
        href="https://ourworldindata.org/grapher/number-of-reported-guinea-worm-dracunculiasis-cases",
    ),
]


def post_html(post):
    figure = f'\n      <figure>{post["figure"]}</figure>' if post.get("figure") else ""
    return f"""    <article class="post">
      <p class="kind">{html.escape(post["kind"])}</p>
      <p class="say">{post["body"]}</p>{figure}
      <p class="src">{html.escape(post["meta"])} <a href="{post["href"]}">{html.escape(post["source"])}</a></p>
    </article>"""


PAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>contrashittification</title>
<meta name="description" content="{html.escape(PROMISE)} A collection of long-run data and things that have not been enshittified.">
<link rel="canonical" href="{SITE}/">
<meta property="og:title" content="contrashittification">
<meta property="og:description" content="{html.escape(PROMISE)}">
<meta property="og:url" content="{SITE}/">
<meta property="og:type" content="website">
<meta property="og:image" content="{SITE}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="stylesheet" href="/styles.css">
</head>
<body>
  <header>
    <h1>{WORDMARK}</h1>
    <p class="sub">{SUBTITLE}</p>
    <p class="promise">{html.escape(PROMISE)}</p>
  </header>

  <main>
{chr(10).join(post_html(p) for p in POSTS)}
  </main>

  <footer>
    <p class="about">{ABOUT}</p>
    <p class="foot"><a href="/changelog/">changelog</a></p>
  </footer>
</body>
</html>
"""

(ROOT / "index.html").write_text(PAGE, encoding="utf-8")
print(f"index.html written: {len(POSTS)} posts, built {date.today()}")

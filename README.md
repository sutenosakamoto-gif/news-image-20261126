# World News — 26 November 2026 (one-image summary)

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/sutenosakamoto-gif/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/sutenosakamoto-gif/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

A one-image broadsheet front page summarising forty world news
stories of Thursday, 26 November 2026, prepared as an entry
for the make.fun bounty "Sum up 26 November's world news in one image"
(final deadline 2026-11-28 09:00 JST).

## Contents

- `main.py` — the entry point: a standard-library only program that
  copies the finished page to `/output/entry.png` (no network). It checks
  the page is a 1024×1024 PNG under the 1 MiB cap before copying.
- `page.png` — the finished 1024×1024 front page.
- `render.py` — the build-time renderer that drew `page.png` from
  `content.py` with real fonts (system Noto Serif, OFL).
- `content.py` — the day's stories, numbers, timeline and exclusions
  as structured data.
- `fallback_main.py` — a standard-library-only renderer that draws the
  same broadsheet with a built-in bitmap font; the insurance version if
  the build-time render ever fails.
- `SOURCES.md` — the forty stories, their sources (outlet + date)
  and URLs.

## How to run

```bash
python3 main.py   # standard library only, no dependencies
```

Running `python3 main.py` copies `page.png` to `/output/entry.png`,
falling back to `./entry.png` next to the script when `/output` is not
writable. The render is deterministic: repeated runs produce identical
bytes.

To re-render the page from the structured content (build-time only,
needs PIL and the Noto fonts):

```bash
python3 render.py   # writes page.png
```

## The forty stories

Lead panels (large):

1. Iran says more ships hit mines in the Strait of Hormuz; Brent climbs
   to $94.71 (Reuters) — CLAIM for the mine strikes
2. Israel kills nine in Gaza on a third night of strikes (Reuters) —
   REPORTED
3. Thanksgiving storm slams the US East Coast; the 100th Macy's parade
   moves to Saturday (AFP) — CONFIRMED

Medium panels:

4. Congo Ebola cases pass 12,000
5. UniCredit clears the last hurdle for its €41bn Commerzbank deal
6. Bank of Korea hikes to 3.25%
7. Kim tours nuclear sites, urges wider nuke use
8. UK writes to 100,000 strategic reservists
9. Japan calls the US tariff plan "regrettable"
10. Asian shares bounce after Wall Street's fightback
11. Indonesia mine: 13 dead, 13 still trapped
12. Myanmar says it will not fully obey the ICJ genocide orders
13. EU leaders open a two-day summit on a €1.6tn budget
14. Pacific trade bloc meets in Vietnam after the US tariff salvo
15. Sinner ruled out of the Australian Open
16. Babcock wins a record £8.7bn submarine contract

Plus twenty-four briefs (17–40), a world map with numbered pins and a
Europe detail inset, a THE DAY IN NUMBERS strip, a UTC timeline, and a
DATE CHECK footer naming the stories excluded as other days' news.

# Structured content for the 26 November 2026 world-news broadsheet.
# Every item verified against a dated 26 Nov 2026 wire/official source
# (see SOURCES.md). Certainty: CONFIRMED = wire reports the fact directly;
# OFFICIAL = official statement/statistics; REPORTED = wire reports it citing
# a source; CLAIM = one party's claim, attribution kept in the headline/body.

MASTHEAD = "THE WORLD IN ONE PAGE"
DATE_LINE = "THURSDAY 26 NOVEMBER 2026"
SUBHEAD = ("Mines in Hormuz lift oil past $94  ·  Gaza strikes a third night  ·  "
           "A Thanksgiving storm batters the East Coast")
REGION_COUNTS = [("MIDDLE EAST", 5), ("EUROPE", 11), ("ASIA-PACIFIC", 12),
                 ("AFRICA", 6), ("NORTH AMERICA", 2), ("LATIN AMERICA", 2),
                 ("GLOBAL", 2)]
TOTAL_STORIES = 40

# num, region, certainty, headline, body, chip, illustration kind, (lon, lat)
LEADS = [
    (1, "MIDDLE EAST", "CLAIM",
     "Iran says more ships hit mines in the Strait of Hormuz",
     "Tehran reports an LNG carrier on fire and a container ship mined; "
     "identities unconfirmed. Brent $94.71.",
     "$94.71", "strait", (56.3, 26.5)),
    (2, "MIDDLE EAST", "REPORTED",
     "Israel kills nine in Gaza on a third night of strikes",
     "Medics say the dead include the Hamas-appointed deputy education "
     "minister and his wife.",
     "9 KILLED", "night", (34.5, 31.4)),
    (3, "NORTH AMERICA", "CONFIRMED",
     "Thanksgiving storm slams the US East Coast",
     "80m+ under alerts, gusts to 70 mph, flooding. The 100th "
     "Macy\u2019s parade moves to Saturday \u2014 a first.",
     "80M+ ALERTS", "storm", (-74.0, 40.7)),
]

# num, region, certainty, headline, body, chip, illustration kind, (lon, lat)
MIDDLE = [
    (4, "AFRICA", "CONFIRMED",
     "Congo Ebola cases pass 12,000",
     "12,021 cases, 5,904 deaths; now in 8 of 26 provinces.",
     "12,021", "congo", (23.0, -3.0)),
    (5, "EUROPE", "CONFIRMED",
     "UniCredit clears last hurdle for \u20ac41bn deal",
     "Poland\u2019s regulator gives the final approval; a board vote is sought.",
     "\u20ac41bn", "bank", (8.7, 50.1)),
    (6, "ASIA-PACIFIC", "OFFICIAL",
     "Bank of Korea hikes to 3.25%",
     "A quarter-point rise, the highest since Nov 2024, on a chip export boom.",
     "3.25%", "bars", (127.0, 37.5)),
    (7, "ASIA-PACIFIC", "OFFICIAL",
     "Kim tours nuclear sites, urges wider nuke use",
     "KCNA reports the tour on Thursday; the visit was Wednesday.",
     "KCNA \u00b7 THU", "centrifuge", (125.8, 39.0)),
    (8, "EUROPE", "CONFIRMED",
     "UK writes to 100,000 strategic reservists",
     "First such letters since the Cold War; \u2018a sensible precaution\u2019, "
     "not mobilisation.",
     "100,000", "soldiers", (-0.1, 51.5)),
    (9, "ASIA-PACIFIC", "CONFIRMED",
     "Japan calls the US tariff plan \u2018regrettable\u2019",
     "Tokyo protests a proposed 15% levy; Seoul vows talks to protect "
     "its interests.",
     "15%", "tariff", (139.7, 35.7)),
    (10, "ASIA-PACIFIC", "CONFIRMED",
     "Asian shares bounce after Wall Street\u2019s fightback",
     "Nikkei +1.6%, Kospi +1.9% in a thin holiday session.",
     "+1.6%", "line", (139.7, 35.7)),
    (11, "ASIA-PACIFIC", "CONFIRMED",
     "Indonesia mine: 13 dead, 13 still trapped",
     "Search resumes in the flooded Bogor gold mine; 26 were inside "
     "when a river burst in.",
     "13 + 13", "mine", (106.8, -6.6)),
    (12, "ASIA-PACIFIC", "CONFIRMED",
     "Myanmar says it will not fully obey the ICJ genocide orders",
     "The junta rejects \u2018inappropriate\u2019 parts of last week\u2019s ruling "
     "on the 2017 crackdown.",
     "ICJ", "court", (96.2, 19.8)),
    (13, "EUROPE", "CONFIRMED",
     "EU leaders open a two-day summit on a \u20ac1.6tn budget",
     "No deal expected this week; the aim is agreement on 17\u201318 December.",
     "\u20ac1.6tn", "summit", (4.35, 50.85)),
    (14, "LATIN AMERICA", "CONFIRMED",
     "Pacific trade bloc meets in Vietnam after the US tariff salvo",
     "CPTPP, ASEAN and the EU\u2019s trade chief gather; members include "
     "Chile, Mexico and Peru.",
     "12 NATIONS", "ship", (105.85, 21.0)),
    (15, "ASIA-PACIFIC", "CONFIRMED",
     "Sinner ruled out of the Australian Open",
     "The two-time champion, 25, misses January after knee surgery; "
     "out since winning Wimbledon.",
     "AO 2027", "tennis", (145.0, -37.8)),
    (16, "EUROPE", "CONFIRMED",
     "Babcock wins a record \u00a38.7bn submarine contract",
     "A five-year UK defence deal, the largest in the firm\u2019s history; "
     "shares rise 5.8%.",
     "\u00a38.7bn", "submarine", (-4.15, 50.37)),
]

# num, region, certainty, headline, detail
ALSO = [
    (17, "MIDDLE EAST", "REPORTED",
     "Saudi defences stop two Houthi missiles aimed at Riyadh",
     "Coalition says both were intercepted; a blast rocks Sanaa."),
    (18, "EUROPE", "CONFIRMED",
     "European stocks rally; STOXX 600 +1.4%",
     "Banks and tech lead as tariff fears ease."),
    (19, "EUROPE", "CONFIRMED",
     "Diesel tanker sinks off Ibiza; one crew member dies",
     "Spain activates its maritime pollution plan."),
    (20, "EUROPE", "REPORTED",
     "Snow blankets Vienna; buses stuck in the morning rush",
     "Up to 15 cm possible; warnings across the region."),
    (21, "EUROPE", "OFFICIAL",
     "German consumer sentiment edges up to \u221230.2",
     "GfK/NIM index rises 0.7 points into December."),
    (22, "EUROPE", "CONFIRMED",
     "Italy asks Germany to stop a Henkel factory closure",
     "Rome wants Berlin to intercede with the Persil-maker."),
    (23, "EUROPE", "REPORTED",
     "airBaltic offers crew exit, demotion or a PNG secondment",
     "Staff hit by soaring jet fuel prices since the Iran war."),
    (24, "MIDDLE EAST", "CONFIRMED",
     "Eisenkot resumes coalition talks with the Democrats",
     "Israel\u2019s would-be PM restarts talks after a suspension."),
    (25, "MIDDLE EAST", "REPORTED",
     "Kushner: Trump keeps \u2018all options on table\u2019 on Iran",
     "Envoy confirms he has met Iranian representatives."),
    (26, "ASIA-PACIFIC", "CONFIRMED",
     "Australia set to pass an LNG reserve law",
     "Exporters would keep up to a fifth of output at home."),
    (27, "ASIA-PACIFIC", "CONFIRMED",
     "Japan opposition files a censure motion on the education minister",
     "Eight parties act over a political funds scandal."),
    (28, "ASIA-PACIFIC", "CONFIRMED",
     "Hong Kong marks a year since the Tai Po fire killed 168",
     "Mourners lay flowers; the government holds no memorial."),
    (29, "ASIA-PACIFIC", "CONFIRMED",
     "Indian shares extend gains on record foreign inflows",
     "A record $15.16bn came in this month."),
    (30, "AFRICA", "CONFIRMED",
     "DR Congo summons Uganda\u2019s envoy over rebel-takeover posts",
     "Statement was Wednesday; BBC reports it Thursday."),
    (31, "AFRICA", "CONFIRMED",
     "Kenya court: Ebola quarantine site build breached the constitution",
     "The US-backed facility\u2019s construction was ruled unlawful."),
    (32, "AFRICA", "OFFICIAL",
     "Rwanda hikes its rate 75bp to 9.5% as inflation hits 19.5%",
     "Central bank acts to pull inflation towards 5%."),
    (33, "AFRICA", "CONFIRMED",
     "First generic HIV-prevention drug shipments reach Africa",
     "300,000 vials planned for Zambia, Uganda and Zimbabwe."),
    (34, "AFRICA", "CONFIRMED",
     "Tullow Oil to beat its annual output target",
     "New Ghana wells outperform; output averaged 45.2 kboepd."),
    (35, "GLOBAL", "CONFIRMED",
     "Gold steadies after hitting a more-than-one-year low",
     "Hot US inflation data keeps Fed hike bets alive."),
    (36, "EUROPE", "REPORTED",
     "Trump and NATO chief urge Russia not to widen the Ukraine war",
     "Meeting was Wednesday in Florida; statement reported Thursday."),
    (37, "LATIN AMERICA", "CONFIRMED",
     "Brazil calls the US tariff plan \u2018unacceptable\u2019",
     "Statement was Wednesday evening; Lula\u2019s office warns of "
     "reciprocal measures."),
    (38, "NORTH AMERICA", "CONFIRMED",
     "US markets shut for Thanksgiving",
     "Wall Street closed after the Nasdaq slid 2% on Wednesday."),
    (39, "ASIA-PACIFIC", "CONFIRMED",
     "Japan property draws global money",
     "Funds raised $4.66bn in 2026, nearing 2025\u2019s $4.99bn."),
    (40, "GLOBAL", "CONFIRMED",
     "Apple pulls MiniMax\u2019s Talkie chatbot",
     "Removed over child-safety concerns; data was also accessed."),
]

# (big figure, caption) — all 26 Nov figures
NUMBERS = [
    ("$94.71", "BRENT CRUDE, THU"),
    ("12,021", "EBOLA CASES, DR CONGO"),
    ("100,000", "UK RESERVISTS WRITTEN TO"),
    ("80M+", "PEOPLE UNDER STORM ALERTS"),
    ("\u20ac41bn", "UNICREDIT DEAL VALUE"),
    ("+1.6%", "NIKKEI ON THURSDAY"),
    ("13", "DEAD IN INDONESIA MINE"),
]

# (UTC time label, event) — time order
TIMELINE = [
    ("OVERNIGHT", "Israeli strikes kill nine in Gaza"),
    ("01:19", "KCNA reports Kim\u2019s nuclear-site tour"),
    ("01:37", "Brent $94.71 as Iran claims mine strikes"),
    ("02:05", "Macy\u2019s 100th parade moved to Saturday"),
    ("03:01", "Seoul vows talks after US tariff plans"),
    ("03:55", "Indonesia mine search resumes"),
    ("05:29", "Congo Ebola passes 12,000 cases"),
    ("07:14", "Babcock wins \u00a38.7bn submarine deal"),
    ("07:28", "UniCredit clears last Commerzbank hurdle"),
]

# (day label, exclusion note)
DATECHECK = [
    ("WED 25 NOV",
     "Section 301 tariff announcement; US PCE +3.8%, core 3.3%; Q3 GDP "
     "4.3%. Only the reactions are Thu."),
    ("WED 25 NOV",
     "Shenzhou-24 launch; Houthi claims on Ras Tanura and Riyadh; "
     "Cairo tanker fire, 31 dead."),
    ("WED 25 NOV",
     "UK energy price cap +26%; Australia\u2013Solomon Islands pact; "
     "N. Korea expels the Swiss envoy."),
    ("WED 25 NOV",
     "SpaceX FCC approval for 1m Starmind satellites; MLB sues its "
     "players\u2019 union; Luma contract axed."),
    ("WED 25 NOV",
     "Two tankers hit mines in Hormuz; UKMTO Dubai explosion; Kyiv hit "
     "by ballistic missiles; Savasleyka."),
    ("TUE 24 NOV",
     "Sudan RSF drone strikes kill 19 in Blue Nile; Duran Duran "
     "guitarist Andy Taylor dies, 65."),
    ("WED EVENING",
     "Decided Wed, reported Thu: Macy\u2019s move; Kim\u2019s tour; Myanmar\u2019s "
     "ICJ refusal; Congo\u2013Uganda summons; more."),
    ("NOT YET",
     "Spain election Sun 29 Nov; OPEC+ meetings 29 Nov; ITLOS Falklands "
     "ruling Sat 28 Nov; Europa League results."),
]

LEGEND = ("CONFIRMED = 2+ outlets  \u00b7  OFFICIAL = on the record  \u00b7  "
          "REPORTED = one outlet  \u00b7  CLAIM = one side\u2019s account")
ILLU_NOTE = "Scenes are drawn illustrations, not photographs."

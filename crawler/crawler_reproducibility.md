# Crawler Reproducibility

## Purpose

The crawler pipeline collects public Instagram text data for the project. Python is used only for data acquisition. All substantive data processing and analysis are conducted in R.

## Environment

Recommended environment:

```text
Python 3.10+
Google Chrome installed
selenium>=4.45.0
```

Install dependencies from inside this folder:

```powershell
python -m pip install -r requirements.txt
```

## Scripts

```text
scripts/instagram_higo_scrape.py
scripts/hashtag_market_collect_raw.py
```

`instagram_higo_scrape.py` collects posts, captions, engagement counts, and visible comments from the project account.

`hashtag_market_collect_raw.py` collects raw candidate posts for the selected hashtags. It does not clean, deduplicate, sample, or model the data.

## Hashtag Collection Plan

The hashtag crawler uses 16 Higo-derived hashtags:

```text
#yogaretreat
#retreatlife
#retreatcenter
#yogaretreatsworldwide
#retreatmallorca
#yogamallorca
#mallorcayogaretreat
#mallorcaretreat
#fincahigo
#mallorcahotel
#calatuent
#sacalobra
#wellnessretreat
#mindfulness
#ecoretreat
#consciousliving
```

The Python target is approximately 200 raw candidates per hashtag when available.

## How To Run

Higo account scrape:

```powershell
.un_higo_scrape.ps1
```

Hashtag raw candidate scrape:

```powershell
.un_hashtag_raw_collect.ps1
```

If Instagram asks for login, run the script in visible mode or open the Chrome profile manually. Do not commit the Chrome profile folder.

## Outputs

Account-level output:

```text
outputs/instagram_higo/higo_instagram_posts.csv
outputs/instagram_higo/higo_instagram_comments.csv
outputs/instagram_higo/higo_posts_raw.json
outputs/instagram_higo/higo_scrape_summary.json
```

Raw hashtag output:

```text
outputs/instagram_hashtags/hashtag_candidates_raw.csv
outputs/instagram_hashtags/hashtag_raw_collection_summary.csv
outputs/instagram_hashtags/hashtag_raw_collection_summary.json
outputs/instagram_hashtags/hashtag_list.txt
```

## R Handoff

The raw hashtag file should be loaded in R from:

```text
crawler/outputs/instagram_hashtags/hashtag_candidates_raw.csv
```

R should then perform:

```text
1. duplicate removal
2. caption quality filtering
3. relevance filtering
4. spam/giveaway filtering
5. account-level cap
6. final sampling, e.g. 100 posts per hashtag
7. LLM/BERT-ready corpus creation
```

## Limitations

- Instagram page and internal API structures may change.
- Login may be required for stable data collection.
- The crawler stores aggregate engagement counts, not liker lists.
- Comments from the account scrape are only the visible comments on the web page.
- No private accounts or private customer data are collected.

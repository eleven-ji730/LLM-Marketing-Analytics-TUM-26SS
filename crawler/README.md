# Crawler Materials

This folder contains all Python-based data collection materials for the project.

Python is used only for Instagram data collection because browser automation and Instagram web extraction are more practical in Python. All downstream data processing, cleaning, deduplication, sampling, modeling, visualization, and interpretation should be conducted in R according to the course requirements.

## Folder Structure

```text
crawler/
|-- README.md
|-- crawler_reproducibility.md
|-- requirements.txt
|-- config.example.json
|-- run_higo_scrape.ps1
|-- run_hashtag_raw_collect.ps1
|-- scripts/
|   |-- instagram_higo_scrape.py
|   |-- hashtag_market_collect_raw.py
|-- outputs/
|   |-- instagram_higo/
|   |-- instagram_hashtags/
```

## What Belongs Here

- Python crawler scripts
- Python dependency list
- crawler run commands
- raw crawler outputs
- crawler reproducibility notes

## What Does Not Belong Here

- R cleaning or modeling scripts
- manually edited final datasets
- private email or WhatsApp data
- Instagram passwords, cookies, or Chrome profile folders
- final figures, tables, or model outputs

## Current Raw Outputs

`outputs/instagram_higo/` contains the account-level Instagram post and comment data.

`outputs/instagram_hashtags/` contains raw hashtag candidate posts. These are not final cleaned samples. They are intended as input to the R pipeline.

## Important Method Rule

For hashtag market data, Python stops after raw candidate collection. The following steps should be implemented in R:

- cleaning duplicate posts
- removing empty or too-short captions
- filtering irrelevant/spam/giveaway content
- limiting posts per account
- selecting final 100 posts per hashtag where possible
- creating LLM-ready corpora

# Crawler Data Dictionary

This document explains the fields in the crawler output files.

## 1. `outputs/instagram_higo/higo_instagram_posts.csv`

This table contains post-level data from the project Instagram account.

| Field | Meaning |
|---|---|
| `url` | URL of the Instagram post or reel |
| `shortcode` | Unique Instagram post/reel identifier in the URL |
| `media_id` | Instagram internal media ID |
| `taken_at` | Original Instagram timestamp in Unix format |
| `datetime_utc` | Post timestamp converted to UTC datetime |
| `media_type` | Instagram media type code, e.g. image, video, carousel |
| `product_type` | Instagram product type, e.g. `feed`, `clips`, `carousel_container` |
| `location_name` | Location attached to the post, if available |
| `like_count` | Number of likes at the time of scraping |
| `comment_count` | Number of comments at the time of scraping |
| `view_count` | Number of views, if available |
| `caption` | Main text caption of the post |
| `hashtags` | Hashtags extracted from the caption |
| `mentions` | Mentioned accounts extracted from the caption |
| `scraped_comments_count` | Number of visible comments collected for this post |
| `parse_status` | Whether the post was successfully parsed, e.g. `ok` |

## 2. `outputs/instagram_higo/higo_instagram_comments.csv`

This table contains visible comments from the project Instagram account posts.

| Field | Meaning |
|---|---|
| `post_shortcode` | Shortcode of the post the comment belongs to |
| `post_url` | URL of the related Instagram post |
| `comment_id` | Instagram internal comment ID |
| `comment_created_at` | Original comment timestamp in Unix format |
| `comment_datetime_utc` | Comment timestamp converted to UTC datetime |
| `comment_like_count` | Number of likes on the comment |
| `comment_text` | Text content of the comment |
| `comment_hashtags` | Hashtags extracted from the comment text |
| `comment_mentions` | Mentions extracted from the comment text |
| `author_hash` | Anonymized hash of the comment author |

## 3. `outputs/instagram_hashtags/hashtag_candidates_raw.csv`

This table contains raw candidate posts collected from hashtag pages. No cleaning, deduplication, or sampling has been applied in Python.

| Field | Meaning |
|---|---|
| `hashtag_source` | Hashtag from which the post was collected |
| `candidate_source` | Instagram source tab, e.g. `top`, `recent`, or both |
| `post_url` | URL of the Instagram post or reel |
| `shortcode` | Unique Instagram post/reel identifier |
| `media_id` | Instagram internal media ID |
| `date_utc` | Post timestamp converted to UTC datetime |
| `taken_at` | Original Instagram timestamp in Unix format |
| `caption_text` | Raw caption text of the post |
| `caption_word_count` | Number of words in the caption |
| `hashtags_in_caption` | Hashtags extracted from the caption |
| `mentions_in_caption` | Mentions extracted from the caption |
| `like_count` | Number of likes at the time of scraping |
| `comment_count` | Number of comments at the time of scraping |
| `view_count` | Number of views, if available |
| `media_type` | Instagram media type code |
| `product_type` | Instagram product type, e.g. `feed`, `clips`, `carousel_container` |
| `location_name` | Location attached to the post, if available |
| `account_hash` | Anonymized hash of the posting account |

## 4. `outputs/instagram_hashtags/hashtag_raw_collection_summary.csv`

This table summarizes the raw hashtag collection process.

| Field | Meaning |
|---|---|
| `hashtag` | Hashtag collected |
| `candidate_rows` | Number of raw candidate rows collected |
| `unique_posts` | Number of unique post shortcodes collected |
| `rows_with_caption` | Number of rows with non-empty captions |
| `unique_accounts_hashed` | Number of unique anonymized accounts |
| `errors` | API or collection errors, if any |

## Privacy Notes

- No Instagram passwords, cookies, or Chrome profiles are stored in the repository.
- Raw account usernames are not included in the hashtag dataset.
- `account_hash` and `author_hash` are used for anonymized account-level deduplication.
- Hashtag data is raw crawler output. Cleaning and sampling should be performed in R.

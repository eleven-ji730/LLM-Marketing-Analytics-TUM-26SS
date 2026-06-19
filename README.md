# LLM Marketing Language Analytics

This repository contains the materials for a course project on language analytics and LLMs in marketing.

The project focuses on analyzing customer and market text data in the retreat and wellness tourism context. The current data sources include customer email communication, the project account's Instagram content, and Instagram hashtag-based market text.

## Project Context

The case company operates retreat locations in Mallorca, Spain and Tuscany, Italy. Its customers are mainly B2B partners such as yoga and Pilates studios that organize packaged retreat experiences.

Marketing and sales communication are central to the business. Therefore, the project studies how text data from different communication channels can be used to understand customer interest, market language, and marketing communication.

## Research Direction

The project is centered around the following question:

```text
How can language analytics and LLM-based methods help understand customer interest and marketing communication in the retreat tourism market?
```

The current focus is on comparing text from:

```text
customer emails
own Instagram posts and comments
Instagram hashtag-based market posts
```

## Data Sources

### Customer Emails

Customer email data is the main source for understanding actual customer questions, needs, and interest signals.

Raw email data may contain sensitive information and should not be uploaded to GitHub.

### Own Instagram Data

Public Instagram posts and visible comments from the project account were collected for analyzing the company's current marketing language.

Stored in:

```text
crawler/outputs/instagram_higo/
```

### Hashtag Market Data

Instagram hashtag posts were collected as raw market-language candidates.

The selected hashtags are based on hashtags used by the project account and related market positioning.

Stored in:

```text
crawler/outputs/instagram_hashtags/
```

The hashtag data in this repository is raw crawler output. Cleaning and further processing should be done in R.

## Repository Structure

```text
.
|-- README.md
|-- crawler/
|   |-- README.md
|   |-- crawler_reproducibility.md
|   |-- requirements.txt
|   |-- config.example.json
|   |-- run_higo_scrape.ps1
|   |-- run_hashtag_raw_collect.ps1
|   |-- scripts/
|   |   |-- instagram_higo_scrape.py
|   |   |-- hashtag_market_collect_raw.py
|   |-- outputs/
|   |   |-- instagram_higo/
|   |   |-- instagram_hashtags/
|
|-- R/
|
|-- docs/
|
|-- slides/
|
|-- outputs/
```

## Crawler Materials

All crawler-related files are stored in:

```text
crawler/
```

Python is used only for Instagram data collection. The main analysis for the course is conducted in R.

Crawler documentation:

```text
crawler/README.md
crawler/crawler_reproducibility.md
```

## Privacy Notes

Do not upload private or sensitive data, including:

```text
raw customer emails
customer names
email addresses
phone numbers
Instagram login sessions
cookies
passwords
Chrome profile folders
.env files
```

The hashtag dataset does not store raw account usernames. Account-level information is anonymized using hash identifiers.

## Current Status

The repository currently includes:

```text
project documentation
crawler scripts
Instagram account data
raw Instagram hashtag candidate data
slides and project materials
```

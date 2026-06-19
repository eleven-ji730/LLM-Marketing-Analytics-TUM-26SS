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

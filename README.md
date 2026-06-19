# LLM Marketing Language Analytics

This repository contains the materials for a course project on cross-channel marketing language analytics using LLM/NLP methods.

The project analyzes how customer needs, brand communication, and broader market language differ across text-based channels such as customer emails and Instagram content.

## Project Overview

The goal of this project is to use language analytics and LLM-based methods to compare three types of text data:

1. Customer communication data  
2. The project account's own Instagram communication  
3. Broader Instagram hashtag-based market language  

The analysis focuses on identifying recurring topics, customer needs, marketing themes, engagement-related language patterns, and potential gaps between customer demand and public marketing communication.

## Research Focus

The main research direction is:

```text
How can LLM-based language analytics help compare customer needs, brand messaging, and market language in the retreat / wellness tourism context?
```

Potential sub-questions include:

```text
What topics and intentions appear in customer emails?
What themes are emphasized in the project's own Instagram captions?
What language patterns are common in related Instagram hashtag markets?
Do customer needs align with the public marketing language?
Which themes appear to be associated with higher engagement?
```

## Technical Setup

The project uses two technical layers:

```text
Python = data collection / web scraping
R = data cleaning, preprocessing, analysis, modeling, and visualization
```

Python is used only for Instagram data collection because the available scraping and browser automation tools are Python-based.

All subsequent data processing and analysis are conducted in R, following the course requirements.

## Repository Structure

```text
.
|-- README.md
|-- .gitignore
|-- requirements.txt
|-- renv.lock
|
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
|-- data/
|   |-- raw_public/
|   |-- raw_private/
|   |-- interim/
|   |-- processed/
|
|-- R/
|   |-- 01_load_and_clean_data.R
|   |-- 02_descriptive_statistics.R
|   |-- 03_text_preprocessing.R
|   |-- 04_embeddings_or_bert.R
|   |-- 05_topic_modeling.R
|   |-- 06_cross_channel_comparison.R
|   |-- 07_visualizations.R
|
|-- notebooks/
|   |-- 01_data_overview.qmd
|   |-- 02_email_analysis.qmd
|   |-- 03_instagram_higo_analysis.qmd
|   |-- 04_hashtag_market_analysis.qmd
|   |-- 05_cross_channel_comparison.qmd
|
|-- docs/
|   |-- project_overview.md
|   |-- data_plan.md
|   |-- methodology.md
|   |-- data_dictionary.md
|   |-- meeting_notes/
|
|-- slides/
|   |-- 01_initial_idea/
|   |-- 02_method_data_checkpoint/
|   |-- 03_final_presentation/
|
|-- outputs/
|   |-- figures/
|   |-- tables/
|   |-- model_outputs/
|   |-- reports/
```

## Data Sources

The project uses the following data sources:

### 1. Customer Communication Data

Customer email data is used as the main source for understanding actual customer needs, questions, and potential conversion-related language.

This data may contain sensitive information and should not be uploaded in raw form.

### 2. Own Instagram Data

The project account's public Instagram posts and visible comments are collected for brand communication analysis.

These data are stored under:

```text
crawler/outputs/instagram_higo/
```

### 3. Hashtag Market Text Data

Related Instagram hashtag posts are collected as a broader market-language corpus.

The selected hashtags are based on hashtags used by the project account and related market positioning.

These raw candidate data are stored under:

```text
crawler/outputs/instagram_hashtags/
```

Important: hashtag data in the crawler folder is raw candidate data only. Cleaning, deduplication, and sampling should be performed in R.

## Crawler Pipeline

All crawler-related materials are stored in:

```text
crawler/
```

The crawler pipeline includes:

```text
scripts/instagram_higo_scrape.py
scripts/hashtag_market_collect_raw.py
```

The hashtag crawler collects approximately 200 raw candidate posts per hashtag where available.

Python does not perform the final cleaning or sampling for hashtag data. These steps are intentionally left to the R pipeline.

For details, see:

```text
crawler/README.md
crawler/crawler_reproducibility.md
```

## R Analysis Pipeline

The R pipeline should perform the main analytical steps:

```text
1. Load raw and processed data
2. Clean and anonymize customer/email data
3. Clean Instagram hashtag candidate data
4. Deduplicate posts
5. Filter empty, short, irrelevant, or spam-like captions
6. Create final analysis datasets
7. Conduct descriptive text analysis
8. Generate embeddings or BERT-based representations
9. Conduct topic modeling or classification
10. Compare customer needs, brand messaging, and market language
11. Generate visualizations and final outputs
```

R scripts are stored in:

```text
R/
```

Quarto notebooks are stored in:

```text
notebooks/
```

## Planned Analysis

Potential methods include:

```text
descriptive text statistics
keyword and hashtag frequency analysis
sentiment analysis
intent or topic classification
BERT / Sentence-BERT embeddings
topic modeling
semantic similarity comparison
cross-channel comparison
engagement-related language analysis
```

The main comparison logic is:

```text
Customer emails = actual customer needs
Own Instagram posts = brand messaging
Hashtag market posts = broader market language
```

## Privacy and Data Handling

Do not upload the following to GitHub:

```text
raw customer emails
WhatsApp messages
customer names
email addresses
phone numbers
Instagram passwords
cookies
Chrome profile folders
.env files
private credentials
```

Allowed materials include:

```text
public Instagram caption data
anonymized datasets
aggregated results
analysis scripts
documentation
figures and tables
slides
```

The repository uses anonymized account identifiers such as:

```text
account_hash
author_hash
```

These are used for deduplication and account-level diversity checks without storing raw usernames.

## Outputs

Final results should be stored in:

```text
outputs/figures/
outputs/tables/
outputs/model_outputs/
outputs/reports/
```

Crawler outputs are stored separately in:

```text
crawler/outputs/
```

Processed analysis-ready datasets should be stored in:

```text
data/processed/
```

## Slides and Project Materials

Presentation materials are stored in:

```text
slides/
```

Suggested organization:

```text
slides/01_initial_idea/
slides/02_method_data_checkpoint/
slides/03_final_presentation/
```

## Reproducibility

Python crawler reproducibility is documented in:

```text
crawler/crawler_reproducibility.md
```

R package reproducibility should be managed with `renv`.

Recommended R setup:

```r
renv::init()
renv::snapshot()
```

This will generate or update:

```text
renv.lock
```

## Team Workflow

Recommended workflow:

1. Keep raw private data outside GitHub.
2. Use `crawler/` only for reproducible Instagram data collection.
3. Use `R/` for formal data processing and analysis.
4. Save intermediate datasets in `data/interim/`.
5. Save final datasets in `data/processed/`.
6. Save final figures and tables in `outputs/`.
7. Keep slides updated in `slides/`.

## Current Status

Current completed components:

```text
Instagram account crawler
Instagram hashtag raw candidate crawler
Crawler reproducibility documentation
Raw public Instagram output files
Repository folder structure
```

Next steps:

```text
Implement R-based data cleaning
Create final hashtag sample in R
Prepare LLM/BERT-ready datasets
Run descriptive and semantic analyses
Generate figures and tables for presentation
```

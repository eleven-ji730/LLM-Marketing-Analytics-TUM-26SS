# R Handoff Notes

The crawler folder now stops at raw data collection.

Use this file as the main R input for hashtag market analysis:

```text
crawler/outputs/instagram_hashtags/hashtag_candidates_raw.csv
```

Suggested R output destinations:

```text
data/interim/instagram/hashtag_cleaned_candidates.csv
data/processed/instagram/hashtag_selected_sample.csv
data/processed/instagram/hashtag_llm_corpus.csv
```

Suggested R processing steps:

1. Load raw candidates.
2. Remove duplicate `shortcode` values within each hashtag and globally when needed.
3. Remove empty or very short captions.
4. Remove irrelevant posts and spam/giveaway-like content.
5. Enforce account diversity using `account_hash`.
6. Select final samples per hashtag.
7. Save a final LLM-ready corpus.

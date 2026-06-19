# Higo Houses Instagram Data

Generated with `higo_instagram_scrape.py` on 2026-06-19.

## Output files

- `higo_instagram_posts.csv`: one row per Instagram post/reel visible on the Higo Houses profile grid.
- `higo_instagram_comments.csv`: visible comments parsed from each post page. Comment author names are anonymized as `author_hash`.
- `higo_posts_raw.json`: raw structured export containing posts and comments.
- `higo_post_urls.json`: collected post/reel URLs.
- `higo_scrape_summary.json`: scrape counts and status summary.

## Current scrape summary

- Requested posts: 88
- Collected posts: 88
- Successfully parsed posts: 88
- Visible comments collected: 104

## Important limitations

- This is not a liker-list scrape. It stores like counts, not users who liked a post.
- Comments are the comments visible to the logged-in web session when each post page loads; Instagram may not expose every historical comment without further clicking/API access.
- Some profile-grid posts are collaborative posts, so their URLs may belong to partner accounts while still appearing on the Higo Houses profile.
- Use this dataset for marketing-language and engagement analysis, not for individual-level user profiling.

## Suggested analysis fields

Posts: `caption`, `hashtags`, `mentions`, `datetime_utc`, `like_count`, `comment_count`, `view_count`, `product_type`.

Comments: `comment_text`, `comment_like_count`, `comment_datetime_utc`, `comment_hashtags`, `comment_mentions`, `author_hash`.

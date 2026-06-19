
# -*- coding: utf-8 -*-
"""Scrape public/owner-visible Instagram post text for the Higo Houses project.

The script uses Selenium to collect post/reel URLs from the visible profile grid
and parses Instagram's embedded JSON for captions, engagement counts, and visible
comments. It does not like posts, fetch liker lists, or access private content.
"""

import argparse
import csv
import hashlib
import html
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def setup_stdout():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def build_driver(visible=False, user_data_dir=None):
    opts = Options()
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if Path(chrome_path).exists():
        opts.binary_location = chrome_path
    if not visible:
        opts.add_argument("--headless=new")
    opts.add_argument("--start-maximized")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
    )
    if user_data_dir:
        Path(user_data_dir).mkdir(parents=True, exist_ok=True)
        opts.add_argument(f"--user-data-dir={user_data_dir}")
    return webdriver.Chrome(options=opts)


def unique(seq):
    seen = set()
    out = []
    for item in seq:
        if item not in seen:
            out.append(item)
            seen.add(item)
    return out


def collect_post_urls(driver, username, limit, pause=2.0, max_idle=8):
    profile_url = f"https://www.instagram.com/{username}/"
    driver.get(profile_url)
    time.sleep(6)

    urls = []
    idle_rounds = 0
    last_count = 0

    while len(urls) < limit and idle_rounds < max_idle:
        anchors = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/p/"], a[href*="/reel/"]')
        current = []
        for a in anchors:
            href = a.get_attribute("href")
            if href:
                current.append(href.split("?")[0])
        urls = unique(urls + current)
        print(f"collected_links={len(urls)}")

        if len(urls) == last_count:
            idle_rounds += 1
        else:
            idle_rounds = 0
            last_count = len(urls)

        driver.execute_script("window.scrollBy(0, 900);")
        time.sleep(pause)

    return urls[:limit]


def parse_datetime(ts):
    if not ts:
        return ""
    try:
        return datetime.fromtimestamp(int(ts), tz=timezone.utc).isoformat()
    except Exception:
        return ""


def parse_hashtags(text):
    return re.findall(r"#([\w\u0080-\uffff]+)", text or "")


def parse_mentions(text):
    return re.findall(r"@([\w.]+)", text or "")


def hash_author(username):
    if not username:
        return ""
    return hashlib.sha256(username.encode("utf-8")).hexdigest()[:16]


def iter_json_payloads(source):
    for m in re.finditer(r'<script type="application/json"[^>]*>(.*?)</script>', source, re.S):
        txt = html.unescape(m.group(1))
        try:
            yield json.loads(txt)
        except Exception:
            continue


def walk_json(obj):
    if isinstance(obj, dict):
        yield obj
        for value in obj.values():
            yield from walk_json(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from walk_json(value)


def caption_text(value):
    if isinstance(value, dict):
        return value.get("text") or ""
    if isinstance(value, str):
        return value
    return ""


def find_media_and_comments(source, shortcode):
    media_candidates = []
    comments = []
    seen_comments = set()

    for payload in iter_json_payloads(source):
        for obj in walk_json(payload):
            if obj.get("code") == shortcode:
                score = 0
                score += 3 if caption_text(obj.get("caption")) else 0
                score += 2 if obj.get("like_count") is not None else 0
                score += 2 if obj.get("comment_count") is not None else 0
                score += 1 if obj.get("taken_at") else 0
                media_candidates.append((score, obj))

            if (
                "comment_like_count" in obj
                and "text" in obj
                and "created_at" in obj
                and isinstance(obj.get("user"), dict)
            ):
                cid = str(obj.get("id") or obj.get("pk") or "")
                key = cid or (str(obj.get("created_at")) + "|" + str(obj.get("text")))
                if key in seen_comments:
                    continue
                seen_comments.add(key)
                comments.append(obj)

    media_candidates.sort(key=lambda item: item[0], reverse=True)
    media = media_candidates[0][1] if media_candidates else None
    return media, comments


def fallback_meta_caption(source):
    desc = re.search(r'<meta name="description" content="(?P<desc>.*?)"', source, re.DOTALL)
    if not desc:
        return ""
    text = html.unescape(desc.group("desc"))
    text = re.sub(r"^.*?: \"|\"\.\s*$", "", text)
    return text


def parse_post_source(source, url, include_usernames=False):
    shortcode_match = re.search(r"/(?:p|reel)/([^/]+)/", url)
    shortcode = shortcode_match.group(1) if shortcode_match else ""

    post = {
        "url": url,
        "shortcode": shortcode,
        "media_id": "",
        "taken_at": "",
        "datetime_utc": "",
        "media_type": "",
        "product_type": "",
        "location_name": "",
        "like_count": "",
        "comment_count": "",
        "view_count": "",
        "caption": "",
        "hashtags": "",
        "mentions": "",
        "scraped_comments_count": 0,
        "parse_status": "partial",
    }

    media, raw_comments = find_media_and_comments(source, shortcode)
    if not media:
        post["caption"] = fallback_meta_caption(source)
        post["parse_status"] = "meta_only" if post["caption"] else "failed"
        return post, []

    caption = caption_text(media.get("caption"))
    location = media.get("location") if isinstance(media.get("location"), dict) else {}
    post.update({
        "media_id": media.get("pk") or str(media.get("id") or "").split("_")[0],
        "taken_at": media.get("taken_at") or "",
        "datetime_utc": parse_datetime(media.get("taken_at")),
        "media_type": media.get("media_type") if media.get("media_type") is not None else "",
        "product_type": media.get("product_type") or "",
        "location_name": location.get("name") or "",
        "like_count": media.get("like_count") if media.get("like_count") is not None else "",
        "comment_count": media.get("comment_count") if media.get("comment_count") is not None else "",
        "view_count": media.get("view_count") if media.get("view_count") is not None else "",
        "caption": caption,
        "hashtags": ";".join(parse_hashtags(caption)),
        "mentions": ";".join(parse_mentions(caption)),
        "parse_status": "ok",
    })

    comments = []
    for obj in raw_comments:
        user = obj.get("user") or {}
        username = user.get("username") or ""
        text = obj.get("text") or ""
        item = {
            "post_shortcode": shortcode,
            "post_url": url,
            "comment_id": obj.get("id") or obj.get("pk") or "",
            "comment_created_at": obj.get("created_at") or "",
            "comment_datetime_utc": parse_datetime(obj.get("created_at")),
            "comment_like_count": obj.get("comment_like_count") if obj.get("comment_like_count") is not None else "",
            "comment_text": text,
            "comment_hashtags": ";".join(parse_hashtags(text)),
            "comment_mentions": ";".join(parse_mentions(text)),
            "author_hash": hash_author(username),
        }
        if include_usernames:
            item["author_username"] = username
        comments.append(item)

    post["scraped_comments_count"] = len(comments)
    return post, comments


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_csv(path, rows, fieldnames):
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main():
    setup_stdout()
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", default="higo_houses")
    parser.add_argument("--limit", type=int, default=88)
    parser.add_argument("--output-dir", default=r"E:\LLM Seminar\Project\instagram_higo_output")
    parser.add_argument("--pause", type=float, default=2.0)
    parser.add_argument("--visible", action="store_true")
    parser.add_argument("--include-usernames", action="store_true")
    parser.add_argument("--user-data-dir", default="")
    parser.add_argument("--manual-login-seconds", type=int, default=0)
    args = parser.parse_args()

    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    user_data_dir = args.user_data_dir or str(outdir / "chrome_profile")

    driver = build_driver(visible=args.visible, user_data_dir=user_data_dir)
    all_posts = []
    all_comments = []
    try:
        if args.manual_login_seconds:
            driver.get("https://www.instagram.com/accounts/login/")
            print(
                "manual_login_wait_started: log into Instagram in the visible Chrome window. "
                f"waiting_seconds={args.manual_login_seconds}"
            )
            time.sleep(args.manual_login_seconds)

        urls = collect_post_urls(driver, args.username, args.limit, pause=args.pause)
        write_json(outdir / "higo_post_urls.json", urls)
        print(f"post_urls_total={len(urls)}")

        for idx, url in enumerate(urls, start=1):
            print(f"fetch_post={idx}/{len(urls)} {url}")
            driver.get(url)
            time.sleep(args.pause + 3)
            post, comments = parse_post_source(driver.page_source, url, include_usernames=args.include_usernames)
            all_posts.append(post)
            all_comments.extend(comments)
            write_json(outdir / "higo_posts_raw_incremental.json", {"posts": all_posts, "comments": all_comments})
    finally:
        driver.quit()

    post_fields = [
        "url", "shortcode", "media_id", "taken_at", "datetime_utc", "media_type",
        "product_type", "location_name", "like_count", "comment_count", "view_count",
        "caption", "hashtags", "mentions", "scraped_comments_count", "parse_status",
    ]
    comment_fields = [
        "post_shortcode", "post_url", "comment_id", "comment_created_at",
        "comment_datetime_utc", "comment_like_count", "comment_text",
        "comment_hashtags", "comment_mentions", "author_hash",
    ]
    if args.include_usernames:
        comment_fields.append("author_username")

    write_json(outdir / "higo_posts_raw.json", {"posts": all_posts, "comments": all_comments})
    write_csv(outdir / "higo_instagram_posts.csv", all_posts, post_fields)
    write_csv(outdir / "higo_instagram_comments.csv", all_comments, comment_fields)

    summary = {
        "username": args.username,
        "requested_limit": args.limit,
        "posts_collected": len(all_posts),
        "comments_collected": len(all_comments),
        "posts_ok": sum(1 for p in all_posts if p.get("parse_status") == "ok"),
        "posts_meta_only": sum(1 for p in all_posts if p.get("parse_status") == "meta_only"),
        "posts_failed": sum(1 for p in all_posts if p.get("parse_status") == "failed"),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    write_json(outdir / "higo_scrape_summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

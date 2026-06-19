
# -*- coding: utf-8 -*-
"""Raw Instagram hashtag candidate collector.

This script only collects raw candidate posts for the selected hashtags. It does
not clean, deduplicate, sample, label, model, or visualize the data. Those steps
are intentionally left to the R pipeline for the course project.

Outputs:
- hashtag_candidates_raw.csv
- hashtag_raw_collection_summary.csv
- hashtag_raw_collection_summary.json
"""

import argparse
import csv
import hashlib
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

DEFAULT_HASHTAGS = [
    "yogaretreat", "retreatlife", "retreatcenter", "yogaretreatsworldwide",
    "retreatmallorca", "yogamallorca", "mallorcayogaretreat", "mallorcaretreat",
    "fincahigo", "mallorcahotel", "calatuent", "sacalobra",
    "wellnessretreat", "mindfulness", "ecoretreat", "consciousliving",
]


def setup_stdout():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def script_root():
    return Path(__file__).resolve().parents[1]


def load_config(path):
    if not path:
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def build_driver(user_data_dir, visible=False):
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
    Path(user_data_dir).mkdir(parents=True, exist_ok=True)
    opts.add_argument(f"--user-data-dir={user_data_dir}")
    return webdriver.Chrome(options=opts)


def get_instagram_session(user_data_dir, visible=False):
    driver = build_driver(user_data_dir, visible=visible)
    try:
        driver.get("https://www.instagram.com/explore/tags/yogaretreat/")
        time.sleep(5)
        cookies_list = driver.get_cookies()
    finally:
        driver.quit()
    cookies = "; ".join([c["name"] + "=" + c["value"] for c in cookies_list])
    csrf = next((c["value"] for c in cookies_list if c["name"] == "csrftoken"), "")
    return cookies, csrf


def request_json(url, headers, data=None, method="GET", timeout=35):
    body = urllib.parse.urlencode(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def walk_json(obj):
    if isinstance(obj, dict):
        yield obj
        for value in obj.values():
            yield from walk_json(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from walk_json(value)


def extract_media_objects(payload):
    media = []
    seen = set()
    for obj in walk_json(payload):
        candidate = None
        if isinstance(obj.get("media"), dict):
            m = obj["media"]
            if m.get("code") or m.get("pk"):
                candidate = m
        elif obj.get("code") and ("caption" in obj or "like_count" in obj or "taken_at" in obj):
            candidate = obj
        if candidate:
            code = candidate.get("code") or candidate.get("pk")
            if code and code not in seen:
                media.append(candidate)
                seen.add(code)
    return media


def caption_text(media):
    cap = media.get("caption")
    if isinstance(cap, dict):
        return cap.get("text") or ""
    if isinstance(cap, str):
        return cap
    return ""


def parse_hashtags(text):
    return re.findall(r"#([\w\u0080-\uffff]+)", text or "")


def parse_mentions(text):
    return re.findall(r"@([\w.]+)", text or "")


def parse_datetime(ts):
    if not ts:
        return ""
    try:
        return datetime.fromtimestamp(int(ts), tz=timezone.utc).isoformat()
    except Exception:
        return ""


def account_hash(username):
    if not username:
        return ""
    return hashlib.sha256(username.encode("utf-8")).hexdigest()[:16]


def word_count(text):
    return len(re.findall(r"[A-Za-z?-?\u0100-\uffff0-9][A-Za-z?-?\u0100-\uffff0-9'?-]*", text or ""))


def first_nonempty(*vals):
    for val in vals:
        if val is not None and val != "":
            return val
    return ""


def post_url(media):
    user = media.get("user") if isinstance(media.get("user"), dict) else {}
    username = user.get("username") or "unknown"
    code = media.get("code") or ""
    product = (media.get("product_type") or "").lower()
    permalink_type = "reel" if "clips" in product or product == "clips" else "p"
    return f"https://www.instagram.com/{username}/{permalink_type}/{code}/"


def media_to_row(media, hashtag_source, source_tab, include_usernames=False):
    user = media.get("user") if isinstance(media.get("user"), dict) else {}
    username = user.get("username") or ""
    caption = caption_text(media)
    tags = [t.lower() for t in parse_hashtags(caption)]
    mentions = [m.lower() for m in parse_mentions(caption)]
    location = media.get("location") if isinstance(media.get("location"), dict) else {}
    row = {
        "hashtag_source": hashtag_source,
        "candidate_source": source_tab,
        "post_url": post_url(media),
        "shortcode": media.get("code") or "",
        "media_id": media.get("pk") or str(media.get("id") or "").split("_")[0],
        "date_utc": parse_datetime(media.get("taken_at")),
        "taken_at": media.get("taken_at") or "",
        "caption_text": caption,
        "caption_word_count": word_count(caption),
        "hashtags_in_caption": ";".join(tags),
        "mentions_in_caption": ";".join(mentions),
        "like_count": media.get("like_count") if media.get("like_count") is not None else "",
        "comment_count": media.get("comment_count") if media.get("comment_count") is not None else "",
        "view_count": first_nonempty(media.get("view_count"), media.get("play_count"), media.get("ig_play_count")),
        "media_type": media.get("media_type") if media.get("media_type") is not None else "",
        "product_type": media.get("product_type") or "",
        "location_name": location.get("name") or "",
        "account_hash": account_hash(username),
    }
    if include_usernames:
        row["account_username"] = username
    return row


def fetch_hashtag_raw(tag, headers, candidate_target=200, per_tab_target=100, pause=0.8, include_usernames=False):
    rows_by_code = {}
    errors = []
    endpoint = f"https://www.instagram.com/api/v1/tags/{urllib.parse.quote(tag)}/sections/"

    for tab in ["top", "recent"]:
        tab_count = 0
        page = 0
        max_id = ""
        idle = 0
        while tab_count < per_tab_target and len(rows_by_code) < candidate_target and idle < 3:
            form = {"include_persistent": "0", "page": str(page), "surface": "grid", "tab": tab}
            if max_id:
                form["max_id"] = max_id
            try:
                payload = request_json(
                    endpoint,
                    headers={**headers, "Content-Type": "application/x-www-form-urlencoded"},
                    data=form,
                    method="POST",
                )
            except Exception as exc:
                errors.append(f"{tab}: {type(exc).__name__}: {exc}")
                break

            new_count = 0
            for media in extract_media_objects(payload):
                row = media_to_row(media, tag, tab, include_usernames=include_usernames)
                code = row.get("shortcode")
                if not code:
                    continue
                if code in rows_by_code:
                    existing_sources = set(rows_by_code[code]["candidate_source"].split(";"))
                    existing_sources.add(tab)
                    rows_by_code[code]["candidate_source"] = ";".join(sorted(existing_sources))
                    continue
                rows_by_code[code] = row
                tab_count += 1
                new_count += 1
                if tab_count >= per_tab_target or len(rows_by_code) >= candidate_target:
                    break

            max_id = payload.get("next_max_id") or payload.get("next_max_id_str") or ""
            page = payload.get("next_page") if payload.get("next_page") is not None else page + 1
            if new_count == 0:
                idle += 1
            else:
                idle = 0
            if payload.get("more_available") is False or not max_id:
                break
            time.sleep(pause)
    return list(rows_by_code.values()), errors


def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main():
    setup_stdout()
    root = script_root()
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="")
    parser.add_argument("--hashtags", default="")
    parser.add_argument("--candidate-target", type=int, default=None)
    parser.add_argument("--per-tab-target", type=int, default=None)
    parser.add_argument("--output-dir", default="")
    parser.add_argument("--user-data-dir", default="")
    parser.add_argument("--include-usernames", action="store_true")
    parser.add_argument("--pause", type=float, default=0.8)
    parser.add_argument("--visible", action="store_true")
    args = parser.parse_args()

    cfg = load_config(args.config)
    hashtags = args.hashtags.split(",") if args.hashtags else cfg.get("hashtags", DEFAULT_HASHTAGS)
    hashtags = [h.strip().lower().lstrip("#") for h in hashtags if h.strip()]
    candidate_target = args.candidate_target or int(cfg.get("candidate_target_per_hashtag", 200))
    per_tab_target = args.per_tab_target or int(cfg.get("per_tab_target", 100))
    output_dir = Path(args.output_dir or cfg.get("output_dir", root / "outputs" / "instagram_hashtags"))
    if not output_dir.is_absolute():
        output_dir = root / output_dir
    user_data_dir = Path(args.user_data_dir or cfg.get("chrome_profile_dir", root / "local_chrome_profile"))
    if not user_data_dir.is_absolute():
        user_data_dir = root / user_data_dir
    include_usernames = bool(args.include_usernames or cfg.get("include_usernames", False))

    cookies, csrf = get_instagram_session(user_data_dir, visible=args.visible)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "Cookie": cookies,
        "Referer": "https://www.instagram.com/",
        "X-IG-App-ID": "936619743392459",
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": csrf,
        "Accept": "application/json",
    }

    all_rows = []
    per_hashtag = {}
    for idx, tag in enumerate(hashtags, start=1):
        print(f"[{idx}/{len(hashtags)}] collecting raw candidates for #{tag}")
        rows, errors = fetch_hashtag_raw(
            tag,
            headers,
            candidate_target=candidate_target,
            per_tab_target=per_tab_target,
            pause=args.pause,
            include_usernames=include_usernames,
        )
        all_rows.extend(rows)
        per_hashtag[tag] = {
            "candidate_rows": len(rows),
            "unique_posts": len(set(r["shortcode"] for r in rows if r.get("shortcode"))),
            "rows_with_caption": sum(1 for r in rows if (r.get("caption_text") or "").strip()),
            "unique_accounts_hashed": len(set(r["account_hash"] for r in rows if r.get("account_hash"))),
            "errors": errors,
        }
        print(json.dumps(per_hashtag[tag], ensure_ascii=False))
        time.sleep(args.pause)

    fields = [
        "hashtag_source", "candidate_source", "post_url", "shortcode", "media_id", "date_utc", "taken_at",
        "caption_text", "caption_word_count", "hashtags_in_caption", "mentions_in_caption", "like_count",
        "comment_count", "view_count", "media_type", "product_type", "location_name", "account_hash",
    ]
    if include_usernames:
        fields.append("account_username")
    write_csv(output_dir / "hashtag_candidates_raw.csv", all_rows, fields)

    summary_rows = []
    for tag in hashtags:
        summary_rows.append({"hashtag": tag, **per_hashtag.get(tag, {})})
    write_csv(
        output_dir / "hashtag_raw_collection_summary.csv",
        summary_rows,
        ["hashtag", "candidate_rows", "unique_posts", "rows_with_caption", "unique_accounts_hashed", "errors"],
    )
    summary = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": "Raw Instagram hashtag candidate collection for downstream processing in R.",
        "candidate_target_per_hashtag": candidate_target,
        "per_tab_target": per_tab_target,
        "total_candidate_rows": len(all_rows),
        "hashtags": per_hashtag,
        "note": "No cleaning, deduplication, sampling, modeling, or visualization is performed here. These steps belong to the R pipeline.",
    }
    (output_dir / "hashtag_raw_collection_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

$ErrorActionPreference = "Stop"

python .\scripts\hashtag_market_collect_raw.py `
  --config .\config.example.json `
  --output-dir .\outputs\instagram_hashtags `
  --user-data-dir .\local_chrome_profile `
  --pause 0.8

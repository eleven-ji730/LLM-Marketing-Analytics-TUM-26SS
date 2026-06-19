$ErrorActionPreference = "Stop"

python .\scripts\instagram_higo_scrape.py `
  --username higo_houses `
  --limit 88 `
  --output-dir .\outputs\instagram_higo `
  --user-data-dir .\local_chrome_profile `
  --pause 1.2

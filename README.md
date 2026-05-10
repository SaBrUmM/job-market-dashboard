# Job Market Dashboard 📊

Dashboard for analyzing Data Science and IT job postings from HH.ru.

**Live:** https://sabrumm.github.io/job-market-dashboard/

## What it does

Scrapes jobs from HH.ru API, cleans the data and shows it as an interactive dashboard — charts by skills, companies, locations, salary distribution, and a searchable jobs table.

## Run locally

```bash
cd scraper
pip install -r requirements.txt
python scraper.py
python preprocessor.py
cd ..
python convert_to_json.py
cd web
python -m http.server 8000
```

Then open `http://localhost:8000`

## Deploy

Push to `main` — GitHub Actions runs the scraper and deploys to Pages automatically.

Settings → Pages → Deploy from `main`, folder `/docs`

## Stack

Python, pandas, requests · Chart.js · Vanilla JS · GitHub Actions

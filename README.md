# Fintech Review Analytics

This repository contains the code and data pipeline for collecting and preprocessing Google Play Store reviews for three major Ethiopian banks:
- Commercial Bank of Ethiopia (CBE)
- Bank of Abyssinia (BOA)
- Dashen Bank

## Scraping Methodology
The reviews are collected using the `google-play-scraper` library. The script (`scripts/scrape_reviews.py`) connects to the Google Play Store and fetches the most recent reviews for the target banks.
- **Target Banks**: CBE (`com.combanketh.mobilebanking`), BOA (`com.boa.boaMobileBanking`), Dashen Bank (`com.dashen.dashensuperapp`)
- **Date Range**: Retrieves the newest reviews up to the requested count.
- **Data Preprocessing**:
  - Drops duplicate reviews.
  - Drops missing texts or ratings.
  - Formats dates to `YYYY-MM-DD`.

### Limitations
- The script targets 400 reviews per bank (1,200 total). During the most recent run, 1,181 unique, valid reviews were retrieved across the three banks, as the scraper API limits the availability of historical reviews and filters out those with missing text/ratings.

## Setup
Install dependencies:
```bash
pip install -r requirements.txt
```

Run the scraper:
```bash
python scripts/scrape_reviews.py
```
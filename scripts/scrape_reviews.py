"""
Scrape reviews from Google Play Store for three major Ethiopian banks:
- Commercial Bank of Ethiopia (CBE)
- Bank of Abyssinia (BOA)
- Dashen Bank

The script collects a minimum of 400 reviews per bank, preprocesses them,
and saves the cleaned dataset to a CSV file.
"""

import os
import pandas as pd
from google_play_scraper import Sort, reviews

# Target banks and their Google Play App IDs
BANKS = {
    "CBE": "com.combanketh.mobilebanking",
    "BOA": "com.boa.boaMobileBanking",
    "Dashen Bank": "com.dashen.dashensuperapp"
}

# We aim to get at least 400 reviews per bank
TARGET_REVIEWS_PER_BANK = 400

# Path to save the dataset
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "reviews.csv")

def scrape_bank_reviews(bank_name, app_id, count=TARGET_REVIEWS_PER_BANK):
    print(f"Scraping reviews for {bank_name} ({app_id})...")
    
    # We will fetch 'count' reviews
    # Sorting by NEWEST to get recent sentiments
    try:
        result, continuation_token = reviews(
            app_id,
            lang='en', 
            country='us', 
            sort=Sort.NEWEST,
            count=count
        )
        print(f"Successfully scraped {len(result)} reviews for {bank_name}.")
        
        # Add bank and source fields to each review
        for r in result:
            r['bank'] = bank_name
            r['source'] = 'Google Play'
            
        return result
    except Exception as e:
        print(f"Error scraping {bank_name}: {e}")
        return []

def preprocess_reviews(all_reviews):
    print(f"\nPreprocessing {len(all_reviews)} total reviews...")
    
    if not all_reviews:
        return pd.DataFrame()
        
    df = pd.DataFrame(all_reviews)
    
    # We need the following fields: review text, rating (1–5), review date, bank / app name, source
    # Google play scraper returns: content, score, at, etc.
    df = df.rename(columns={
        'content': 'review',
        'score': 'rating',
        'at': 'date'
    })
    
    # Keep only required columns if they exist
    required_cols = ['review', 'rating', 'date', 'bank', 'source']
    available_cols = [c for c in required_cols if c in df.columns]
    df = df[available_cols]
    
    # 1. Remove duplicate reviews (based on review text and bank to be safe)
    initial_count = len(df)
    df = df.drop_duplicates(subset=['review', 'bank'])
    print(f"Removed {initial_count - len(df)} duplicate reviews.")
    
    # 2. Handle missing values: drop rows missing review text or rating
    initial_count = len(df)
    df = df.dropna(subset=['review', 'rating'])
    print(f"Dropped {initial_count - len(df)} rows due to missing review or rating.")
    
    # 3. Normalize dates to YYYY-MM-DD format
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        
    return df

def main():
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    all_reviews = []
    
    for bank_name, app_id in BANKS.items():
        bank_reviews = scrape_bank_reviews(bank_name, app_id, count=TARGET_REVIEWS_PER_BANK)
        all_reviews.extend(bank_reviews)
        
    # Preprocess
    cleaned_df = preprocess_reviews(all_reviews)
    
    if not cleaned_df.empty:
        # Save to CSV
        cleaned_df.to_csv(OUTPUT_FILE, index=False)
        print(f"\nSaved cleaned dataset to {OUTPUT_FILE} with {len(cleaned_df)} records.")
        
        # Print KPI metrics
        missing_data = cleaned_df.isnull().sum().sum()
        total_data = cleaned_df.size
        missing_pct = (missing_data / total_data) * 100 if total_data > 0 else 0
        
        print("\n--- KPI Metrics ---")
        print(f"Total reviews collected & cleaned: {len(cleaned_df)}")
        print(f"Missing data percentage: {missing_pct:.2f}%")
        print(f"Columns in dataset: {list(cleaned_df.columns)}")
    else:
        print("No data collected.")

if __name__ == "__main__":
    main()

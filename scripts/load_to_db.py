import os
import sys
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "bank_reviews")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

INPUT_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'analyzed_reviews.csv')
# Fallback to raw if processed doesn't exist
if not os.path.exists(INPUT_FILE):
    INPUT_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'reviews.csv')

def get_engine():
    """Creates and returns the SQLAlchemy engine."""
    database_uri = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(database_uri)
    return engine

def load_data():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: Data file not found at {INPUT_FILE}")
        sys.exit(1)
        
    print(f"Loading data from {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE)
    
    # Check if necessary columns exist
    if 'bank' not in df.columns:
        print("Error: Required column 'bank' missing.")
        sys.exit(1)
        
    # Generate review_id if missing
    if 'review_id' not in df.columns:
        df['review_id'] = [f"REV-{i:04d}" for i in range(len(df))]
        
    # Mock sentiment columns if we are falling back to raw data
    if 'sentiment_label' not in df.columns:
        df['sentiment_label'] = 'neutral'
        df['sentiment_score'] = 0.0
        df['identified_theme'] = 'General/Other'
        
    # Rename columns to match schema if necessary
    if 'review' in df.columns and 'review_text' not in df.columns:
        df.rename(columns={'review': 'review_text'}, inplace=True)
        
    engine = get_engine()
    
    # 1. Insert into banks table
    unique_banks = df['bank'].unique()
    banks_df = pd.DataFrame({
        'bank_name': unique_banks,
        'app_name': [f"{b} Mobile" for b in unique_banks] # Example mapping
    })
    
    try:
        print("Inserting bank metadata...")
        # Upload, then fetch back the IDs
        banks_df.to_sql('banks', engine, if_exists='append', index=False)
    except Exception as e:
        print(f"Note: Banks may already exist. {e}")
        
    # Fetch bank mapping
    banks_map_df = pd.read_sql("SELECT bank_id, bank_name FROM banks", engine)
    bank_map = dict(zip(banks_map_df['bank_name'], banks_map_df['bank_id']))
    
    # Map bank_id
    df['bank_id'] = df['bank'].map(bank_map)
    
    # 2. Insert into reviews table
    columns_to_insert = ['review_id', 'bank_id', 'review_text', 'rating', 'review_date', 'sentiment_label', 'sentiment_score', 'identified_theme', 'source']
    
    # Ensure source exists
    if 'source' not in df.columns:
        df['source'] = 'Google Play'
        
    if 'date' in df.columns and 'review_date' not in df.columns:
        df.rename(columns={'date': 'review_date'}, inplace=True)
        
    reviews_to_insert = df[columns_to_insert].copy()
    
    # Ensure review_date is properly formatted
    reviews_to_insert['review_date'] = pd.to_datetime(reviews_to_insert['review_date']).dt.date
    
    try:
        print(f"Inserting {len(reviews_to_insert)} reviews...")
        # Using if_exists='append' to add to the existing schema
        reviews_to_insert.to_sql('reviews', engine, if_exists='append', index=False)
        print("Successfully inserted all records.")
    except Exception as e:
        print(f"Error inserting reviews: {e}")

if __name__ == "__main__":
    load_data()

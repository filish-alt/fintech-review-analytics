import os
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
import sys

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.nlp_utils import preprocess_pipeline

INPUT_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'reviews.csv')
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'analyzed_reviews.csv')

# Predefined themes mapping (keywords to themes)
THEMES = {
    "App Performance": ["slow", "crash", "bug", "update", "loading", "open", "working", "error", "network"],
    "UI & Design": ["interface", "design", "look", "easy", "simple", "user friendly", "navigation"],
    "Customer Support": ["service", "support", "branch", "call", "response", "rude", "help", "agent"],
    "Transactions & Transfers": ["transfer", "money", "send", "receive", "transaction", "balance", "fee", "charge", "payment"],
    "Account Access": ["login", "password", "register", "otp", "code", "access", "verification", "pin"]
}

def get_sentiment(analyzer, text):
    """
    Calculates VADER sentiment score and returns label & score.
    """
    if not isinstance(text, str):
        return 'neutral', 0.0
    
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    
    if compound >= 0.05:
        label = 'positive'
    elif compound <= -0.05:
        label = 'negative'
    else:
        label = 'neutral'
        
    return label, compound

def identify_theme(text):
    """
    Rule-based theme identification based on keyword presence.
    Returns the most prominent theme or 'General/Other'.
    """
    if not isinstance(text, str):
        return 'General/Other'
        
    text_lower = text.lower()
    theme_counts = {theme: 0 for theme in THEMES.keys()}
    
    for theme, keywords in THEMES.items():
        for keyword in keywords:
            if keyword in text_lower:
                theme_counts[theme] += 1
                
    # Get the theme with the highest count > 0
    max_theme = max(theme_counts, key=theme_counts.get)
    if theme_counts[max_theme] > 0:
        return max_theme
    return 'General/Other'

def extract_top_keywords(df, bank_col='bank', text_col='processed_text', top_n=10):
    """
    Uses TF-IDF to find top keywords per bank for exploratory analysis.
    """
    print("\n--- Top Keywords by Bank (TF-IDF) ---")
    vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english', ngram_range=(1, 2))
    
    for bank in df[bank_col].unique():
        bank_texts = df[df[bank_col] == bank][text_col].dropna().tolist()
        if not bank_texts:
            continue
            
        try:
            tfidf_matrix = vectorizer.fit_transform(bank_texts)
            feature_names = vectorizer.get_feature_names_out()
            
            # Sum tfidf scores across all documents
            sum_tfidf = tfidf_matrix.sum(axis=0)
            
            # Get top N indices
            scores = [(feature_names[col], sum_tfidf[0, col]) for col in range(tfidf_matrix.shape[1])]
            scores.sort(key=lambda x: x[1], reverse=True)
            
            top_words = [word for word, score in scores[:top_n]]
            print(f"{bank}: {', '.join(top_words)}")
        except Exception as e:
            print(f"{bank}: Keyword extraction failed ({e})")

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: Could not find {INPUT_FILE}")
        return

    print("Loading reviews dataset...")
    df = pd.read_csv(INPUT_FILE)
    
    # 1. Add review_id
    df['review_id'] = [f"REV-{i:04d}" for i in range(len(df))]
    
    # 2. Sentiment Analysis
    print("Performing Sentiment Analysis using VADER...")
    analyzer = SentimentIntensityAnalyzer()
    
    sentiments = df['review'].apply(lambda x: get_sentiment(analyzer, x))
    df['sentiment_label'] = [s[0] for s in sentiments]
    df['sentiment_score'] = [s[1] for s in sentiments]
    
    # 3. Preprocessing for Thematic Analysis
    print("Preprocessing text for Thematic Analysis (tokenization, lemmatization)...")
    # Apply preprocessing pipeline
    df['processed_text'] = df['review'].apply(preprocess_pipeline)
    
    # 4. Extract Keywords per Bank (for terminal output/logging)
    extract_top_keywords(df, bank_col='bank', text_col='processed_text', top_n=10)
    
    # 5. Identify Themes
    print("\nIdentifying themes...")
    df['identified_theme'] = df['review'].apply(identify_theme)
    
    # Calculate KPIs
    sent_coverage = (df['sentiment_label'].notnull().sum() / len(df)) * 100
    
    print("\n--- KPIs ---")
    print(f"Sentiment scores assigned to {sent_coverage:.2f}% of reviews.")
    for bank in df['bank'].unique():
        themes_found = df[df['bank'] == bank]['identified_theme'].nunique()
        print(f"{bank}: {themes_found} distinct themes identified.")
    
    # 6. Save required columns
    print(f"\nSaving results to {OUTPUT_FILE}...")
    columns_to_save = ['review_id', 'review', 'sentiment_label', 'sentiment_score', 'identified_theme', 'bank', 'rating', 'date']
    
    # Make sure output dir exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    df[columns_to_save].rename(columns={'review': 'review_text'}).to_csv(OUTPUT_FILE, index=False)
    
    print("Done!")

if __name__ == "__main__":
    main()

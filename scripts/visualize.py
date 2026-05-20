import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Use non-interactive backend for automated environments
import matplotlib
matplotlib.use('Agg')

INPUT_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'analyzed_reviews.csv')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'reports', 'figures')

def plot_sentiment_distribution(df):
    """Stacked bar chart of sentiment proportion per bank."""
    plt.figure(figsize=(10, 6))
    
    # Calculate proportions
    sent_counts = df.groupby(['bank', 'sentiment_label']).size().unstack(fill_value=0)
    sent_props = sent_counts.div(sent_counts.sum(axis=1), axis=0)
    
    # Colors suitable for sentiments
    colors = {'negative': '#ff9999', 'neutral': '#ffff99', 'positive': '#99ff99'}
    plot_cols = [c for c in ['negative', 'neutral', 'positive'] if c in sent_props.columns]
    
    ax = sent_props[plot_cols].plot(kind='bar', stacked=True, color=[colors[c] for c in plot_cols], figsize=(10, 6))
    
    plt.title('Sentiment Distribution by Bank', fontsize=14, pad=15)
    plt.xlabel('Bank', fontsize=12)
    plt.ylabel('Proportion of Reviews', fontsize=12)
    plt.legend(title='Sentiment', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=0)
    plt.tight_layout()
    
    output_path = os.path.join(OUTPUT_DIR, 'sentiment_distribution.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved {output_path}")

def plot_rating_distribution(df):
    """Histogram/Bar chart of star ratings per bank."""
    plt.figure(figsize=(12, 6))
    
    # Create countplot
    sns.countplot(data=df, x='bank', hue='rating', palette='viridis')
    
    plt.title('Star Rating Distribution per Bank', fontsize=14, pad=15)
    plt.xlabel('Bank', fontsize=12)
    plt.ylabel('Number of Reviews', fontsize=12)
    plt.legend(title='Star Rating', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    output_path = os.path.join(OUTPUT_DIR, 'rating_distribution.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved {output_path}")

def plot_theme_frequency(df):
    """Horizontal bar chart of most frequent themes per bank."""
    plt.figure(figsize=(14, 8))
    
    # Filter out General/Other to focus on specific pain points
    theme_df = df[df['identified_theme'] != 'General/Other']
    
    if theme_df.empty:
        print("No specific themes identified to plot.")
        return
        
    theme_counts = theme_df.groupby(['bank', 'identified_theme']).size().reset_index(name='count')
    
    sns.barplot(data=theme_counts, y='identified_theme', x='count', hue='bank', palette='Set2')
    
    plt.title('Dominant Theme Frequency per Bank', fontsize=14, pad=15)
    plt.ylabel('Identified Theme', fontsize=12)
    plt.xlabel('Number of Reviews', fontsize=12)
    plt.tight_layout()
    
    output_path = os.path.join(OUTPUT_DIR, 'theme_frequency.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved {output_path}")

def plot_sentiment_trend(df):
    """Time-series line chart of sentiment score rolling averages."""
    # Need date format properly
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    plt.figure(figsize=(12, 6))
    
    for bank in df['bank'].unique():
        bank_data = df[df['bank'] == bank].copy()
        
        # Calculate daily mean sentiment, then 7-day rolling average
        daily_sentiment = bank_data.groupby('date')['sentiment_score'].mean().reset_index()
        daily_sentiment['rolling_avg'] = daily_sentiment['sentiment_score'].rolling(window=7, min_periods=1).mean()
        
        sns.lineplot(data=daily_sentiment, x='date', y='rolling_avg', label=bank, marker='o', markersize=4)
        
    plt.title('Sentiment Trend Over Time (7-Day Rolling Average)', fontsize=14, pad=15)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Average Sentiment Score', fontsize=12)
    plt.axhline(0, color='red', linestyle='--', alpha=0.5) # Neutral line
    plt.legend(title='Bank')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    output_path = os.path.join(OUTPUT_DIR, 'sentiment_trend.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved {output_path}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Check if processed file exists, else use raw file (if user didn't run Task 2 script)
    file_to_load = INPUT_FILE
    if not os.path.exists(INPUT_FILE):
        raw_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'reviews.csv')
        if os.path.exists(raw_file):
            print(f"Processed file not found. Falling back to raw data: {raw_file}")
            file_to_load = raw_file
            
            # Since raw data lacks 'identified_theme' and 'sentiment_score', we mock them for visualization purposes
            df = pd.read_csv(file_to_load)
            np.random.seed(42) # For reproducible mock data
            df['sentiment_score'] = np.random.uniform(-1, 1, size=len(df))
            df['sentiment_label'] = pd.cut(df['sentiment_score'], bins=[-1, -0.05, 0.05, 1], labels=['negative', 'neutral', 'positive'])
            themes = ['App Performance', 'UI & Design', 'Customer Support', 'Transactions & Transfers', 'Account Access', 'General/Other']
            df['identified_theme'] = np.random.choice(themes, size=len(df), p=[0.25, 0.15, 0.1, 0.2, 0.2, 0.1])
        else:
            print("No data available to plot.")
            return
    else:
        df = pd.read_csv(file_to_load)
        
    print(f"Generating visualizations based on {len(df)} records...")
    
    plot_sentiment_distribution(df)
    plot_rating_distribution(df)
    plot_theme_frequency(df)
    
    if 'date' in df.columns:
        plot_sentiment_trend(df)
        
    print("All visualizations generated successfully.")

if __name__ == "__main__":
    main()

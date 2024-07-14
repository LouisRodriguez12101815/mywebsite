import praw
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime, timedelta

# Set up Reddit API
reddit = praw.Reddit(client_id='PVB70Nf5tLOySUsY7eICbA',
                     client_secret='H7SUs6MlPHNyvqk_-FFfx8_b4GpHFA',
                     user_agent='Stock_app')

# Define the date range
start_date = datetime.utcnow() - timedelta(days=30)
end_date = datetime.utcnow()

# Function to get Reddit posts
def get_reddit_posts(subreddit, query, start_date, end_date):
    posts = []
    for submission in reddit.subreddit(subreddit).search(query, time_filter='month'):
        post_date = datetime.utcfromtimestamp(submission.created_utc)
        if start_date <= post_date <= end_date:
            posts.append(submission.title + " " + submission.selftext)
    return posts

# Sentiment Analysis function
def analyze_sentiment(stock_symbol):
    reddit_posts = get_reddit_posts('stocks', stock_symbol, start_date, end_date)
    
    analyzer = SentimentIntensityAnalyzer()
    sentiments = [analyzer.polarity_scores(post) for post in reddit_posts]
    
    df = pd.DataFrame(sentiments)
    df['text'] = reddit_posts
    
    numeric_cols = df.select_dtypes(include='number')
    summary = numeric_cols.mean()
    
    summary_str = summary.to_string()
    print("\nSentiment Analysis Summary for {}:".format(stock_symbol))
    print(summary_str)

# Main loop to continuously ask for stock symbols
while True:
    stock_symbol = input("Enter the stock symbol you want to analyze (or type 'exit' to quit): ").upper()
    if stock_symbol.lower() == 'exit':
        break
    analyze_sentiment(stock_symbol)

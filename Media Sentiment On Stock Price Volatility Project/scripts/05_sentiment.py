# scripts/05_semtiment.py

import os
from config import settings
from src.processing.sentiment_processor import SentimentProcessor
from src.utils.helpers import save_csv, load_csv, load_json

def main():
    # load directory structure
    dirs = load_json("project_paths.json")

    TICKERS = settings.TICKERS
    SentimentProcessor()

    for ticker in TICKERS:

        # loads and saves to processed_dir
        raw_dir = dirs["tickers"][ticker]["raw"]
        processed_dir = dirs["tickers"][ticker]["processed"]

        # checks if news and price data exists in raw
        if not os.path.exists(raw_dir, f"{ticker}_news_data.csv"):
            print("Skipping {ticker}: News data not found")
            continue
        if not os.path.exists(raw_dir, f"{ticker}_price_data.csv"):
            print("Skipping {ticker}: Price data not found")
            continue

        # load relevance scored news data
        news_data = load_csv(processed_dir, f"{ticker}_relevance_scored_news_data.csv")
        print(f"{ticker} relevance scored news data loaded")

        # calculates sentiment scores for news articles
        print(f"Calculating {ticker} sentiment scores")
        news_sentiment_scores = SentimentProcessor.assign_sentiment_score(news_data)
        print(f"{ticker} sentiment scores calculated!")

        # saves new csv with sentiment scores
        save_csv(news_sentiment_scores, processed_dir, f"{ticker}_sentiment_scored_news_data.csv")


if __name__ == "__main__":
    main()

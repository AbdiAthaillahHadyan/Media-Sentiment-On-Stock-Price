# scripts/06_sentiment_metrics.py

import os
from config import settings
from src.daily_metrics.sentiment_metrics import filtered_sentiment_metrics, weighted_sentiment_metrics
from src.utils.helpers import save_csv, load_csv, load_json

def main():
    # load directory structure
    dirs = load_json("project_paths.json")

    TICKERS = settings.TICKERS
  
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

        # load sentiment scored news data
        news_data = load_csv(processed_dir, f"{ticker}_sentiment_scored_news_data.csv")
        print(f"{ticker} relevance scored news data loaded")

        # calculates daily sentiment metrics based on filtering threshold
        print(f"Calculating {ticker} filtered daily sentiment metrics")
        filtered_sentiment_metrics = filtered_sentiment_metrics(news_data)
        print(f"{ticker} filtered daily sentiment metrics calculated!")

        # calculates daily sentiment metrics based on relevancy weights
        print(f"Calculating {ticker} relevancy weighted daily sentiment metrics")
        weighted_sentiment_metrics = weighted_sentiment_metrics(news_data)
        print(f"{ticker} relevancy weighted daily sentiment metrics calculated!")

        save_csv(filtered_sentiment_metrics, processed_dir, f"{ticker}_filtered_sentiment_metrics.csv")
        save_csv(filtered_sentiment_metrics, processed_dir, f"{ticker}_relevancy_weighted_sentiment_metrics.csv")


if __name__ == "__main__":
    main()

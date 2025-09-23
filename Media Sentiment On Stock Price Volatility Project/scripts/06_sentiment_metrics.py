# scripts/06_sentiment_metrics.py

from src.daily_metrics.sentiment_metrics import daily_sentiment_metrics
from src.utils.helpers import save_csv, load_csv, load_json, missing_file

def main():
    # load directory structure
    dirs = load_json("project_paths.json")

    TICKERS = load_json(dirs["raw"], "valid_tickers.json")

    metric_strategy = ["filtered_sentiment_metrics", "weighted_sentiment_metrics"]
  
    for ticker in TICKERS:

        # loads and saves to processed_dir
        raw_dir = dirs["tickers"][ticker]["raw"]
        processed_dir = dirs["tickers"][ticker]["processed"]

        # checks if raw news and price data exists
        if missing_file(raw_dir, ticker, f"{ticker}_news_data.csv"):
            continue
        if missing_file(raw_dir, ticker, f"{ticker}_price_data.csv"):
            continue

        # load sentiment scored news data
        news_data = load_csv(processed_dir, f"{ticker}_sentiment_scored_news_data.csv")
        print(f"{ticker} relevance scored news data loaded")

        for metric in metric_strategy:

            # calculates daily sentiment metrics based on metric calculation strategy
            print(f"Calculating {ticker} {metric.replace("_", " ")}")
            sentiment_metrics = daily_sentiment_metrics(news_data, metric)
            print(f"{ticker} {metric.replace("_", " ")} calculated!")
            save_csv(sentiment_metrics, processed_dir, f"{ticker}_{metric}.csv")

if __name__ == "__main__":
    main()

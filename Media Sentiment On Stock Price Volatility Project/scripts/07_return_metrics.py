# scripts/07_return_metrics.py

import os
from config import settings
from src.daily_metrics.return_metrics import return_metrics
from src.utils.helpers import save_csv, load_csv, load_json

def main():
    # load directory structure
    dirs = load_json("project_paths.json")

    TICKERS = settings.TICKERS

    for ticker in TICKERS:

        # loads from raw_dir and saves to processed_dir
        raw_dir = dirs["tickers"][ticker]["raw"]
        processed_dir = dirs["tickers"][ticker]["processed"]

        # checks if news and price data exists in raw
        if not os.path.exists(raw_dir, f"{ticker}_news_data.csv"):
            print("Skipping {ticker}: News data not found")
            continue
        if not os.path.exists(raw_dir, f"{ticker}_price_data.csv"):
            print("Skipping {ticker}: Price data not found")
            continue

        # load raw price data
        price_data = load_csv(raw_dir, f"{ticker}_price_data.csv")
        print(f"{ticker} price data loaded")

        # creates a new dataframe containing 3 return metrics: daily returns, overnight returns, and intraday returns
        print(f"Calculating {ticker} return metrics")
        metrics = return_metrics(price_data)
        print(f"{ticker} return metrics calculated!")

        save_csv(metrics, processed_dir, f"{ticker}_return_metrics.csv")





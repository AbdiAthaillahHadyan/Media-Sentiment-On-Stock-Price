# scripts/07_return_metrics.py

from src.daily_metrics.return_metrics import return_metrics
from src.utils.helpers import save_csv, load_csv, load_json, missing_file

def main():
    # load directory structure
    dirs = load_json("project_paths.json")

    TICKERS = load_json(dirs["raw"], "valid_tickers.json")

    for ticker in TICKERS:

        # loads from raw_dir and saves to processed_dir
        raw_dir = dirs["tickers"][ticker]["raw"]
        processed_dir = dirs["tickers"][ticker]["processed"]

        # checks if raw news and price data exists
        if missing_file(raw_dir, ticker, f"{ticker}_news_data.csv"):
            continue
        if missing_file(raw_dir, ticker, f"{ticker}_price_data.csv"):
            continue

        # load raw price data
        price_data = load_csv(raw_dir, f"{ticker}_price_data.csv")
        print(f"{ticker} price data loaded")

        # creates a new dataframe containing 3 return metrics: daily returns, overnight returns, and intraday returns
        print(f"Calculating {ticker} return metrics")
        metrics = return_metrics(price_data)
        print(f"{ticker} return metrics calculated!")

        save_csv(metrics, processed_dir, f"{ticker}_return_metrics.csv")





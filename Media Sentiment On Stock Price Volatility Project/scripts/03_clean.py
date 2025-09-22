# scripts/03_clean.py
import os
from config import settings
from src.processing.clean_data import clean_data
from src.utils.helpers import save_csv, load_csv, load_json

def main():
    # load directory structure
    dirs = load_json("project_paths.json")

    TICKERS = settings.TICKERS

    for ticker in TICKERS:

        # loads from raw_dir, saves to processed_dir
        raw_dir = dirs["tickers"][ticker]["raw"]
        processed_dir = dirs["tickers"][ticker]["processed"]

        # checks if news and price data exists
        if not os.path.exists(raw_dir, f"{ticker}_news_data.csv"):
            print("Skipping {ticker}: News data not found")
            continue
        if not os.path.exists(raw_dir, f"{ticker}_price_data.csv"):
            print("Skipping {ticker}: Price data not found")
            continue



        # load raw news data
        raw_news_data = load_csv(raw_dir, f"{ticker}_news_data.csv")
        print(f"{ticker} news data loaded ")

        # clean raw data and save to csv
        cleaned_news_data = clean_data(raw_news_data)
        save_csv(cleaned_news_data, processed_dir, f"{ticker}_cleaned_news_data.csv")
        print(f"{ticker} cleaned data saved")

if __name__ == "__main__":
    main()
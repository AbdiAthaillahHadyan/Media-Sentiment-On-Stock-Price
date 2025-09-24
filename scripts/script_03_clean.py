# scripts/03_clean.py

from src.processing.clean_data import clean_data
from src.utils.helpers import save_csv, load_csv, load_json

def main():
    # load directory structure
    dirs = load_json("project_paths.json")

    TICKERS = load_json(dirs["raw"], "valid_tickers.json")

    for ticker in TICKERS:
        # loads from raw_dir, saves to processed_dir
        raw_dir = dirs["tickers"][ticker]["raw"]
        processed_dir = dirs["tickers"][ticker]["processed"]

        # load raw news data
        try: 
            raw_news_data = load_csv(raw_dir, f"{ticker}_news_data.csv")
            print(f"{ticker} news data loaded ")

            # clean raw data and save to csv
            cleaned_news_data = clean_data(raw_news_data)
            save_csv(cleaned_news_data, processed_dir, f"{ticker}_cleaned_news_data.csv")
            print(f"{ticker} cleaned data saved")
        
        except FileNotFoundError as e:
            print(e)
            continue


if __name__ == "__main__":
    main()
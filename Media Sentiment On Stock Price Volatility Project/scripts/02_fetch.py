# scripts/02_fetch and clean.py
import sys
from config import settings
from src.data_fetching.finnhub_client import FinnhubClient
from src.data_fetching.yfinance_client import YFinanceClient
from src.utils.helpers import save_csv, save_json, load_json

def main():
    # load directory structure
    try:
        dirs = load_json("project_paths.json")

        TICKERS = settings.TICKERS
        START_DATE = settings.START_DATE
        END_DATE = settings.END_DATE

        # get aliases and price data from yfinance
        try:
            print("Retrieving data from yfinance")
            stock_aliases = YFinanceClient.get_stock_aliases(TICKERS)
            save_json(stock_aliases, dirs["raw"], "ticker_aliases.json")
            complete_price_data = YFinanceClient.get_price_data(TICKERS)
            print("yfinance data retrieved successfully")
        except Exception as e:
            print("Yahoo Finance API failed")
            raise

        # initiate finnhub client
        print("Retrieving data from Finnhub")
        finnhub = FinnhubClient()
        successful_tickers = []
        failed_tickers = []

        for ticker in TICKERS:
            try:
                raw_dir = dirs["tickers"][ticker]["raw"]

                # get news data from finnhub and save into a csv
                news_data = finnhub.get_stock_news(ticker, START_DATE, END_DATE)
                print(f"{ticker} news data retrieved successfully")
                save_csv(news_data, raw_dir, f"{ticker}_raw_news_data.csv")
                print(f"{ticker} news data saved")

                # extract and save price data for ticker into a csv
                stock_price_data = complete_price_data.xs(ticker, axis=1, level=1, drop_level=True)
                stock_price_data.columns = [col.lower() for col in stock_price_data.columns]
                stock_price_data.index.name = "date"
                save_csv(stock_price_data, raw_dir, f"{ticker}_price_data.csv")
                print(f"{ticker} price data saved")
                successful_tickers

            except Exception as e:
                print(f"Finnhub has failed to process {ticker}: {e}")
                failed_tickers.append(ticker)
                continue

        print("All required data have been fetched!")
        print("Fetch Summary:")
        print(f"Successful Tickers:" + " ".join(successful_tickers))
        print(f"Failed Tickers:" + " ".join(failed_tickers))

        if not successful_tickers:
            print("All tickers failed")
            sys.exit(1)

    except Exception as e:
        print(f"Critical error in fetch script: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
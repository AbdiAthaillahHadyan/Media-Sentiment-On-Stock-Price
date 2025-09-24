# scripts/02_fetch and clean.py

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
            complete_price_data = YFinanceClient.get_price_data(TICKERS, START_DATE, END_DATE)
            print("yfinance data retrieved successfully")

        except Exception as e:
            print("Yahoo Finance API failed")
            return 1 # Complete Failure

        # initiate finnhub client
        
        finnhub = FinnhubClient()
        valid_tickers = []
        failed_tickers = []

        for ticker in TICKERS:
            raw_dir = dirs["tickers"][ticker]["raw"]

            try:
                # extract and save price data for ticker into a csv
                if ticker not in complete_price_data.columns.get_level_values(1):
                    raise ValueError(f"No yfinance data returned for {ticker}")
                stock_price_data = complete_price_data.xs(ticker, axis=1, level=1, drop_level=True)
                stock_price_data.columns = [col.lower() for col in stock_price_data.columns]
                stock_price_data.index.name = "date"
                stock_price_data.reset_index(inplace=True)
                
                # get news data from finnhub and save into a csv
                print(f"Retrieving {ticker} data from Finnhub")
                news_data = finnhub.get_stock_news(ticker, START_DATE, END_DATE)
                print(f"{ticker} news data retrieved successfully")

                # saves data appends ticker to valid tickers only if both data can be fetched
                save_csv(stock_price_data, raw_dir, f"{ticker}_price_data.csv")
                save_csv(news_data, raw_dir, f"{ticker}_news_data.csv")
                valid_tickers.append(ticker)

            except Exception as e:
                print(f"Finnhub has failed to process {ticker}: {e}")
                stock_aliases.pop(ticker, None)
                failed_tickers.append(ticker)
                continue

        print("All required data have been fetched!")
        print("Fetch Summary:")
        print(f"Valid Tickers:" + " ".join(valid_tickers))
        print(f"Failed Tickers:" + " ".join(failed_tickers))

        save_json(valid_tickers, dirs["raw"], "valid_tickers.json")
        save_json(stock_aliases, dirs["raw"], "ticker_aliases.json")

        if not valid_tickers:
            print("All tickers failed")
            return 1 # Complete Failure



        return 0

    except Exception as e:
        print(f"Critical error in fetch script: {e}")
        return 1 # Complete Failure

if __name__ == "__main__":
    main()
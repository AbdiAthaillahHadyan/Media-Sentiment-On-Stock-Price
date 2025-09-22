# src/data_fetching/yfinance_client.py

import yfinance as yf


class YFinanceClient:
    def __init__(self):
        pass

    @staticmethod
    def get_price_data(tickers, start_date, end_date):
        return yf.download(tickers, start=start_date, end=end_date)
    
    @staticmethod
    def get_stock_aliases(tickers):
        alias_dict = {}

        for ticker in tickers:
            stock = yf.Ticker(ticker)
            info = stock.info

            aliases = [
                ticker,
                info.get("longName"),
                info.get("shortName")
                ]
            
            alias_dict[ticker] = [a for a in aliases if a]

        return alias_dict 
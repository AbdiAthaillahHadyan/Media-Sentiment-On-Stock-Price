# 

import yfinance as yf
from config import settings

def get_company_aliases():
    alias_dict = {}

    for ticker in settings.TICKERS:
        stock = yf.Ticker(ticker)

        aliases = [
            ticker,
            stock.info.get("longName"),
            stock.info.get("shortName")
            ]
        
        alias_dict[ticker] = [a for a in aliases if a]

    return alias_dict 
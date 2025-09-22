import yfinance as yf
from config import settings

def get_target_entities():
    target_entities = {}

    for ticker in settings.TICKERS:
        stock = yf.Ticker(ticker)

        aliases = [
            ticker,
            stock.info.get("longName"),
            stock.info.get("shortName")
            ]
        
        target_entities[ticker] = [a for a in aliases if a]

    return target_entities 
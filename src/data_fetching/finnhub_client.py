# src/data_Fetching/finnhub_client.py
import finnhub
import pandas as pd
import datetime as dt
import time
from ratelimit import limits, sleep_and_retry
from config import settings

class FinnhubClient:
    def __init__(self):
        self.client =  finnhub.Client(api_key=settings.FINNHUB_API_KEY)

    @sleep_and_retry
    @limits(calls=60, period=60)
    def call_company_news(self, stock, _from, to):
        """ Wrapper for self.client.company_news() with rate limiting"""
        try:
            return self.client.company_news(stock, _from=_from, to=to)
        except finnhub.FinnhubAPIException as e:
            print(f"Finnhub API error for {stock}: {e}")

    def get_stock_news(self, ticker, start_date, end_date):
        """Returns all news for a ticker in a DataFrame using Finnhub API"""
        
        print(f"Downloading news for {ticker} from Finnhub API...")
        stock = ticker
        news_data = []
        batch_start = start_date

        while batch_start <= end_date:
            batch_end = batch_start + dt.timedelta(days=6)
            batch = self.call_company_news(stock, _from=batch_start, to=(batch_end))
            news_data.extend(batch)
            batch_start += dt.timedelta(days=7)
            time.sleep(1)

        print(f"news for {ticker} collected...")
        return pd.DataFrame(news_data)

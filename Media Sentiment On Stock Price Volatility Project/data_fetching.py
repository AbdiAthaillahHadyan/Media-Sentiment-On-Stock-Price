from stock_news_processor import StockNewsProcessing
from sentiment_metrics import calculate_weighted_sentiment_metrics, calculate_filtered_sentiment_metrics
import yfinance as yf
import datetime as dt
import os

start_date = dt.date.today() - dt.timedelta(days=7)
end_date = dt.date.today()

target_ents_dict = {
    "TSLA": ["TSLA", "Tesla","Tesla Inc.", "Tesla Motors"]#,
    #"NVDA": ["NVDA", "Nvidia", "NVIDIA", "Nvidia Corporation", "Nvidia Corp.", "Nvidia Corp", "GeForce"],
    #"GME":  ["GME", "GameStop", "Game Stop","GameStop Corporation", "GameStop Corp.", "GameStop Corp"]
}

tickers = list(target_ents_dict.keys())

news_processor = StockNewsProcessing(
    api_key="d25lmkhr01qns40fidn0d25lmkhr01qns40fidng",
    nlp="en_core_web_trf", # "en_core_web_sm", "en_core_web_md", "en_core_web_lg", "en_core_web_trf"
    relevance_threshold=0.5
)

# create main folder
SAVE_DIR = "csv"
os.makedirs(SAVE_DIR, exist_ok=True)

# download price data for all stocks
price_data = yf.download(tickers, start=start_date, end=end_date)


for ticker in tickers:
    # create subfolder
    ticker_dir = os.path.join(SAVE_DIR, ticker)
    os.makedirs(ticker_dir, exist_ok=True)
    print(f"{ticker} subfolder created...")

    # full news data pipeline
    target_ents = target_ents_dict[ticker]
    news_data= news_processor.process_ticker(ticker, target_ents, start_date, end_date)
    print(f"{ticker} news data retrieved...")

    # calculate sentiment metrics
    filtered_sentiment_metrics = calculate_filtered_sentiment_metrics(news_data)
    weighted_sentiment_metrics = calculate_weighted_sentiment_metrics(news_data)
    print(f"{ticker} aggregate sentiment metrics calculated...")
    # save csv
    filtered_sentiment_metrics.to_csv(os.path.join(ticker_dir, f"{ticker}_filtered_sentiment_metrics_data.csv"))
    weighted_sentiment_metrics.to_csv(os.path.join(ticker_dir, f"{ticker}_weighted_sentiment_metrics_data.csv"))
    news_data.to_csv(os.path.join(ticker_dir, f"{ticker}_news_data.csv"), index=False)
    print(f"{ticker} news data saved...")

    # extract and save price data for ticker
    stock_price_data = price_data.xs(ticker, axis=1, level=1, drop_level=True)
    stock_price_data.columns = [col.lower() for col in stock_price_data.columns]
    stock_price_data.index.name = "date"
    stock_price_data.to_csv(os.path.join(ticker_dir, f"{ticker}_price_data.csv"))
    print(f"{ticker} price data saved...")
    

print("finished")

# scripts/04_relevancy.py

import os
from config import settings
from src.processing.relevance_processor import RelevanceProcessor
from src.utils.helpers import save_csv, load_csv, load_json

def main():
    # load directory structure
    dirs = load_json("project_paths.json")
    alias_dict = load_json("ticker_aliases.json")

    TICKERS = settings.TICKERS
    RelevanceProcessor()

    for ticker in TICKERS:

        # loads and saves to processed_dir
        raw_dir = dirs["tickers"][ticker]["raw"]
        processed_dir = dirs["tickers"][ticker]["processed"]
        
        # checks if news and price data exists in raw
        if not os.path.exists(raw_dir, f"{ticker}_news_data.csv"):
            print("Skipping {ticker}: News data not found")
            continue
        if not os.path.exists(raw_dir, f"{ticker}_price_data.csv"):
            print("Skipping {ticker}: Price data not found")
            continue

        ticker_aliases = alias_dict[ticker]
    
        # load cleaned news data

        news_data = load_csv(processed_dir, f"{ticker}_cleaned_news_data.csv")
        print(f"{ticker} cleaned news data loaded ")

        # calculates scores for news articles
        news_relevance_scores = RelevanceProcessor.calculate_relevance(news_data, ticker_aliases)

        # filters out news articles that do not directly mention the ticker
        news_relevance_scores = news_relevance_scores[news_relevance_scores["relevance"] > 0]
        save_csv(news_relevance_scores, processed_dir, f"{ticker}_relevance_scored_news_data.csv")


if __name__ == "__main__":
    main()
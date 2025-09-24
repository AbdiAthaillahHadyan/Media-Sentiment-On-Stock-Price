# scripts/04_relevancy.py

from src.processing.relevance_processor import RelevanceProcessor
from src.utils.helpers import save_csv, load_csv, load_json

def main():
    # load directory structure
    dirs = load_json("project_paths.json")
    alias_dict = load_json(dirs["raw"], "ticker_aliases.json")

    TICKERS = load_json(dirs["raw"], "valid_tickers.json")
    relevance_processor = RelevanceProcessor()

    for ticker in TICKERS:
        # loads and saves to processed_dir
        processed_dir = dirs["tickers"][ticker]["processed"]

        ticker_aliases = alias_dict[ticker]
        try:
            # load cleaned news data
            news_data = load_csv(processed_dir, f"{ticker}_cleaned_news_data.csv")
            print(f"{ticker} cleaned news data loaded ")

            # calculates relevance scores for news articles
            print(f"Calculating {ticker} relevance scores")
            news_relevance_scores = relevance_processor.calculate_relevance(news_data, ticker_aliases)
            print(f"{ticker} relevance scores calculated")

            # filters out news articles that do not directly mention the ticker
            news_relevance_scores = news_relevance_scores[news_relevance_scores["relevance"] > 0]

            # saves new csv with relevance scores
            save_csv(news_relevance_scores, processed_dir, f"{ticker}_relevance_scored_news_data.csv")

        except FileNotFoundError as e:
            print(e)
            continue


if __name__ == "__main__":

    main()
import scripts.script_01_directories as directories
import scripts.script_02_fetch as fetch
import scripts.script_03_clean as clean
import scripts.script_04_relevancy as relevancy
import scripts.script_05_sentiment as sentiment
import scripts.script_06_sentiment_metrics as sentiment_metrics
import scripts.script_07_return_metrics as return_metrics
import scripts.script_08_analysis_and_visualisation as analysis_and_visualisation
from src.utils.helpers import load_json
import os

def main():
    print("Starting pipeline execution...")

    # Step 1: Set up directories
    print("Running script_01_directories...")
    directories.main()

    # Step 2: Fetch data
    print("Running script_02_fetch...")
    fetch.main()

    # Check if valid_tickers.json exists and has tickers
    try:
        valid_tickers = load_json("data/raw", "valid_tickers.json")
        if not valid_tickers:
            print("Error: valid_tickers.json is empty. No valid tickers to process. Exiting.")
            return
    except FileNotFoundError:
        print("Error: valid_tickers.json not found. Exiting.")
        return

    # Step 3: Clean news data
    print("Running script_03_clean...")
    clean.main()

    # Step 4: Calculate relevance scores
    print("Running script_04_relevancy...")
    relevancy.main()

    # Step 5: Calculate sentiment scores
    print("Running script_05_sentiment...")
    sentiment.main()

    # Step 6: Calculate sentiment metrics
    print("Running script_06_sentiment_metrics...")
    sentiment_metrics.main()

    # Step 7: Calculate return metrics
    print("Running script_07_return_metrics...")
    return_metrics.main()

    # Step 8: Perform analysis and visualization
    print("Running script_08_analysis...")
    analysis_and_visualisation.main()

    print("Pipeline execution completed!")

if __name__ == "__main__":
    main()
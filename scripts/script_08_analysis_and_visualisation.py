# scripts/08_analysis.py

import pandas as pd
import seaborn as sns
from src.analysis.correlation import correlation_statistic
from src.analysis.regression import regression_statistic
from src.visualisation.scatterplot import create_scatterplot
from src.utils.helpers import create_path, load_csv, save_json, load_json
sns.set_theme()

def main():
    # load directory structure
    dirs = load_json("project_paths.json")

    TICKERS = load_json(dirs["raw"], "valid_tickers.json")

    return_metrics_types = ["daily_returns", "overnight_returns", "intraday_returns"]
    sentiment_metrics_types = ["filtered_sentiment_metrics", "weighted_sentiment_metrics"]

    for ticker in TICKERS:
        # loads from processed_dir and saves to analysis_dir
        processed_dir = dirs["tickers"][ticker]["processed"]
        analysis_dir = dirs["tickers"][ticker]["analysis"]

        analysis_results = {
            "ticker": ticker,
            "metric_combinations": {}
        }

        try:
            # loads the return metrics file of the ticker
            return_metrics_data = load_csv(processed_dir, f"{ticker}_return_metrics.csv")

            for s_metric in sentiment_metrics_types:
                # loads the sentiment metric file (filtered or weighted) with date, and mean_sentiment only
                sentiment_df = load_csv(processed_dir, f"{ticker}_{s_metric}.csv")
                sentiment_df = sentiment_df[["date", "mean_sentiment"]]
                
                for r_metric in return_metrics_types:
                    # create a unique key for the combination
                    combo_key = f"{s_metric}_{r_metric}"

                    # fetches the specified return metric on each day
                    return_df = return_metrics_data[["date", r_metric]]

                    # merges the two dataframes, dropping the date column, and rows with na
                    paired_df = pd.merge(sentiment_df, return_df, on="date")
                    paired_df = paired_df[["mean_sentiment", r_metric]].dropna()

                    # returns correlation and regression statistics in dictionary format
                    print(f"Analysing results for {ticker}: {combo_key}")
                    analysis_results["metric_combinations"][combo_key] = {
                        "sentiment_metric": s_metric,
                        "returns_metric": r_metric,
                        "n_observations": len(paired_df),
                        "correlation": correlation_statistic(
                            data=paired_df, 
                            x="mean_sentiment", 
                            y=r_metric,
                            ticker=ticker
                            ),
                        "regression": regression_statistic(
                            data=paired_df, 
                            x="mean_sentiment", 
                            y=r_metric,
                            ticker=ticker
                            )
                    }

                    plot_title = f"{ticker}: {s_metric.replace('_', ' ').title()} On {r_metric.replace('_', ' ').title()}"
                    create_scatterplot(
                        data=paired_df, 
                        x="mean_sentiment", 
                        y=r_metric, 
                        title=plot_title,
                        file_path=create_path(analysis_dir, f"{ticker}_{s_metric}_on_{r_metric}.png")
                        )
                    
            save_json(analysis_results, analysis_dir, f"{ticker}_analysis_results.json")      
                    
        except FileNotFoundError as e:
            print(e)
            continue

if __name__ == "__main__":
    main()

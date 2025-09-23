# src/daily_metrics/sentiment_metrics.py

def daily_sentiment_metrics(sentiment_data, metric_type):
    if metric_type == "filtered_sentiment":
        df = sentiment_data[sentiment_data["relevance"] > 0.5].copy()
        df["_score"] = df["sentiment_score"]
    if metric_type == "weighted_sentiment":
        df = sentiment_data.copy()
        df["_score"] = df["sentiment_score"] * df["relevance"]

    df_metrics = df.groupby("date").agg(
        mean_sentiment=("_score", "mean"),
        polarity=("_score", lambda x: "positive" if x.mean() > 0 else ("negative" if x.mean() < 0 else "neutral")),
        sentiment_volatility=("_score", "std"),
        minimum_sentiment= ("_score", "min"),
        Q1_sentiment= ("_score", lambda x: x.quantile(0.25)),
        median_sentiment= ("_score", "median"),
        Q3_sentiment= ("_score", lambda x: x.quantile(0.75)),
        maximum_sentiment= ("_score", "max"),
        IQR= ("_score", lambda x: x.quantile(0.75) - x.quantile(0.25))
        )

    return df_metrics


    

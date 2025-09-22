# src/daily_metrics/sentiment_metrics.py

def filtered_sentiment_metrics(df):
    """Returns daily sentiment metrics """
    df = df[df["relevance"] > 0.5]
    df = df.groupby("date").agg(
    mean_sentiment=("sentiment_score", "mean"),
    polarity=("sentiment_score", lambda x: "positive" if x.mean() > 0 else ("negative" if x.mean() < 0 else "neutral")),
    sentiment_volatility=("sentiment_score", "std"),
    minimum_sentiment= ("sentiment_score", "min"),
    Q1_sentiment= ("sentiment_score", lambda x: x.quantile(0.25)),
    median_sentiment= ("sentiment_score", "median"),
    Q3_sentiment= ("sentiment_score", lambda x: x.quantile(0.75)),
    maximum_sentiment= ("sentiment_score", "max"),
    IQR= ("sentiment_score", lambda x: x.quantile(0.75) - x.quantile(0.25)))

    return df  

def weighted_sentiment_metrics(df):
    """Returns daily sentiment metrics """

    df["weighted_sentiment"] = df["sentiment_score"] * df["relevance"]
    df = df.groupby("date").agg(
    mean_sentiment=("weighted_sentiment", "mean"),
    polarity=("weighted_sentiment", lambda x: "positive" if x.mean() > 0 else ("negative" if x.mean() < 0 else "neutral")),
    sentiment_volatility=("weighted_sentiment", "std"),
    minimum_sentiment= ("weighted_sentiment", "min"),
    Q1_sentiment= ("weighted_sentiment", lambda x: x.quantile(0.25)),
    median_sentiment= ("weighted_sentiment", "median"),
    Q3_sentiment= ("weighted_sentiment", lambda x: x.quantile(0.75)),
    maximum_sentiment= ("weighted_sentiment", "max"),
    IQR= ("weighted_sentiment", lambda x: x.quantile(0.75) - x.quantile(0.25)))

    return df  
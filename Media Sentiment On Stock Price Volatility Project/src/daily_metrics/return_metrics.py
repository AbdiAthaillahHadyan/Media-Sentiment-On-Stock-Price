# /src/daily_metrics/return_metrics

import pandas as pd

def return_metrics(price_data):
    df = price_data[["date", "open","close"]].copy
    
    # creates new columns for return metrics
    daily_returns = df["close"].pct_change() * 100
    overnight_returns = (df["open"]/df["close"].shift(1) - 1) * 100
    intraday_returns = (df["close"]/df["open"] - 1) * 100

    # create a dataframe for metrics only
    metrics = pd.DataFrame({
        "date": df["date"],
        "daily_returns": daily_returns,
        "overnight_returns": overnight_returns,
        "intraday_returns": intraday_returns
    })

    return metrics
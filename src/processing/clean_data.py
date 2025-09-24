# src/processing/news_cleaner.py

import pandas as pd


def clean_data(df):
    """Cleans Dataframe"""
    print("Cleaning data from Finnhub API...")
    # rename datetime column into date for consistency
    df = df.rename(columns={"datetime": "date"})
    # filters out irrelevant columns
    df = df[["date", "headline", "summary", "source"]]
    # filters out erroneous dates
    df = df[df["date"] > 0]
    # filters out any articles with missing date, headline, summary, and source data
    df.replace("", pd.NA, inplace=True)
    df.dropna(inplace=True)
    # filters out duplicate articles if present
    df.drop_duplicates(subset=["headline", "summary"], inplace=True)
    # sort by date
    df.sort_values(by="date", ascending=True, inplace=True)
    # converts date (UNIX timestamps in seconds) into datetime objects
    df["date"] = pd.to_datetime(df["date"], unit="s", errors="coerce")
    df["date"] = df["date"].dt.date
    print("Data cleaned...")
    return df


    

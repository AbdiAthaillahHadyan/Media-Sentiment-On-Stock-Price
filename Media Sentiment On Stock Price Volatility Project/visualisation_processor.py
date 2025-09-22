import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import numpy as np
import os

class Price_Sentiment_Processor:

    def sentiment_returns_df(sentiment_data, price_data):
        price_data = price_data[["date", "open","close"]]
        
        # creates new columns for return metrics
        price_data["daily_returns"] = price_data["close"].pct_change() * 100
        price_data["overnight_returns"] = (price_data["open"]/price_data["close"].shift(1) - 1) * 100
        price_data["intrday_returns"] = (price_data["close"]/price_data["open"] - 1) * 100
        price_data = price_data.drop(columns="close")

        # create a dataframe for sentiment
        daily_sentiment = sentiment_data[["date", "mean_sentiment"]]

        # merge dataframe on date
        df = pd.merge(df, daily_sentiment, on="date")
        #df["mean_sentiment"] = df["mean_sentiment"].shift(1)

        return df[["mean_sentiment", "return"]].dropna()

    def create_scatterplot(sentiment, returns, title, save_loc):
        sns.regplot(x=sentiment, y=returns, scatter_kws={"alpha":0.6})
        plt.xlabel("Daily Average Sentiment")
        plt.ylabel("Returns")
        plt.title(title)
        plt.savefig(os.path.join(save_loc, f"{title}.png"))
        plt.show()

    def regression_statistics(sentiment, returns, ticker):
        x = sentiment
        y = returns
        model = sm.OLS(y, x).fit()
        text = model.summary()
        
        print(text)


MAIN_FOLDER_DIR = "csv"
dir_list = os.listdir(MAIN_FOLDER_DIR)
for ticker in dir_list:
    
    ticker_dir = os.path.join(MAIN_FOLDER_DIR, ticker)

    sentiment_data = pd.read_csv(os.path.join(ticker_dir, f"{ticker}_weighted_sentiment_metrics_data.csv"))    
    price_data = pd.read_csv(os.path.join(ticker_dir, f"{ticker}_price_data.csv"))
    df = Price_Sentiment_Processor.sentiment_returns_df(sentiment_data, price_data)
    Price_Sentiment_Processor.create_scatterplot(
        sentiment=df["mean_sentiment"], 
        returns=df["return"], 
        title=f"{ticker} Weighted Sentiment on Daily Returns", 
        save_loc=ticker_dir)

    Price_Sentiment_Processor.regression_statistics(df[["mean_sentiment"]], df["return"], ticker)
    
    
    


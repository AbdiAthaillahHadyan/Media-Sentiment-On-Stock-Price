# src/analysis/correlation_analysis.py

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import numpy as np
import os

class CorrelationAnalyser:

    def __init__(self):
        pass
    
    @staticmethod
    def create_scatterplot(sentiment, returns, title):
        sns.regplot(x=sentiment, y=returns, scatter_kws={"alpha":0.6})
        plt.xlabel("Daily Average Sentiment")
        plt.ylabel("Returns")
        plt.title(title)
        plt.savefig()
        plt.show()

    @staticmethod
    def regression_statistics(sentiment, returns, ticker):
        x = sentiment
        y = returns
        model = sm.OLS(y, x).fit()
        text = model.summary()
        
        print(text)

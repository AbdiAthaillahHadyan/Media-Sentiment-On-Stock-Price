# src/analysis/regression.py

import statsmodels.api as sm
import pandas as pd


def regression_statistic(data, x, y, ticker):

    # returns none if there is insufficient data for a regression.
    if len(data) < 2:
        print(f"{ticker}: Too few datapoints")
        return None 

    X = sm.add_constant(data[x])
    Y = data[y]
    model = sm.OLS(Y, X).fit()
    
    results = {
        "r_squared": model.rsquared,
        "adjusted_r_squared": model.rsquared_adj,
        "slope_coefficient": model.params[x], 
        "slope_p_value": model.pvalues[x],
        "intercept": model.params["const"], 
        "f_statistic": model.fvalue,
        "f_p_value": model.f_pvalue,
        "n_observations": int(model.nobs)

    }

    return results
    

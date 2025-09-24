# src/analysis/correlation_analysis.py

from scipy.stats import pearsonr, spearmanr

def calculate_pearson(x, y):
    corr, p_value = pearsonr(x, y)
    results = {
        "correlation": corr,
        "p_value": p_value
    }
    return results

def calculate_spearman(x, y):
    corr, p_value = spearmanr(x, y)
    results = {
        "correlation": corr,
        "p_value": p_value
    }
    return results

def correlation_statistic(data, x, y, ticker):
    # returns none if there is insufficient data for a regression.
    if len(data) < 2:
        print(f"{ticker}: Too few datapoints")
        return None
    
    pearson_results = calculate_pearson(data[x], data[y])
    spearman_results = calculate_spearman(data[x], data[y])

    results = {
        "pearson": pearson_results,
        "spearman": spearman_results
        
    }

    return results

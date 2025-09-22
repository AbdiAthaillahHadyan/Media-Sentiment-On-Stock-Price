# config/settings.py
import os
from dotenv import load_dotenv
# Model Settings
FINNHUB_API_KEY = None
NER_MODEL = "en_core_web_trf"

# Relevancy calculation settings
# ALPHA and BETA are weights for headlines and summaries respectively and should sum to 1
# RELEVANCE_THRESHOLD is the minimum relevance score an article must have for the filtered_sentiment_metrics
ALPHA = 0.67
BETA = 0.33
RELEVANCE_THRESHOLD = 0.5

# List of tickers to be analysed
TICKERS = []




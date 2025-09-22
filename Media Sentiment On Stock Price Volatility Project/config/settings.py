# config/settings.py
import os
import datetime as dt
from dotenv import load_dotenv


def parse_date(var, default):
    """ Checks if the date input in .env is in the correct format. returns input if true, returns default if false"""
    date = os.getenv(var)
    if date:
        try:
            return dt.datetime.strptime(date, "%Y-%m-%d")
        except (ValueError, TypeError):
            print(f"Warning: Invalid date format. Using default.")
    return default


def parse_float(var, default):
    """ Checks if the float input in .env is in the correct format. returns input if true, returns default if false"""
    float_var = os.getenv(var)
    if float:
        try:
            return float(float_var)
        except TypeError:
            print(f"Warning: Invalid {var} input. Using default")
    return default

def check_settings():
    """ Checks all required settings """
    errors = []
    if not FINNHUB_API_KEY:
        errors.append("FINNHUB_API_KEY Required, get your free API key from https://finnhub.io/")
    
    if END_DATE < START_DATE:
        errors.append(f"END_DATE {END_DATE} cannot be before START_DATE {START_DATE}")

    if not TICKERS:
        errors.append("No TICKERS named in .env")

    if errors:
        error_message = "Config Errors:\n" + "".join(f" - {error}\n" for error in errors)
        raise ValueError(error_message)

# Load .env
load_dotenv()

# API Settings
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

# MODEL Settings
NER_MODEL = "en_core_web_trf"

# Analysis Duration
START_DATE = parse_date("START_DATE", dt.date.today() - dt.timedelta(days=7))
END_DATE = parse_date("END_DATE", dt.date.today())

# Relevancy calculation settings
ALPHA = parse_float("ALPHA", 0.67)
BETA = parse_float("BETA", 0.33)
RELEVANCE_THRESHOLD = parse_float("RELEVANCE_THRESHOLD", 0.5)

# List of tickers to be analysed
TICKERS = [ticker.strip().upper() for ticker in os.getenv("TICKERS", "").split(",") if ticker.strip]

check_settings()


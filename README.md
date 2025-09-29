# Analyse Impact of Financial News Media on Stock Price

## Overview
The ultimate objective of this project is to determine how stock prices fluctuate based on news media sentiment. To do this, the project fetches historical news articles and stock prices from Finnhub, and Yahoo Finance respectively. This data is then processed to aggregate daily sentiment scores using NLP models, such as spaCy's pre-trained English Language model `en_core_web_trf` and Hugging Face's `FinBERT` model. Using this data, correlation coefficients, Ordinary-Least-Squares regressions, and scatter-plots are employed.

## Features
- Fetches historical financial news of target companies
- Fetches historical price data of target companies
- Calculates relevancy scores of news articles
- Calculates sentiment scores of news articles
- Calculates two measures of aggregate daily sentiment scores
- Calculates three measures of stock returns
- Analyses all combinations of sentiment and return measures
- Plots all combinations of sentiment and return measures

## Installation

Clone the repository and install dependencies.

```bash
git clone _
cd _
pip install -r requirements.txt
```

Download spaCy NLP model.
```bash
python -m spacy download en_core_web_trf
```

## Configuration

This project uses a .env file for parameter customisation. To use:
1. Copy `.env.example` and rename it into .env.
2. Customise parameters to your liking

### Example .env file
```ini
# FINNHUB API CONFIGURATION
FINNHUB_API_KEY=your_api_key

# DATA SETTINGS
TICKERS=TSLA,NVDA,GME

START_DATE=
END_DATE=

# NLP MODEL SETTINGS
NER_MODEL=en_core_web_trf
SENTIMENT_MODEL=ProsusAI/finbert

# ANALYSIS PARAMETERS
ALPHA=0.67
BETA=0.33
RELEVANCE_THRESHOLD=0.1
```

### Notes
- `FINNHUB_API_KEY` must be replaced with your own API key, available for free at [Finnhub](https://finnhub.io/)
- `TICKERS` can be a single ticker or a list of tickers, separated by a comma.
- If `START_DATE` and `END_DATE` is empty, it defaults to the past 365 days.
- `NER_MODEL` and `SENTIMENT_MODEL` specifies the models for relevancy and sentiment calculations respectively.
- `NER_MODEL` defaults to `en_core_web_trf`.
- `SENTIMENT_MODEL` defaults to `ProsusAI/finbert`.
- `ALPHA` and `BETA` are the relevancy weightings for headlines and summaries respectively.
- `ALPHA` defaults to `0.67`.
- `BETA` defaults tp `0.33`.
- `RELEVANCE_THRESHOLD` is the filter threshold for the `filtered_sentiment_metrics`. Defaults to `0.1`.

## Usage
Run the full pipeline with:
```bash
python run_pipeline.py
```

## Output
For each ticker listed in `.env`, the pipeline will output all analysed data in `data/analysis/ticker`. This will include the following:
- Analysis results found in `TICKER_analysis_results.json`.
- Plots for all metric combinations.

### Example output
Examples of outputs tested for TSLA, NVDA, and GME can be found in the `data` directory of the repository.
## Report
For a detailed report on the methodology, limitations, and a detailed analysis of results for TSLA, NVDA, and GME, please find [REPORT.md](REPORT.md).

## References
### Data Sources
- [Finnhub API](https://finnhub.io/) - for news data
- [Yahoo Finance](https://uk.finance.yahoo.com/) - for stock price data via `yfinance`
### NLP Models
- [en_core_web_trf (spaCy)](https://spacy.io/) - for sentiment analysis
- [ProsusAI/FinBERT](https://huggingface.co/ProsusAI/finbert) - for relevancy calculations

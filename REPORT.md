# A Study of News Media Sentiment on Stock Price

## Table of Contents
 - [1. The Objective](#1.-The-Objective)
 - [1. The Data](#2.-The-Data)
 - [1. The Methodology](#3.-The-Methodology)
 - [1. The Results](#4.-The-Results)
 - [1. The Limitations](#5.-The-Limitations)

## 1. The Objective

News on companies can often be found publically available from sources such as Yahoo Finance. Thus, a question arises: "Can analysing news sentiment of companies enable the prediction of stock price fluctuations?".
Employing correlation, and Ordinary-Least-Squares (OLS) regression, this project aims to test this hypothesis.

## 2. The Data

There are 2 primary components of data this project will analyse to test the hypothesis:
 - News Data
 - Stock Price Data

The news data refers to all the available news articles that specify a target stock, spanning the entire period being studied. 
This project fetches all this data from [Finnhub](https://finnhub.io/), a free API that provides the dataset of news articles from a variety of sources.
Conveniently, all of this data is accessible via the `finnhub-python` library.
However, the Finnhub API does place limitations on its free users, limiting our dataset to the past 365 days, and fixing the maximum study period to a year's worth of data.
Furthermore, news data does not include the entire article. Rather, Finnhub provides the headline, and a short summary. 
Whilst the summary can provide a more compact version of the concepts covered in the entire article, sentiment calculations of the article will not be perfectly accurate, due to some loss in data.

The stock price data refers to the open and close prices of target stocks from [Yahoo Finance](https://uk.finance.yahoo.com/). In this project, this data is fetched using the `yfinance` Python package.
Again, due to the limitations set by Finnhub, `script_02_fetch.py`, will only fetch price data for the past 365 days.

In `script_07_return_metrics.py`, this price data is used to calculate 3 measures of returns:
- `daily_returns` (%) $ = \frac{close_{t} - close_{t-1}}{close_{t-1}} \times 100\% $
- `overnight_returns` (%) $ = \frac{close_{t+1} - close_{t}}{close_{t}}  \times 100\% $ 
- `intraday_returns` (%) $ = \frac{close_{t} - open_{t}}{open_{t}}  \times 100\%$



## 3. The Methodology

As mentioned in the objective, the final act of this project will involve a statistical analysis on the relationship between news sentiment on stock price (% returns).
However, before expanding on the calculations involved in this endeavor, this section will also cover the methods used to clean the data and prepare sentiment scores.

The first step of this operation was to 'clean' the data. This step mainly involved reformatting news data and price data from finnhub and yfinance respectively.
However, a core component of this step, that is not immediately obvious is the cleaning of irrelevant news articles.
Finnhub, although powerful, and most importantly a free tool, is not perfect in providing news articles. Looking at the raw news data, many articles focus on entire stock indexes such as the Standard & Poor's 500 (S&P500).
Although sentiment on stock indexes may result in individual stock price fluctuations, the goal of this project is to see the impact of news articles with direction mentions to the company/stock.
Thus, to calculate a 'relevance score' this project employed a Natural Language Processing (NLP) model. More specifically, `en_core_web_trf`, a pretrained English Language model from spaCy with a Named Entity Recognition componenent. Using this model, entities listed under the label 'ORG', and the frequencies at which they are mentioned are extracted from the headline and summaries of all fetched articles.
The relevance score of those articles are then calculated by the following formula:
$$
\text{Relevance Score} = \frac{\alpha \times h_{\text{target\_count}} + \beta \times s_{\text{target\_count}}} {\alpha \cdot \sum h_{\text{counts}} + \beta \cdot \sum s_{\text{counts}}}
$$
where:
- $\alpha$ = weight constant of headline mentions
- $\beta$ = weight constant of summary mentions
- $h_{\text{target\_count}}$ = headline mentions of target organisation
- $s_{\text{target\_count}}$ = summary mentions of target organisation
- $h_{\text{counts}}$ = headline mentions of all organisations
- $s_{\text{counts}}$ = summary mentions of all organisations

Undoubtedly, the level of 'sentiment' a news article has, directed to a company, is naturally unavailable from the raw news data. Initially, this data was extracted using the `vaderSentiment` Python package, due to its simplicity and the ease of integrating the analyser into existing code. However, this approached proved to be ineffective for this project's use-case. As the `vaderSentiment` is a lexicon-based sentiment analyser, context sensitivity was often times poor. Additionally, finance-specific language was often misinterpreted, resulting in a `sentiment_score` that did not accurately represent the tone of the article.

To illustrate, consider the following generic news summary:

    "Over the past six months, [COMPANY]’s shares (currently trading at [PRICE]) have posted a disappointing [LOSS]% loss, well below the market’s [BENCHMARK]% gain. This may have investors wondering how to approach the situation."

Using `vaderSentiment`, a news summary such as this would often be misclassified as neutral or even positive, despite a clear decline in stock performance.

To overcome this, the FinBERT (ProsusAI/finbert) transformer model, pre-trained using financial text, from [Hugging Face](https://huggingface.co/ProsusAI/finbert) was adopted, providing frequently more accurate sentiment scores. For the purposes of this report, the underlying mechanisms by which teh FinBERT model analyses sentiment will not be discussed as the focus here is on its application on financial news, rather than its architecture. What is important, however, is that the custom class (`SentimentProcessor`) in the `sentiment_processor,py` module was developed and imported into the `script_05_sentiment.py` script. This class applies FinBERT to each article's headline and summary, returning the probability of each sentiment classification (positive, negative, neutral). A final `sentiment_score` for the article is calculated using the following formula:
`sentiment_score`  
$$
= P(\text{positive}) \times 1 + P(\text{negative}) \times -1 + P(\text{neutral}) \times 0 = P(\text{positive}) - P(\text{negative})
$$













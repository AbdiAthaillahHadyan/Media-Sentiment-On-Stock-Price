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
This project fetches all this data from Finnhub, a free API that provides the dataset of news articles from a variety of sources.
Conveniently, all of this data is accessible via the Finnhub Python client library.
However, the Finnhub API does place limitations on its free users, limiting our dataset to previous year, and fixing the maximum study period to a year's worth of data.
Furthermore, news data does not include the entire article. Rather, finnhub provides the headline, and a short summary. 
Whilst, the summary can provide a more compact version of the concepts covered in the entire article, sentiment calculations of the article will not be perfectly accurate.

The stock price data refers to the open and close prices of target stocks.
This project fetches this data using the yfinance python package for accessing Yahoo Finance data.

## 3. The Methodology

As mentioned in the objective, the final act of this project will involve a statistical analysis on the relationship between news sentiment on stock price (% returns).
However, before expanding on the calculations involved in this endeavor, this section will also cover the methods used to clean the data and prepare sentiment scores.

The first step of this operation was to 'clean' the data. This step mainly involved reformatting news data and price data from Finnhub and yfinance respectively.
However, a core component of this step, that is not immediately obvious is the cleaning of irrelevant news articles.
Finnhub, although powerful, and most importantly a free tool, is not perfect in providing news articles. Looking at the raw news data, many articles focus on entire stock indexes such as the Standard & Poor's 500 (S&P500).
Although sentiment on stock indexes may result in individual stock price fluctuations, the goal of this project is to see the impact of news articles with direction mentions to the company/stock.
Thus, to calculate a 'Relevancy Score' this project employed a Natural Language Processing (NLP) model. More specifically, 'en_core_web_trf', a pretrained English Language model from spaCy with a Named Entity Recognition componenent. Using this model, entities listed under the label 'ORG', and the frequencies at which they are mentioned are extracted from the headline and summaries of all fetched articles.
The relevance score of those articles are then calculated by the following formula:
$$
\text{Relevance Score} = \dfrac{\alpha \times h_{\text{target\_count}} + \beta \times s_{\text{target\_count}}} {\alpha \cdot \sum h_{\text{counts}} + \beta \cdot \sum s_{\text{counts}}}
$$
where:
- $\alpha$ = weight constant of headline mentions
- $\beta$ = weight constant of summary mentions
- $h_{\text{target\_count}}$ = headline mentions of target organisation
- $s_{\text{target\_count}}$ = summary mentions of target organisation
- $h_{\text{counts}}$ = headline mentions of all organisations
- $s_{\text{counts}}$ = summary mentions of all organisations

Undoubtedly, the level of 'sentiment' a news article has, directed to a company, is naturally unavailable from the raw news data. Thus, to calculate this sentiment another NLP model was employed, that being the FinBERT transformer model from Hugging Face.









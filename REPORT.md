# A Study of News Media Sentiment on Stock Price

## Table of Contents
 - [1. The Objective](#1.-The-Objective)
 - [2. The Data](#2.-The-Data)
 - [3. The Methodology](#3.-The-Methodology)
 - [4. The Results](#4.-The-Results)
 - [5. The Limitations](#5.-The-Limitations)
 - [6. The Conclusion](#6-the-conclusion)
 - [7. References](#7-references)

## 1. The Objective

News on companies can often be found publically available from sources such as Yahoo Finance. Thus, a question arises: "Can analysing news sentiment of companies enable the prediction of stock price fluctuations?".
Employing correlation, and Ordinary-Least-Squares (OLS) regression, this project aims to test this hypothesis by testing three stocks with the developed pipeline.
These stocks include:
1. Two established but narrative-amplified growth stocks (Nvidia and Tesla), where sentiment may influence stock price alongside fundamentals.
2. One meme stock (GameStop), where historically, sentiment has driven price movements.

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

To overcome this, the FinBERT (ProsusAI/finbert) transformer model, pre-trained using financial text, from [Hugging Face](https://huggingface.co/ProsusAI/finbert) was adopted, providing frequently more accurate sentiment scores. For the purposes of this report, the underlying mechanisms by which teh FinBERT model analyses sentiment will not be discussed as the focus here is on its application on financial news, rather than its architecture. What is important, however, is that the custom class (`SentimentProcessor`) in the `sentiment_processor.py` module was developed to apply the FinBERT model to each article's headline and summary, returning the probability of each sentiment classification (positive, negative, neutral). A final `sentiment_score` for the article is calculated using the following formula:

  $ \text{Sentiment Score} = P(\text{positive}) \times 1 + P(\text{negative}) \times -1 + P(\text{neutral}) \times 0 = P(\text{positive}) - P(\text{negative}) $

Before any analysis, both price data and sentiment data required pre-processing. Individual sentiment scores were aggregated into daily metrics based on filtering, or by using relevancy weights and price data were used to calculate three measures of returns:
- `daily_returns` (%) $ = \frac{close_{t} - close_{t-1}}{close_{t-1}} \times 100\% $
- `overnight_returns` (%) $ = \frac{close_{t+1} - close_{t}}{close_{t}}  \times 100\% $ 
- `intraday_returns` (%) $ = \frac{close_{t} - open_{t}}{open_{t}}  \times 100\% $
This allowed 6 combinations of daily sentiment and return metrics to be analysed.

With both datasets aligned to a daily measure, two main statistical methods were employed to investigate the relationship between financial news sentiment and stock returns:
1. Correlation analysis

    A correlation analysis was carried out by computing both the Pearson correlation coefficients and Spearman's rank correlation coefficients of all 6 combinations. The Pearson correlation was used to confirm a linear relationship between the two metrics, while the Spearman's rank correlation was used as a robustness check to measure some level of monotonic relationship. Results from my own testing justified proceeding to the regression analysis.
2. Ordinary-Least-Squares Regression

    An OLS regression was carried out with daily sentiment as the independent variable and daily returns as the dependent variable, as seen in the following formula:

      $ r_{t} = \alpha + \beta \times s_{t} + \epsilon_{t} $

    where
    - $ r_{t}$ denotes the return at day $t$
    - $\alpha$ denotes the intercept
    - $\beta$ denotes the coefficient of sentiment on returns
    - $s_{t}$ denotes the sentiment at day $t$
    - $\epsilon_{t}$ denotes the error term at day $t$


## 4. The Results

As a whole, the analysis revealed statistically significant relationships between news sentiment and stock returns across all three stocks.
While the statistical significance for correlation and regression calculations were relatively widespread (p < 0.05 for almost all combinations), the effect sizes varied considerably among the three stocks. 

|Stock|Best Combination|Pearson's Correlation|P-value|$R^2$| 
|:-:|:-:|:-:|:-:|:-:|
|**Tesla (TSLA)**|Filtered Sentiment + Daily Returns|0.308|4.39E-06|0.095|
|**Nvidia (NVDA)**|Weighted Sentiment + Daily Returns|0.166|0.020|0.028|
|**GameStop (GME)**|Weighted Sentiment + Daily Returns|0.271|0.003|0.073|

These results are based on approximately 200 daily observations for TSLA and NVDa and 115 for GME.

Throughout all tests, Tesla consistently demonstrated the strongest correlations between its price movements and media sentiment, with filtered sentiment explaining 9.05% of the variance of its daily returns. Furthermore, Tesla often showed order-of-magnitude better p-values, when compared to GameStop and especially Nvidia.
Slightly behind Tesla, GameStop showed a relatively strong relationship between the two variables, with weighted sentiment explaining 7.3% of the variance in daily returns, with decent p values to support its significance.
Out of the three, the calculations consistently show Nvidia price movements being the most resistant to news sentiment. Weighted sentiment explained only 2.8% of daily returns variance. For all combinations, measures of correlation were also almost always the lowest, with higher p values relative to the others.

While the $R^2$ values observed in the analysis appear modest, they are consistent with established understanding in financial economics. Stock returns are influenced by a number of factors including market movements, macroeconomic releases, and company-specific announcements. In this context, sentiment explaining a small percentage of daily return variance, can represent a significant and meaningful relationship.

The analysis revealed consistent patterns in the relative performance of different metric combinations. For a measure of sentiment, both filtered and weighted sentiment metrics produced generally similar results across the three stock, with weighted sentiment showing slightly stronger correlation and significance in most cases. Thus, it is likely that both metrics can capture similar sentiment signals.

For return metrics, a clear hierarchy emerged. Daily returns consistently showed the strongest relationships with sentiment, with intraday returns showing generally weaker, but mostly significant correlations in several cases.
A consistent negative result of the analysis was the correlation coefficient of the overnight returns. All three stocks showed non-significant (p > 0.05), near 0, relationships for overnight returnn. This may suggest that the influence of news sentiment may be temporallly constrained to trading hours, possibly as market participants mostly react when liquidity is at its highest.

While for most combinations, the two measures of correlation employed (Pearson's Correlation and Spearman's Rank Correlation) displayed similar patterns accross the three stocks, a notable pattern also emerged: Spearman's rank correlation demonstrated slightly stronger relationships than the Pearson's correlation.
For instance, GameStop's daily returns showed Pearson r = 0.27 (p = 0.003), while Spearman $\rho$ = 0.35 (p = 1.26E-4). This pattern, although slightly less pronounce was also present for Nvidia and Tesla as well. These results suggest the sentiment-return relationship may be better characterised as monotonic rather than strictly linear, particularly for stock with more volatile returns like GameStop.

## 5. The Limitations
While the results provdie considerable insights into the relationship between financial news sentiment and stock returns, several limitations of this project should be acknowledged.
The analysis relied exclusively on Finnhub for news data which constrained the study in three key aspects:
1. The temporal scope of the stocks to be studied is limited to one year of historical data, using the free plan.
2. The summary-based content may lack the full nuance of individual articles.
3. There is incomplete media source coverage, especially in regards to paywalled sources.
Methodologically, the analysis focused on three selected stocks. Insights gained from these stocks may not be generalisable and extend to other stocks.
For improvement, future research could address these limitations by expanding the temporal scope, incorporating several news sources and testing a wider range of securities.

## 6. The Conclusion

This project developed a pipeine to test the relationship between financial news sentiment and stock returns. Our analysis establishes a statistically significant relationship between these factors, and, although the strength of these relationships are modest in absolute values, sentiment analysis may provide meaningful insights into market behaviour, potentially serving as a complementary tool alongside traditional financial indicators.

The most compelling finding was the superior performance of sentiment analysis for Tesla (TSLA), where news sentiment explained roughly 9.5% of the daily return variance, compared to Nvidia's 2.8% and GameStop's 7.3%.

Methodologically, this project demonstrated that daily returns provide the strongest relationship with news sentiment, while overnight returns proved to consistently show non-significiant relationships across the three studied stocks. This highlights how the efficacy of sentiment analysis may be confined to active trading hours, when market participants can qucikly react to new information. Spearman correlations also reveal that the sentiment-return relationship may be better classified as monotonic rather than strictly linear.

While there are limitations in data scope and coverage that constrain broader generalisations, this study provides evidence that transformer-based sentiment analysis of financial news can offer valuable insight for quantitative financ applications.

Future work could build upon this by incorporating more data sources, expand temporal scope, and testing a greater spectrum of diverse securties to further refine understanding of the complex relationship between sentiment and market movements.

Ultimately, the analysis demonstrates significant correlations between financial news sentiment and returns, establishing true predictive capability would require further testing of trading strategies. Nevertheless, the results provide meaningful evidence that news sentiment contains valuable signals worthy of future investigation.

## 7. References
### Data Sources
- [Finnhub API](https://finnhub.io/) - for news data
- [Yahoo Finance](https://uk.finance.yahoo.com/) - for stock price data via `yfinance`
### NLP Models
- [en_core_web_trf (spaCy)](https://spacy.io/) - for sentiment analysis
- [ProsusAI/FinBERT](https://huggingface.co/ProsusAI/finbert) - for relevancy calculations




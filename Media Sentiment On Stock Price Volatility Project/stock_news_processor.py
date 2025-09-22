import finnhub
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import torch
import datetime as dt
import spacy
import os
from collections import Counter
from ratelimit import limits, sleep_and_retry

class StockNewsProcessing:
    def __init__(self, api_key, nlp, relevance_threshold):
        self.finnhub_client = finnhub.Client(api_key=api_key)
        self.nlp = spacy.load(nlp)
        self.sentiment_tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
        self.sentiment_model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
        

    @sleep_and_retry
    @limits(calls=60, period=60)
    def get_stock_news(self, ticker, start_date, end_date):
        """Returns all news for a ticker in a DataFrame using Finnhub API"""
        stock = ticker
        news_data = []
        batch_start = start_date
        while batch_start <= end_date:
            batch_end = batch_start + dt.timedelta(days=6)
            batch = self.finnhub_client.company_news(stock, _from=batch_start, to=(batch_end))
            news_data.extend(batch)
            batch_start += dt.timedelta(days=7)
        
        df = pd.DataFrame(news_data)

        return df

    def clean_data(self, df):
        """Cleans Dataframe"""
        df = df.rename(columns={"datetime": "date"})
        df = df[df["date"] > 0]
        df["date"] = pd.to_datetime(df["date"], unit="s", errors="coerce")
        df["date"] = df["date"].dt.date
        df.sort_values(by="date", ascending=True, inplace=True)
        df = df[["date", "headline", "summary", "source"]]
        df.replace("", pd.NA, inplace=True)
        df.dropna(inplace=True)
        df.drop_duplicates(subset=["headline", "summary"], inplace=True)
        df["headline"] = df["headline"].fillna("")
        df["summary"] = df["summary"].fillna("")

        return df
    
    
    def calculate_relevance(self, df, target_ents, alpha = 0.67, beta = 0.33):
        """Returns relevance"""
        separator = "\uFFFF"
        article = [f"{headline} {separator} {summary}" for headline, summary in zip(df["headline"], df["summary"])]
        docs = self.nlp.pipe(article)


        relevance_scores = []
        mentioned_entities = []
        for doc in docs:
            separator_index = doc.text.find(separator)

            headline_ents = [ent.text for ent in doc.ents if ent.start_char < separator_index and ent.label_ in {"ORG"}]
            h_counts = Counter(headline_ents)
            h_target_count = sum(h_counts[ent] for ent in h_counts if ent in target_ents)

            summary_ents = [ent.text for ent in doc.ents if ent.start_char > separator_index and ent.label_ in {"ORG"}]
            s_counts = Counter(summary_ents)
            s_target_count = sum(s_counts[ent] for ent in s_counts if ent in target_ents)

            target_scoring = (alpha * h_target_count + beta * s_target_count)
            
            total_ent_scoring = (alpha * sum(h_counts.values()) + beta * sum(s_counts.values())) 

            mentioned_entities.append([ent.text for ent in doc.ents if ent.label_ in ("ORG")])
            relevance = target_scoring/total_ent_scoring if total_ent_scoring > 0 else 0
            relevance_scores.append(round(relevance, 4))
            
            

        df["relevance"] = relevance_scores
        df["entities"] = mentioned_entities

        return df
    
    def calculate_finbert_sentiment(self, text):
        tokenized_text = self.sentiment_tokenizer(text, return_tensors="pt", truncation=True, max_length=512)

        with torch.no_grad():
            output = self.sentiment_model(**tokenized_text)
        labels = ["positive", "negative", "neutral"]
        
        sentiment_scores = softmax(output.logits.numpy()[0])

        return {label: float(score) for label, score in zip(labels, sentiment_scores)}

        
    def assign_sentiment_score(self, df):
        """assigns sentiment scores to each article"""
        df[["positive", "negative", "neutral"]] = (df["headline"] + df["summary"]).apply(lambda text: pd.Series(self.calculate_finbert_sentiment(text)))
        df["sentiment_score"] = df["positive"] - df["negative"] # positive * 1 + negative * - 1 + neutral * 0
        
        return df
    
    def process_ticker(self, ticker, target_ents, start_date, end_date):
        """Full pipeline for stock news data"""
        news_data = self.get_stock_news(ticker, start_date, end_date)
        print(f"{ticker} news data retrieved from finnhub API...")
        if not news_data.empty:
            news_data = self.clean_data(news_data)
            print(f"{ticker} news data cleaned...")
            news_data = self.calculate_relevance(news_data, target_ents)
            print(f"{ticker} news relevancy calculated...")
            news_data = self.assign_sentiment_score(news_data)
            print(f"{ticker} sentiment scores calculated...")
            

        return news_data







































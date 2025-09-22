# src/processing/sentiment_processor.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import torch
import pandas as pd

class SentimentProcessor:

    def __init__(self):
        # loads the FinBERT model for sentiment analysis
        print("Loading FinBERT model...")
        self.sentiment_tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
        self.sentiment_model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
        print("Model successfully loaded...")
        

    def calculate_finbert_sentiment(self, text):
        # Tokenizes the text for the model to analyse. Truncates to 512 tokens
        tokenized_text = self.sentiment_tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        # Ensures gradients are not calculated to increase performance
        with torch.no_grad():
            output = self.sentiment_model(**tokenized_text)

        # converts logit outputs into percentages summing to 100% denoting the likelihood of sentiment label 
        sentiment_scores = softmax(output.logits.numpy()[0])
        labels = ["positive", "negative", "neutral"]

        return {label: float(score) for label, score in zip(labels, sentiment_scores)}

        
    def assign_sentiment_score(self, news_data):
        """assigns sentiment scores to each article"""
        print("Calculating sentiment scores...")
        news_data[["positive", "negative", "neutral"]] = (news_data["headline"] + news_data["summary"]).apply(lambda text: pd.Series(self.calculate_finbert_sentiment(text)))
        news_data["sentiment_score"] = news_data["positive"] - news_data["negative"] # positive * 1 + negative * - 1 + neutral * 0
        print("Sentiment scores calulated...")
        return news_data
    
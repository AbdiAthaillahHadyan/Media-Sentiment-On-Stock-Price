import spacy
from config import settings
import pandas as pd
from collections import Counter

from config import settings

class RelevanceProcessor:
    def __init__(self):
        # loads Named Entity Recognition Model
        self.ner = spacy.load(settings.NER_MODEL)

    def calculate_relevance(self, news_data, aliases, alpha = settings.ALPHA, beta = settings.BETA):
        """Returns relevance"""
        # creates a list of texts consisting of headlines and summaries separated for the named entity recognition model
        separator = "\uFFFF"
        texts = [f"{headline} {separator} {summary}" for headline, summary in zip(news_data["headline"], news_data["summary"])]
        # creates docs from text for analysis
        docs = self.ner.pipe(texts)

        relevance_scores = []
        mentioned_entities = []
        for doc in docs:
            # finds the index of the separator
            separator_index = doc.text.find(separator)

            # gets all mentioned entities under the label ORG into a list
            headline_ents = [ent.text for ent in doc.ents if ent.start_char < separator_index and ent.label_ in {"ORG"}]
            summary_ents = [ent.text for ent in doc.ents if ent.start_char > separator_index and ent.label_ in {"ORG"}]

            # gets the number of times each entity is mentioned, counting the total mentions of the target entity
            h_counts = Counter(headline_ents)
            h_target_count = sum(h_counts[ent] for ent in h_counts if ent in aliases)
            s_counts = Counter(summary_ents)
            s_target_count = sum(s_counts[ent] for ent in s_counts if ent in aliases)

            # calculates relevancy scoring based on alpha and beta and mentions of target entity
            target_scoring = (alpha * h_target_count + beta * s_target_count) 
            total_ent_scoring = (alpha * sum(h_counts.values()) + beta * sum(s_counts.values())) 

            mentioned_entities.append([ent.text for ent in doc.ents if ent.label_ in ("ORG")])
            relevance = target_scoring/total_ent_scoring if total_ent_scoring > 0 else 0
            relevance_scores.append(round(relevance, 4))

        news_data["relevance"] = relevance_scores
        news_data["entities"] = mentioned_entities

        return news_data
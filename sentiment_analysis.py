from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
import datetime
import pathlib
import json
import os
import torch
import matplotlib.pyplot as plt
import psutil


class sentiment_analysis:

    analyzer = None
    updataed_analyzer = None
    tokenizer = None
    finbert_model = None

    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
        self.updataed_analyzer = SentimentIntensityAnalyzer()
        # Update VADER lexicon with new words from file vader_lexicon.csv
        new_words = {}
        with open('./vader_lexicon.csv', 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    # each file contains Word, Score, Word, Score, Word, Score, Word, Score
                    pairs = line.split(' ')
                    for i in range(0, len(pairs), 2):
                        new_words[pairs[i]] = float(pairs[i+1])
        self.updataed_analyzer.lexicon.update(new_words)
        # Load finbert model
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")
        self.tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
        self.finbert_model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert").to(self.device)

    def get_sentiment(self, text):
        return self.analyzer.polarity_scores(text)["compound"]
    
    def get_updated_sentiment(self, text):
        return self.updataed_analyzer.polarity_scores(text)["compound"]

    def get_finbert_sentiment(self, df_list, chunk_size=16):
        num_chunks = (len(df_list) + chunk_size - 1) // chunk_size
        all_predictions = []
        for i in range(num_chunks):

            start_idx = i * chunk_size
            end_idx = min((i+1) * chunk_size, len(df_list))
            chunk = df_list[start_idx:end_idx]
            # Tokenize text_list
            inputs = self.tokenizer(chunk, padding = True, truncation = True, return_tensors='pt').to(self.device)
            # Predict sentiment
            outputs = self.finbert_model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1).cpu().detach()
            positive = predictions[:, 0].cpu().detach().tolist()
            negative = predictions[:, 1].cpu().detach().tolist()
            neutral = predictions[:, 2].cpu().detach().tolist()
            finBert_score = [positive[i] - negative[i] for i in range(len(positive))]
            all_predictions.extend(finBert_score)
        
        return all_predictions

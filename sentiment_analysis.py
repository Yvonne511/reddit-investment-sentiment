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
        self.tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
        self.finbert_model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

    def get_sentiment(self, text):
        return self.analyzer.polarity_scores(text)["compound"]
    
    def get_updated_sentiment(self, text):
        return self.updataed_analyzer.polarity_scores(text)["compound"]

    def get_finbert_sentiment(self, df_list, chunk_size=25):
        num_chunks = (len(df_list) + chunk_size - 1) // chunk_size
        all_predictions = []
        for i in range(num_chunks):

            start_idx = i * chunk_size
            end_idx = min((i+1) * chunk_size, len(df_list))
            chunk = df_list[start_idx:end_idx]
            # Tokenize text_list
            inputs = self.tokenizer(chunk, padding = True, truncation = True, return_tensors='pt')
            # Predict sentiment
            outputs = self.finbert_model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            positive = predictions[:, 0].tolist()
            negative = predictions[:, 1].tolist()
            neutral = predictions[:, 2].tolist()
            finBert_score = [positive[i] - negative[i] for i in range(len(positive))]
            all_predictions.extend(finBert_score)
        
        return all_predictions

sa = sentiment_analysis()
df_comments = pd.DataFrame(columns = ['Sentiment_Score', 'Updated_Sentiment_Score', 'Date'])
cwd = os.getcwd()
target_dir = os.path.join(cwd, 'data', 'cleaned_data', 'gme')
file_path_array = []
for filepath in pathlib.Path(target_dir).glob('**/*'):
    if filepath.is_file():
        file_path_array.append(filepath.relative_to(cwd).as_posix())

chunk_size = 1000
for file_path in file_path_array:
    df = pd.DataFrame(columns = ['Sentiment_Score', 'Updated_Sentiment_Score', 'Date'])
    list = []
    file_path = os.path.join(cwd, file_path)
    df_chunks = pd.read_csv(file_path, chunksize=chunk_size)
    for chunk in df_chunks:
        for index, row in chunk.iterrows():
            row['text'] = str(row['text'])
            list.append(row['text'])
            sentiment_scrore = sa.get_sentiment(row['text'])
            updated_sentiment_scrore = sa.get_updated_sentiment(row['text'])
            row['date'] = datetime.datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S')
            df.loc[len(df)] = [sentiment_scrore, updated_sentiment_scrore, str(row['date'])]
    print(df.shape)
    print(file_path + ' finished')
    # df = pd.concat(chunks, axis=0)

    # df_list = df['text'].tolist()
    # # Get sentiment score
    # # df['FinBert_Sentiment_Score'] = sa.get_finbert_sentiment(df_list)[:, 2].tolist()
    # df['Sentiment_Score'] = df['text'].apply(sa.get_sentiment)
    # df['Updated_Sentiment_Score'] = df['text'].apply(sa.get_updated_sentiment)
    # df['Date'] = df['date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
    # print(sa.get_finbert_sentiment(df_list))

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import datetime
import pathlib
import json
import os
import matplotlib.pyplot as plt

class sentiment_analysis:

    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def get_sentiment(self, text):
        return self.analyzer.polarity_scores(text)["compound"]

def getSubmissionSentimentScore():
    ## Part 1: Generate Sentiment Score for each submission
    cwd = os.getcwd()
    target_dir = os.path.join(cwd, 'data', 'gamestop', 'submissions')
    file_path_array = []
    df_submissions = pd.DataFrame()
    # Get all the files in dir
    print(target_dir)
    for filepath in pathlib.Path(target_dir).glob('**/*'):
        if filepath.is_file():
            file_path_array.append(filepath.relative_to(cwd).as_posix())
    for file_path in file_path_array:
        file_path = os.path.join(cwd, file_path)
        df = pd.read_csv(file_path)
        df['Sentiment_Score'] = df['body'].apply(lambda x: sentiment_analysis().get_sentiment(x))
        df["Date"] = df["utc_datetime_str"].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
        df.drop(columns=['utc_datetime_str', 'body'], inplace=True)
        df_submissions = pd.concat([df_submissions, df], ignore_index=True)
    print(df_submissions.shape)
    df_submissions.to_csv('./wsb_sentiment.csv', index=False)

df = pd.read_csv('./wsb_sentiment.csv')
df["Date"] = df["Date"].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
df.sort_values(by=['Date'], inplace=True)
df.set_index('Date', inplace=True)
df = df.resample('T').sum(numeric_only=True)
df.plot()
plt.show()

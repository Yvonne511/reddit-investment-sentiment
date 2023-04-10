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

df_comments = pd.DataFrame(columns = ['Sentiment_Score', 'Date'])

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

def getCommentSentimentScore():
    ## Part 1: Generate Sentiment Score for each submission
    total_count = 0
    cwd = os.getcwd()
    target_dir = os.path.join(cwd, 'data', 'gamestop', 'comments')
    file_path_array = []
    # Get all the files in dir
    # print(target_dir)
    for filepath in pathlib.Path(target_dir).glob('**/*'):
        if filepath.is_file():
            file_path_array.append(filepath.relative_to(cwd).as_posix())
    for file_path in file_path_array:
        file_path = os.path.join(cwd, file_path)
        with open(filepath, 'r') as f:
            first_line = f.readline().strip()
            count_str = first_line.split(': ')[-1]
            count = int(count_str)
            total_count += count

            # Read rest of file as JSON Array
            json_list = (''.join(f.readlines())).strip().split('\n')
            for json_obj in json_list:
                data = json.loads(json_obj)
                comments = data['comments']
                for comment in comments:
                    df_comments.loc[len(df_comments)] = [sentiment_analysis().get_sentiment(comment['text']), comment['time']]
                    tranverseComments(comment)

def tranverseComments(commentObj):
    if len(commentObj['comments']) > 0:
        for comment in commentObj['comments']:
            df_comments.loc[len(df_comments)] = [sentiment_analysis().get_sentiment(comment['text']), comment['time']]
            tranverseComments(comment)
    else:
        return
    
def getLayeredCommentSentimentScore():
    getCommentSentimentScore()
    print(df_comments.shape)
    df_comments["Date"] = df_comments["Date"].apply(lambda x: datetime.datetime.fromtimestamp(x))
    df_comments.sort_values(by=['Date'], inplace=True)
    df_comments.to_csv('./wsb_comment_sentiment.csv', index=False)

# Read JSON file and convert to dataframe
df_gme = pd.DataFrame()
with open('./GME.json') as f:
    gme = json.load(f)
    df_gme = pd.json_normalize(gme)
df_gme['Date'] = df_gme['datetime'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
df_gme['close'] = df_gme['close'].apply(lambda x: float(x))
df_gme.drop(columns=['datetime'], inplace=True)
df_gme = df_gme[df_gme['Date'] >= '2021-01-25']
df_gme = df_gme[df_gme['Date'] <= '2021-02-05']
df_gme.sort_values(by=['Date'], inplace=True)
df_gme.set_index('Date', inplace=True)
print(df_gme.head())

df = pd.read_csv('./wsb_sentiment_resampled.csv')
df_comments = pd.read_csv('./wsb_comment_sentiment.csv')
df["Date"] = df["Date"].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
df["Sentiment_Score"] = df["Sentiment_Score"].apply(lambda x: float(x)*200)
df_comments["Date"] = df_comments["Date"].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
df = pd.concat([df, df_comments], ignore_index=True)
df = df[df['Date'] >= '2021-01-25']
df = df[df['Date'] <= '2021-02-05']
df.sort_values(by=['Date'], inplace=True)
df.set_index('Date', inplace=True)
df = df.resample('T').sum(numeric_only=True)

# Left join the two dataframes on Date
df = df.join(df_gme, how='left')

print(df.shape)
print(df.head(10))

df.plot()
plt.show()

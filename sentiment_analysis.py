from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import datetime
import pathlib
import json
import os
import matplotlib.pyplot as plt

class sentiment_analysis:

    df_comments = pd.DataFrame(columns = ['Sentiment_Score', 'Updated_Sentiment_Score', 'Date'])
    df_submissions = pd.DataFrame(columns = ['Sentiment_Score', 'Updated_Sentiment_Score', 'Date'])
    analyzer = None
    updataed_analyzer = None

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

    def get_sentiment(self, text):
        return self.analyzer.polarity_scores(text)["compound"]
    
    def get_updated_sentiment(self, text):
        return self.updataed_analyzer.polarity_scores(text)["compound"]

    def getCommentSentimentScore(self, filename):
        ## Part 1: Generate Sentiment Score for each submission
        # cwd = os.getcwd()
        # target_dir = os.path.join(cwd, 'data', 'gme&gamestop', 'comments', 'chunk_group1')
        # file_path_array = []
        # # Get all the files in dir
        # # print(target_dir)
        # for filepath in pathlib.Path(target_dir).glob('**/*'):
        #     if filepath.is_file():
        #         file_path_array.append(filepath.relative_to(cwd).as_posix())
        file_path_array = [filename]
        for file_path in file_path_array:
            # file_path = os.path.join(cwd, file_path)
            with open(file_path, 'r') as f:
                json_list = (''.join(f.readlines())).strip().split('\n')
                for json_obj in json_list:
                    data = json.loads(json_obj)
                    if 'to the moon' in comment['text']:
                        # replce 'to the moon' with 'to_the_moon'
                        comment['text'] = comment['text'].replace('to the moon', 'to_the_moon')
                        comment['time'] = datetime.datetime.fromtimestamp(comment['time'])
                        self.df_comments.loc[len(self.df_comments)] = [self.get_sentiment(comment['text']), self.get_updated_sentiment(comment['text']), comment['time']]
                    comments = data['comments']
                    for comment in comments:
                        self.tranverseComments(comment)

    def tranverseComments(self, commentObj):
        if len(commentObj['comments']) > 0:
            for comment in commentObj['comments']:
                if 'to the moon' in comment['text']:
                    # replce 'to the moon' with 'to_the_moon'
                    comment['text'] = comment['text'].replace('to the moon', 'to_the_moon')
                comment['time'] = datetime.datetime.fromtimestamp(comment['time'])
                self.df_comments.loc[len(self.df_comments)] = [self.get_sentiment(comment['text']), self.get_updated_sentiment(comment['text']), comment['time']]
                self.tranverseComments(comment)
        else:
            return

# Read JSON file and convert to dataframe
# df_gme = pd.DataFrame()
# with open('./GME.json') as f:
#     gme = json.load(f)
#     df_gme = pd.json_normalize(gme)
# df_gme['Date'] = df_gme['datetime'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
# df_gme['close'] = df_gme['close'].apply(lambda x: float(x))
# df_gme.drop(columns=['datetime'], inplace=True)
# df_gme = df_gme[df_gme['Date'] >= '2021-01-25']
# df_gme = df_gme[df_gme['Date'] <= '2021-02-05']
# df_gme.sort_values(by=['Date'], inplace=True)
# df_gme.set_index('Date', inplace=True)
# print(df_gme.head())

sa = sentiment_analysis()
cwd = os.getcwd()
target_dir = os.path.join(cwd, 'data', 'all_reddit_gme&gamestop', 'comments')
file_path_array = []
for filepath in pathlib.Path(target_dir).glob('**/*'):
    if filepath.is_file():
        file_path_array.append(filepath.relative_to(cwd).as_posix())
i = 0
for file_path in file_path_array:
    file_path = os.path.join(cwd, file_path)
    sa.getCommentSentimentScore(file_path)
    print("file processed: " + file_path)
    df_comments = sa.df_comments
    print(df_comments.head())
    df_comments.to_csv('./data/gme_sentiment_score/'+str(i)+'.csv', index=False)
    i += 1

# df = pd.read_csv('./wsb_sentiment_resampled.csv')
# df_comments = pd.read_csv('./wsb_comment_sentiment.csv')
# df["Date"] = df["Date"].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
# df["Sentiment_Score"] = df["Sentiment_Score"].apply(lambda x: float(x)*200)
# df_comments["Date"] = df_comments["Date"].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
# df = pd.concat([df, df_comments], ignore_index=True)
# df = df[df['Date'] >= '2021-01-25']
# df = df[df['Date'] <= '2021-02-05']
# df.sort_values(by=['Date'], inplace=True)
# df.set_index('Date', inplace=True)
# df = df.resample('T').sum(numeric_only=True)

# # Left join the two dataframes on Date
# df = df.join(df_gme, how='left')

# print(df.shape)
# print(df.head(10))

# df.plot()
# plt.show()

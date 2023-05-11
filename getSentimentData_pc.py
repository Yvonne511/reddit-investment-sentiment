import os
import pathlib
import json
import pandas as pd
import datetime
import psutil
# import sentiment analysis class from sentiment_analysis.py
from sentiment_analysis import sentiment_analysis

import multiprocessing as mp

from mpi4py import MPI

class sentiment_analysis_implement:

    df_comments = pd.DataFrame(columns = ['Sentiment_Score', 'Updated_Sentiment_Score', 'Fintech_Sentiment_Score', 'Date'])
    df_comments['Date'] = pd.to_datetime(df_comments['Date'])
    temp_comments = pd.DataFrame(columns = ['Sentiment_Score', 'Updated_Sentiment_Score', 'Fintech_Sentiment_Score', 'Date'])
    temp_comments['Date'] = pd.to_datetime(temp_comments['Date'])
    df_list = []
    sa = sentiment_analysis()
    k = 0

    def tranverseComments(self, commentObj):
        commentObj['text'] = commentObj['text'].replace('to the moon', 'to_the_moon')
        commentObj['time'] = datetime.datetime.fromtimestamp(commentObj['time'])
        if commentObj['text'] != '' and commentObj['text'] != '[deleted]' and commentObj['text'] != '[removed]':
            sentiment_score = self.sa.get_sentiment(commentObj['text'])
            updated_sentiment_score = self.sa.get_updated_sentiment(commentObj['text'])
            self.df_list.append(commentObj['text'])
            self.temp_comments.loc[len(self.temp_comments)] = [sentiment_score, updated_sentiment_score, 0, commentObj['time']]
        if len(commentObj['comments']) > 0:
            for comment in commentObj['comments']:
                self.tranverseComments(comment)
        else:
            return
    
    def getSentimentData(self, file_path):
        file_name = file_path.split('/')[-1].split('.')[0]
        cwd = os.getcwd()
        file_path = os.path.join(cwd, file_path)
        with open(file_path, 'r') as f:
            json_list = (''.join(f.readlines())).strip().split('\n')
            for json_obj in json_list:
                data = json.loads(json_obj)
                data['text'] = data['text'].replace('to the moon', 'to_the_moon')
                data['title'] = data['title'].replace('to the moon', 'to_the_moon')
                data['time'] = datetime.datetime.fromtimestamp(data['time'])
                if data['text'] != '' and data['text'] != '[deleted]' and data['text'] != '[removed]':
                    sentiment_score = self.sa.get_sentiment(data['text'] + ' ' + data['title'])
                    updated_sentiment_score = self.sa.get_updated_sentiment(data['text'] + ' ' + data['title'])
                    self.df_list.append(data['text'] + ' ' + data['title'])
                    self.temp_comments.loc[len(self.temp_comments)] = [sentiment_score, updated_sentiment_score, 0, data['time']]
                else:
                    sentiment_score = self.sa.get_sentiment(data['title'])
                    updated_sentiment_score = self.sa.get_updated_sentiment(data['title'])
                    self.df_list.append(data['title'])
                    self.temp_comments.loc[len(self.temp_comments)] = [sentiment_score, updated_sentiment_score, 0, data['time']]
                comments = data['comments']
                for comment in comments:
                    self.tranverseComments(comment)
                print(self.temp_comments.shape)
                finbert_sentiment_score = self.sa.get_finbert_sentiment(self.df_list)
                print(finbert_sentiment_score)
                self.df_list = []
                self.temp_comments['Fintech_Sentiment_Score'] = finbert_sentiment_score
                self.df_comments = pd.concat([self.df_comments, self.temp_comments])
                self.temp_comments = pd.DataFrame(columns = ['Sentiment_Score', 'Updated_Sentiment_Score', 'Fintech_Sentiment_Score', 'Date'])
        print('file_path: ', file_path, ' finished')
        self.df_comments.to_csv('data/cleaned_data/gme/'+ str(file_name)+'.csv', index=False)
        self.df_comments = pd.DataFrame(columns = ['Sentiment_Score', 'Updated_Sentiment_Score', 'Fintech_Sentiment_Score', 'Date'])

# Parallel Processing of each file
def parallelProcessing(file_path):
    sai = sentiment_analysis_implement()
    sai.getSentimentData(file_path)

# if __name__ == '__main__':
#     num_processes = 2
#     cwd = os.getcwd()
#     target_dir = os.path.join(cwd, 'data', 'all_reddit_gme&gamestop', 'comments')
#     file_path_array = []
#     for filepath in pathlib.Path(target_dir).glob('**/*'):
#         if filepath.is_file():
#             file_path_array.append(filepath.relative_to(cwd).as_posix())
#     print(file_path_array)
#     pool = mp.Pool(num_processes)
#     sai = sentiment_analysis_implement()
#     pool.map(sai.getSentimentData, file_path_array)
#     print('Finished')

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
host = os.uname()[1]
print(f"hello from process {rank} on host {host}")
cwd = os.getcwd()
target_dir = os.path.join(cwd, 'data', 'all_reddit_gme&gamestop', 'comments')
file_path_array = []
# for filepath in pathlib.Path(target_dir).glob('**/*'):
#     if filepath.is_file():
#         file_path_array.append(filepath.relative_to(cwd).as_posix())
file_path_array = ['data/all_reddit_gme&gamestop/comments/chunk_19.txt', 'data/all_reddit_gme&gamestop/comments/chunk_10.txt', 'data/all_reddit_gme&gamestop/comments/chunk_17.txt', 'data/all_reddit_gme&gamestop/comments/chunk_1.txt', 'data/all_reddit_gme&gamestop/comments/chunk_6.txt', 'data/all_reddit_gme&gamestop/comments/chunk_8.txt', 'data/all_reddit_gme&gamestop/comments/chunk_16.txt', 'data/all_reddit_gme&gamestop/comments/chunk_11.txt', 'data/all_reddit_gme&gamestop/comments/chunk_18.txt', 'data/all_reddit_gme&gamestop/comments/chunk_9.txt', 'data/all_reddit_gme&gamestop/comments/chunk_7.txt', 'data/all_reddit_gme&gamestop/comments/chunk_3.txt', 'data/all_reddit_gme&gamestop/comments/chunk_4.txt', 'data/all_reddit_gme&gamestop/comments/chunk_12.txt', 'data/all_reddit_gme&gamestop/comments/chunk_15.txt', 'data/all_reddit_gme&gamestop/comments/chunk_20.txt', 'data/all_reddit_gme&gamestop/comments/chunk_5.txt', 'data/all_reddit_gme&gamestop/comments/chunk_2.txt', 'data/all_reddit_gme&gamestop/comments/chunk_14.txt', 'data/all_reddit_gme&gamestop/comments/chunk_13.txt']
num_files = len(file_path_array)
files_per_core = num_files // size
start_index = rank * files_per_core
end_index = (rank + 1) * files_per_core if rank != size - 1 else num_files
processing_files = file_path_array[start_index:end_index]

for processing_file in processing_files:
    parallelProcessing(processing_file)

MPI.Finalize()

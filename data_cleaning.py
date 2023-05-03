import os
import pathlib
import json
import pandas as pd
import datetime

# Data undertsanding

class data_understanding:

# 1. How many data points are there in total?
    total_data_count = 0
    total_submission_count = 0
    total_comment_count = 0

    deleted_submissions_title_count = 0
    deleted_submissions_count = 0
    deleted_comments_count = 0

    def tranverseComments(self, commentObj):
        self.total_data_count += 1
        self.total_comment_count += 1
        if commentObj['text'] == '' or commentObj['text'] == '[deleted]' or commentObj['text'] == '[removed]':
            self.deleted_comments_count += 1
        if len(commentObj['comments']) > 0:
            for comment in commentObj['comments']:
                self.tranverseComments(comment)
        else:
            return
    
    def countData(self):
        cwd = os.getcwd()
        target_dir = os.path.join(cwd, 'data', 'gme&gamestop', 'comments')
        file_path_array = []
        for filepath in pathlib.Path(target_dir).glob('**/*'):
            if filepath.is_file():
                file_path_array.append(filepath.relative_to(cwd).as_posix())
        for file_path in file_path_array:
            file_path = os.path.join(cwd, file_path)
            with open(file_path, 'r') as f:
                json_list = (''.join(f.readlines())).strip().split('\n')
                for json_obj in json_list:
                    data = json.loads(json_obj)
                    self.total_submission_count += 1
                    self.total_data_count += 1
                    if data['title'] == '' or data['title'] == '[deleted]' or data['title'] == '[removed]':
                        self.deleted_submissions_title_count += 1
                    if data['text'] == '' or data['text'] == '[deleted]' or data['text'] == '[removed]':
                        self.deleted_submissions_count += 1
                    comments = data['comments']
                    for comment in comments:
                        self.tranverseComments(comment)
            print('file_path: ', file_path, ' finished')
        print('total_data_count: ', self.total_data_count)
        print('total_submission_count: ', self.total_submission_count)
        print('total_comment_count: ', self.total_comment_count)
        print('deleted_submissions_title_count: ', self.deleted_submissions_title_count)
        print('deleted_submissions_count: ', self.deleted_submissions_count)
        print('deleted_comments_count: ', self.deleted_comments_count)
            
# du = data_understanding()
# du.countData()

class data_cleaning:

    df_comments = pd.DataFrame(columns = ['text', 'date'])
    df_comments['date'] = pd.to_datetime(df_comments['date'])

    i = 0

    def tranverseComments(self, commentObj):
        commentObj['text'] = commentObj['text'].replace('to the moon', 'to_the_moon')
        commentObj['time'] = datetime.datetime.fromtimestamp(commentObj['time'])
        if commentObj['text'] != '' and commentObj['text'] != '[deleted]' and commentObj['text'] != '[removed]':
            self.df_comments.loc[len(self.df_comments)] = [commentObj['text'], commentObj['time']]
        if len(commentObj['comments']) > 0:
            for comment in commentObj['comments']:
                self.tranverseComments(comment)
        else:
            return
    
    def cleanData(self):
        cwd = os.getcwd()
        target_dir = os.path.join(cwd, 'data', 'all_reddit_gme&gamestop', 'comments')
        file_path_array = []
        for filepath in pathlib.Path(target_dir).glob('**/*'):
            if filepath.is_file():
                file_path_array.append(filepath.relative_to(cwd).as_posix())
        for file_path in file_path_array:
            file_path = os.path.join(cwd, file_path)
            with open(file_path, 'r') as f:
                json_list = (''.join(f.readlines())).strip().split('\n')
                for json_obj in json_list:
                    data = json.loads(json_obj)
                    data['text'] = data['text'].replace('to the moon', 'to_the_moon')
                    data['title'] = data['title'].replace('to the moon', 'to_the_moon')
                    data['time'] = datetime.datetime.fromtimestamp(data['time'])
                    if data['text'] != '' and data['text'] != '[deleted]' and data['text'] != '[removed]':
                        self.df_comments.loc[len(self.df_comments)] = [data['text'] + ' ' + data['title'], data['time']]
                    else:
                        self.df_comments.loc[len(self.df_comments)] = [data['title'], data['time']]
                    comments = data['comments']
                    for comment in comments:
                        self.tranverseComments(comment)
            print('file_path: ', file_path, ' finished')
            self.df_comments.to_csv('data/cleaned_data/all_gme/'+str(self.i)+'.csv', index=False)
            self.i += 1

dc = data_cleaning()
dc.cleanData()
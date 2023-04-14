import pandas as pd
import datetime
import requests
import json
import time

class data_mining_submission:

    def epoch_datatime(self, dt):
        epoch_start = datetime.datetime(1970, 1, 1)
        delta = dt - epoch_start.date()
        epoch_time = delta.days * 86400
        return epoch_time

    def epoch(self, year, month, day):
        dt = datetime.datetime(year, month, day)
        epoch_start = datetime.datetime(1970, 1, 1)
        return int((dt - epoch_start).total_seconds())
    
    def getPushshiftData_Submission(self, query, after, before, sub, size = 500):
        data = None
        while not data:
            try:
                url = 'https://api.pushshift.io/reddit/search/submission?q='+str(query)+'&subreddit='+str(sub)+'&after='+str(after)+'&before='+str(before)+'&size='+str(size)
                print(url)
                r = requests.get(url)
                data = json.loads(r.text)
            except:
                time.sleep(5)
        return data['data']

data_count = 0
start_date = datetime.date(2021, 1, 25)
start_epoch = data_mining_submission().epoch_datatime(start_date)
end_date = datetime.date(2021, 2, 5)
end_epoch = data_mining_submission().epoch_datatime(end_date)
delta = 1800
data = []
over500 = 0
while start_epoch <= end_epoch:
    temp_array = []
    temp_data = data_mining_submission().getPushshiftData_Submission(' GME ', start_epoch, start_epoch+delta, 'wallstreetbets', 500)
    for d in temp_data:
        new_d = {"id":d["id"], "utc_datetime_str":d["utc_datetime_str"], "body":d["selftext"], "title":d["title"], 'upvote_ratio':d['upvote_ratio']}
        temp_array.append(new_d)
    print('Date', start_epoch, 'is Completed.')
    if len(temp_array) == 0:
        print('No Data')
        start_epoch += delta
    else:
        temp_df = pd.DataFrame(temp_array)
        data_count += temp_df.shape[0]
        print('Data Count: ', temp_df.shape[0])
        if temp_df.shape[0] >= 400:
            over500 += 1
            new_delta = 60
            while start_epoch<=start_epoch+delta:
                temp_array = []
                temp_data = data_mining_submission().getPushshiftData_Submission(' GME ', start_epoch, start_epoch+new_delta, 'wallstreetbets', 500)
                for d in temp_data:
                    new_d = {"id":d["id"], "utc_datetime_str":d["utc_datetime_str"], "body":d["selftext"], "title":d["title"], 'upvote_ratio':d['upvote_ratio']}
                    temp_array.append(new_d)
                print('Date', start_epoch, 'is Completed with new delta.')
                if len(data) == 0:
                    print('No Data')
                else:
                    temp_df = pd.DataFrame(temp_array)
                    data_count += temp_df.shape[0]
                    print('Data Count: ', temp_df.shape[0])
                    if temp_df.shape[0] >= 500:
                        print('Over 500 with new delta')
                    else:
                        data.append(temp_df)
                        temp_df = None
                        temp_array = []
                        start_epoch += new_delta
                        break
        else:
            data.append(temp_df)
            temp_df = None
            temp_array = []
            start_epoch += delta
print ('Total Data Count: ', data_count)
print ('Over 500: ', over500)
df = pd.DataFrame(data)
df.to_csv('./data-submission/wsb_submission.csv', index=False)
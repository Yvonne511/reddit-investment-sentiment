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
    
    def getPushshiftData_Submission(self, query, after, length, sub, size = 500):
        data = None
        while not data:
            try:
                url = 'https://api.pushshift.io/reddit/search/submission?q='+str(query)+'&subreddit='+str(sub)+'&after='+str(after)+'&before='+str(after+length)+'&size='+str(size)
                # url = 'https://api.pushshift.io/reddit/search/submission?q='+str(query)+'&after='+str(after)+'&before='+str(after+length)+'&size='+str(size)
                # url = 'https://api.pushshift.io/reddit/search/submission?&subreddit='+str(sub)+'&after='+str(after)+'&before='+str(after+length)+'&size='+str(size)
                print(url)
                r = requests.get(url)
                data = json.loads(r.text)
            except:
                time.sleep(5)
        data = data['data']
        if len(data)>490 and length>3:
            data = self.getPushshiftData_Submission(query, after, int(length/2), sub, 500)
            data += self.getPushshiftData_Submission(query, after+int(length/2), length-int(length/2), sub, 500)
        return data

data_count = 0
start_date = datetime.date(2021, 1, 10)
start_epoch = data_mining_submission().epoch_datatime(start_date)
end_date = datetime.date(2021, 2, 13)
end_epoch = data_mining_submission().epoch_datatime(end_date)
delta = 3600
data = []
over500 = 0
while start_epoch <= end_epoch:
    temp_array = []
    temp_data = data_mining_submission().getPushshiftData_Submission(' GME ', start_epoch, delta, 'wallstreetbets', 500)
    for d in temp_data:
        new_d = {"id":d["id"], "utc_datetime_str":d["utc_datetime_str"], 'upvote_ratio':d['upvote_ratio'], "body":d["selftext"], "title":d["title"]}
        temp_array.append(new_d)
        data.append(new_d)
    print('Date', start_epoch, 'is Completed.')
    if len(temp_array) == 0:
        print('No Data')
    else:
        temp_df = pd.DataFrame(temp_array)
        data_count += temp_df.shape[0]
        print('Data Count: ', temp_df.shape[0])
        if temp_df.shape[0] >= 500:
            over500 += 1         
        temp_df = None
        temp_array = []
    start_epoch += delta
print ('Total Data Count: ', data_count)
print ('Over 500: ', over500)
df = pd.DataFrame(data)
df.to_csv('./data-submission/wsb_submission_5_3_%20GME%20.csv', index=False)
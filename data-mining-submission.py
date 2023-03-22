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
        url = 'https://api.pushshift.io/reddit/search/submission?q='+str(query)+'&subreddit='+str(sub)+'&after='+str(after)+'&before='+str(before)+'&size='+str(size)
        print(url)
        r = requests.get(url)
        data = json.loads(r.text)
        return data['data']

time_period = 60
data_count = 0
start_date = datetime.date(2021, 1, 25)
end_date = datetime.date(2021, 2, 5)
delta = datetime.timedelta(days=1)
current_date = start_date
while current_date <= end_date:
    data = []
    start_epoch=data_mining_submission().epoch_datatime(current_date)
    end_epoch=data_mining_submission().epoch_datatime(current_date+delta)
    current_epoch_by_hour = start_epoch
    while current_epoch_by_hour<=end_epoch:
        temp_data = data_mining_submission().getPushshiftData_Submission('gamestop', current_epoch_by_hour, current_epoch_by_hour+60, 'wallstreetbets', 500)
        current_epoch_by_hour += 60

        for d in temp_data:
            new_d = {"id":d["id"], "utc_datetime_str":d["utc_datetime_str"], "body":d["selftext"]}
            data.append(new_d)

    if len(data) == 0:
            continue
    else:
        df = pd.DataFrame(data)
        data_count += df.shape[0]
        print('Data Count: ', df.shape[0])
        df.to_csv('./data-submission/wsb_'+str(current_date)+'.csv', index=False)
    current_date += delta
print ('Total Data Count: ', data_count)
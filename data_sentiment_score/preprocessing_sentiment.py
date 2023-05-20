import os
import csv
import datetime

folder = "gme"
subfolder = "sentiment_all"

filename_out = subfolder + ".csv"
date_from = "2021-01-24"
date_before = "2021-02-06"

days = set()

start_date = datetime.datetime.strptime(date_from, '%Y-%m-%d')
end_date = datetime.datetime.strptime(date_before, '%Y-%m-%d')
date_format = '%Y-%m-%d'
date_list = []
current_date = start_date
while current_date <= end_date:
    date_list.append(current_date.strftime(date_format))
    current_date += datetime.timedelta(days=1)

score = {}
for day in date_list:
    for i in range(24):
        hour = '{:02d}'.format(i)
        score[day +" "+ hour] = [0,0,0,0,0]
score = dict(sorted(score.items()))

prefix = 13

for filename in os.listdir(os.path.join(folder, subfolder)):
    if filename.endswith('.csv'):
        print("2-" + filename)
        with open(os.path.join(folder, subfolder, filename), 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            next(reader)
            for row in reader:
                if row['Date'][:prefix] in score:
                    if float(row['Sentiment_Score'])>=0:
                        score[row['Date'][:prefix]][0] += float(row['Sentiment_Score'])
                        score[row['Date'][:prefix]][1] += float(row['Updated_Sentiment_Score'])
                    else:
                        score[row['Date'][:prefix]][2] += float(row['Sentiment_Score'])
                        score[row['Date'][:prefix]][3] += float(row['Updated_Sentiment_Score'])

                    score[row['Date'][:prefix]][4] += 1

# for s in score:
#     if score[s][2]:
#         score[s][0] /= score[s][2]
#         score[s][1] /= score[s][2]

with open(os.path.join(folder, filename_out), mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['datetime', 'positive', "updated_positive", 'negative', "updated_negative"])
    for s in score:
        writer.writerow([s, str(score[s][0]), str(score[s][1]), str(score[s][2]), str(score[s][3])])



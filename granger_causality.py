import pandas as pd
import numpy as np
import os
import pathlib
import json
import matplotlib.pyplot as plt
import datetime
from statsmodels.tsa.stattools import grangercausalitytests

# Load the data into a pandas dataframe
cwd = os.getcwd()
target_dir = os.path.join(cwd, 'data', 'gme_sentiment_score', 'wellstreetbets_gme')
file_path_array = []
for filepath in pathlib.Path(target_dir).glob('**/*'):
    if filepath.is_file():
        file_path_array.append(filepath.relative_to(cwd).as_posix())
df = pd.DataFrame()
for file_path in file_path_array:
    file_path = os.path.join(cwd, file_path)
    df_temp = pd.read_csv(file_path)
    df = pd.concat([df, df_temp], ignore_index=True)

print(df.shape)
# Sum by minute
df['Date'] = pd.to_datetime(df['Date'])
# Filter time range from 2021, 1, 25 to 2021, 2, 5
df = df[(df['Date'] >= '2021-01-25') & (df['Date'] <= '2021-02-05')]
print(df.shape)
df = df.set_index('Date')
df = df.resample('1T').sum()

# Add a column with closing prices from the stock market
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

df = df.join(df_gme, how='left')
df = df.interpolate(method='linear')
print(df.head())

df = df.fillna(0)

# Check if there is any missing value
print(df.isnull().sum())

# Visualize the data
# fig, ax = plt.subplots(figsize=(12, 6))
# ax.plot(df.index, df['Updated_Sentiment_Score'], color='blue', label='score')
# ax2 = ax.twinx()
# ax2.plot(df.index, df['close'], color='red', label='close')
# ax.legend(loc='upper left')
# ax2.legend(loc='upper right')
# plt.show()

# Compute Granger causality using the statsmodels library
maxlag = 10
test = 'ssr_chi2test'

granger_test = grangercausalitytests(df[['Sentiment_Score', 'close']], maxlag=maxlag, verbose=False)

# Print the p-values for each lag and interpret the results
for lag in range(1, maxlag+1):
    p_value = granger_test[lag][0][test][1]
    print(f"Lag {lag}: p-value = {p_value:.4f}")
    if p_value < 0.05:
        print(f"Lag {lag} is statistically significant.")
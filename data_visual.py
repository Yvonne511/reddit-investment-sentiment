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
target_dir = os.path.join(cwd, 'data', 'gme_sentiment_score', 'allreddit_gme')
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
df_gme['Date'] = pd.to_datetime(df_gme['datetime'], format='%Y-%m-%d %H:%M:%S')
df_gme['close'] = df_gme['close'].apply(lambda x: float(x))
df_gme.drop(columns=['datetime'], inplace=True)
df_gme = df_gme[df_gme['Date'] >= '2021-01-25']
df_gme = df_gme[df_gme['Date'] <= '2021-02-05']
df_gme.sort_values(by=['Date'], inplace=True)
df_gme.set_index('Date', inplace=True)
print(df_gme.head())

df = df.join(df_gme, how='left')
df = df.interpolate(method='linear')

# Get first non NaN value from the close column
first_non_nan = df['close'].iloc[np.where(df['close'].notnull())[0][0]]
df = df.fillna(first_non_nan)
print(df.head())

# # Normalize the sentiment score
df['N_Updated_Sentiment_Score'] = df['Updated_Sentiment_Score'] / df['Updated_Sentiment_Score'].max()
df['N_Sentiment_Score'] = df['Sentiment_Score'] / df['Sentiment_Score'].max()

# print(df.head())

# # Visualize the data
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df.index, df['N_Updated_Sentiment_Score'], color='blue', label='score')
ax2 = ax.twinx()
ax2.plot(df.index, df['close'], color='red', label='close')
ax.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.show()
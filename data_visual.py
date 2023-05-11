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
target_dir = os.path.join(cwd, 'data', 'data_sentiment_score', 'gme_wsb')
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
df = df[(df['Date'] >= '2021-01-10') & (df['Date'] <= '2021-02-13')]
print(df.shape)
df = df.set_index('Date')
df = df.resample('1T').sum()
print(df.head())

# Add a column with closing prices from the stock market
df_gme = pd.DataFrame()
file_path_finance = os.path.join(cwd, 'data', 'finance', 'GME.csv')
df_gme = pd.read_csv(file_path_finance)
df_gme = df_gme.rename(columns={'datetime': 'Date'})
df_gme['Date'] = pd.to_datetime(df_gme['Date'])
df_gme = df_gme.set_index('Date')
print(df_gme.head())

# fill null values of finance

df = df.join(df_gme, how='left')
# df = df.interpolate(method='linear')

# Get first non NaN value from the close column
print(df.isnull().sum())
print(df.head())

# Visualize the data
fig, ax1 = plt.subplots()
ax1.plot(df.index, df['Sentiment_Score'], color='blue')
ax1.set_xlabel('Date')
ax1.set_ylabel('Column 1', color='blue')

ax2 = ax1.twinx()
ax2.plot(df.index, df['close'], color='red')
ax2.set_ylabel('Column 2', color='red')

plt.show()

df.to_csv('./data/final/gme_wsb.csv', index=True)

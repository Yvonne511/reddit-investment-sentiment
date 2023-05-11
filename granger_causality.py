import pandas as pd
import numpy as np
import os
import pathlib
import json
import matplotlib.pyplot as plt
import datetime
from statsmodels.tsa.stattools import grangercausalitytests

cwd = os.getcwd()
file_path = os.path.join(cwd, 'data', 'final', 'gme_wsb.csv')
df = pd.read_csv(file_path)

df = df.interpolate(method='linear')
first_non_nun_close = df['close'][df['close'].first_valid_index()]
df['close'] = df['close'].fillna(value=first_non_nun_close)

df = df.set_index('Date')
df.index = pd.to_datetime(df.index)

# sum up by 10 minutes
resampled = df.resample('1440T').agg({'Sentiment_Score': 'sum', 'Updated_Sentiment_Score': 'sum', 'Fintech_Sentiment_Score': 'sum',  'close': 'mean'})
df = resampled

print(df.columns)

# # Visualize the data
# fig, ax1 = plt.subplots()
# ax1.plot(df.index, df['Sentiment_Score'], color='blue')
# ax1.set_xlabel('Date')
# ax1.set_ylabel('Sentiment Score', color='blue')

# ax2 = ax1.twinx()
# ax2.plot(df.index, df['close'], color='red')
# ax2.set_ylabel('Stock Price', color='red')

# plt.show()


## fourier transform
close_fft = np.fft.fft(np.asarray(df['Sentiment_Score'].tolist()))
fft_df = pd.DataFrame({'fft':close_fft})
fft_df['absolute'] = fft_df['fft'].apply(lambda x: np.abs(x))
fft_df['angle'] = fft_df['fft'].apply(lambda x: np.angle(x))
fft_list = np.asarray(fft_df['fft'].tolist())

for num_ in [5, 10, 15, 20]:
    fft_list_m10= np.copy(fft_list); fft_list_m10[num_:-num_]=0
    df['fourier '+str(num_)]=np.fft.ifft(fft_list_m10)
    
# Visualize the data
# fig, ax1 = plt.subplots()
# ## df[['fourier 5', 'fourier 10', 'fourier 15', 'fourier 20']]
# ax1.plot(df.index, df['fourier 20'], color='blue')
# ax1.set_xlabel('Date')
# ax1.set_ylabel('Sentiment Score', color='blue')

# ax2 = ax1.twinx()
# ax2.plot(df.index, df['close'], color='red')
# ax2.set_ylabel('Close', color='red')

# plt.show()




# # Compute Granger causality using the statsmodels library
# maxlag = 5
# test = 'ssr_chi2test'

# granger_test = grangercausalitytests(df[['Fintech_Sentiment_Score', 'close']], maxlag=maxlag, verbose=False)

# # Print the p-values for each lag and interpret the results
# for lag in range(1, maxlag+1):
#     p_value = granger_test[lag][0][test][1]
#     print(f"Lag {lag}: p-value = {p_value:.5f}")
#     if p_value < 0.05:
#         print(f"Lag {lag} is statistically significant.")
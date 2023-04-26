import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import grangercausalitytests

# Load the data into a pandas dataframe
df = pd.read_csv('data.csv')

# Create a new dataframe with a datetime index that includes all time points
index = pd.date_range(start=df['date'].min(), end=df['date'].max(), freq='S')
df_all_times = pd.DataFrame(index=index)

# Merge the two columns into the new dataframe using outer join
df_all_times = df_all_times.join(df.set_index('date')[['stock_price']], how='outer')
df_all_times = df_all_times.join(df.set_index('date')[['other_column']], how='outer')

# Use linear interpolation to fill in missing values
df_all_times = df_all_times.interpolate(method='linear')

# Compute Granger causality using the statsmodels library
maxlag = 10
test = 'ssr_chi2test'

granger_test = grangercausalitytests(df_all_times, maxlag=maxlag, verbose=False)

# Print the p-values for each lag
for lag in range(1, maxlag+1):
    p_value = granger_test[lag][0][test][1]
    print(f"Lag {lag}: p-value = {p_value:.4f}")
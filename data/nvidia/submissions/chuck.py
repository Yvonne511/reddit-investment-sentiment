import pandas as pd
import numpy as np
# Load the original DataFrame
df = pd.read_csv('nvidia_submissions_allreddit.csv')
# Split the DataFrame into 7 chunks
df_chunks = np.array_split(df, 9)
# Save each chunk to a separate file
for i, chunk in enumerate(df_chunks):
    chunk.to_csv(f'chunk_{i+1}.csv', index=False)
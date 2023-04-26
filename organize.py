import os
import pathlib
import pandas as pd
# Get all the files from dir with allreddit in its name
cwd = os.getcwd()
path_dir = os.path.join(cwd, 'data-submission')
file_path_array = []
for filepath in pathlib.Path(path_dir).glob('**/*'):
    if filepath.is_file() and 'allreddit' in filepath.name and 'ai' in filepath.name or 'AI' in filepath.name:
        file_path_array.append(filepath.relative_to(cwd).as_posix())
print(file_path_array)
# Read all the files into a dataframe and get the id column
df = pd.DataFrame()
for file_path in file_path_array:
    file_path = os.path.join(cwd, file_path)
    df_temp = pd.read_csv(file_path)
    df = pd.concat([df, df_temp], ignore_index=True)
df = df[['id']]
print(df.shape)
df.duplicated().sum()
df.drop_duplicates(inplace=True)
print(df.shape)
df.to_csv('./submissions_allreddit.csv', index=False)
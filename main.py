import pandas as pd

df = pd.read_csv('input.csv')

df['Parent Title'] = df['Title'].str.split(' - ').str.get(0)

df.to_csv('output.csv')
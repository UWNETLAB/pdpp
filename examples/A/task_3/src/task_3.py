import pandas as pd 

df = pd.read_csv('../input/test.csv')
df.to_csv('../output/test.csv', index=False)

print(df)

import pandas as pd

df = pd.read_csv('../input/example.csv')
df_plus_one = df + 1

print(df)
print(df_plus_one)

df_plus_one.to_csv('../output/df_plus_one.csv', index=False)

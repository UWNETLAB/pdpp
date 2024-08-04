import pandas as pd

df = pd.read_csv('../input/df_plus_one.csv')
df_plus_two = df + 2

print(df)
print(df_plus_two)

df_plus_two.to_csv('../output/df_plus_two.csv', index=False)
import pandas as pd

df = pd.read_csv('../input/df_plus_two.csv')
df_plus_three = df + 3

print(df)
print(df_plus_three)
print('\n')

df_plus_three.to_csv('../output/df_plus_three.csv', index=False)
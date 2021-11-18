import pandas as pd


data_A = pd.read_csv('./results.csv')
df_A = pd.DataFrame(data_A, columns=data_A.keys())

data_B = pd.read_csv('./info_result.csv')
df_B = pd.DataFrame(data_B, columns=data_B.keys())

print(df_A)
print(df_B)

result = pd.merge(df_A,df_B, on="sid", how="left")

result.to_csv('last.csv')
print(result)
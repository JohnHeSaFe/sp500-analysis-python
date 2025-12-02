import pandas as pd

df = pd.read_csv('S&P_500_Stock_Prices_2014-2017.csv')

df['date'] = pd.to_datetime(df['date'])

df['percentage_change'] = df.groupby('symbol')['close'].pct_change()

df = df[df['percentage_change'].notnull()]
print(df)


# df['percentage_change'] = df['percentage_change'].abs()
# average_volatility = df.groupby('symbol')['percentage_change'].mean() * 100
average_volatility = df.groupby('symbol')['percentage_change'].std() * 100


average_volatility = average_volatility.sort_values()
print(average_volatility)                           
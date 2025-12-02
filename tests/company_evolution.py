import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('S&P_500_Stock_Prices_2014-2017.csv')

df['date'] = pd.to_datetime(df['date'])

df = df.sort_values('date')

df_symbol = df.groupby('symbol')

df_least_recent = df_symbol['open'].first()
df_most_recent = df_symbol['close'].last()

df_result = (df_most_recent - df_least_recent) / df_least_recent * 100

df_result = df_result.sort_values()

print("\n--- Evolution of companies beetween 2014 and 2017 ---")
print(df_result)

print("\n--- top 1% ---")
print(np.percentile(df_result.values, 99))
print("\n--- top 5% ---")
print(np.percentile(df_result.values, 95))
print("\n--- bottom 10% ---")
print(np.percentile(df_result.values, 90))
print("\n--- bottom 1% ---")
print(np.percentile(df_result.values, 1))

print("\n--- dasdasda ---")
percentiles = df_result.quantile([0.25, 0.5, 0.75, 0.9])
print(percentiles)




# Crear el gráfico
plt.figure(figsize=(10, 6))

# Crear el histograma
# bins: número de barras
plt.hist(df_result, bins=50, color='skyblue', edgecolor='black')

# Añadir líneas de referencia
plt.axvline(x=0, color='red', label='0% Rentabilidad')
media = df_result.mean()

plt.axvline(x=media, color='green', label=f'Media: {media:.2f}%')

# Textos
plt.title('Distribución de Rentabilidad Total (2014-2017)', fontsize=14)
plt.xlabel('Rentabilidad (%)', fontsize=12)
plt.ylabel('Frecuencia (Nº de empresas)', fontsize=12)
plt.grid(axis='y', alpha=0.5)
plt.legend() 

# Mostrar
plt.show()
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'S&P_500_Stock_Prices_2014-2017.csv')
df = pd.read_csv(data_path)


# Elegimos unas cuantas empresas famosas
top_tech = df[df['symbol'].isin(['AAPL', 'MSFT', 'AMZN', 'ADBE', 'ADI'])]

# Creamos una tabla donde cada columna es el precio de una empresa
precios = top_tech.pivot(index='date', columns='symbol', values='close')

# Calculamos la correlación
corr_matrix = precios.pct_change().corr()

# Dibujamos el mapa de calor
import seaborn as sns
plt.figure(figsize=(8,6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('¿Cómo se relacionan las empresas entre sí?')
plt.show()
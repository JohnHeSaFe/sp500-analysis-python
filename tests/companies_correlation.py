import pandas as pd
import numpy as np  # Importación necesaria
import seaborn as sns
import matplotlib.pyplot as plt
import os

# 1. Cargar datos
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'S&P_500_Stock_Prices_2014-2017.csv')
df = pd.read_csv(data_path)

# 2. Preparar los datos
# Pivotamos y eliminamos columnas con demasiados valores nulos para un cálculo limpio
precios = df.pivot(index='date', columns='symbol', values='close')
retornos = precios.pct_change().dropna(how='all')

# 3. Calcular la matriz de correlación
corr_matrix = retornos.corr()

# 4. ENCONTRAR LAS MÁS CORRELACIONADAS (Lógica corregida)
# Creamos una máscara para ignorar la diagonal (correlación de una empresa consigo misma) 
# y la mitad inferior (que es un espejo de la superior)
mask = np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
sol = corr_matrix.where(mask).stack().sort_values(ascending=False)

# 5. Seleccionar las top empresas
# Tomamos las primeras 10 parejas con mayor correlación
top_pairs = sol.head(10)
# Extraemos los nombres de las empresas involucradas en esas parejas
top_symbols = sorted(list(set([symbol for pair in top_pairs.index for symbol in pair])))

# 6. Filtrar y graficar
final_corr = corr_matrix.loc[top_symbols, top_symbols]

plt.figure(figsize=(10, 8))
sns.heatmap(final_corr, annot=True, cmap='RdYlGn', center=0, fmt=".2f")
plt.title('Empresas con Mayor Correlación Automática (Análisis 2014-2017)')
plt.tight_layout()
plt.show()

print("Parejas más correlacionadas detectadas:")
print(top_pairs)
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Cargar los datos (cambia 'tu_archivo.csv' por el nombre real de tu archivo)
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'S&P_500_Stock_Prices_2014-2017.csv')
df = pd.read_csv(data_path)

# 2. Asegurarnos de que la fecha sea tipo datetime y ordenar
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(['symbol', 'date'])

# 3. Calcular el valor final de invertir 100€ por cada símbolo
def calcular_retorno(group):
    precio_inicial = group.iloc[0]['close']
    precio_final = group.iloc[-1]['close']
    valor_final = (100 / precio_inicial) * precio_final
    return valor_final

# Agrupamos por empresa y aplicamos la función
resultados = df.groupby('symbol').apply(calcular_retorno).reset_index()
resultados.columns = ['symbol', 'valor_final']

# 4. Obtener las 10 mejores para el gráfico
top_10 = resultados.sort_values(by='valor_final', ascending=False).head(10)

# 5. Visualización con Seaborn y Matplotlib
plt.figure(figsize=(12, 6))
sns.set_theme(style="whitegrid")

plot = sns.barplot(data=top_10, x='valor_final', y='symbol', palette='magma')

# Añadir etiquetas de los valores en las barras
plot.bar_label(plot.containers[0], fmt='%.2f€', padding=5)

plt.title('Top 10 empresas: Valor final de una inversión inicial de 100€', fontsize=16)
plt.xlabel('Valor Final en Euros', fontsize=12)
plt.ylabel('Símbolo de la Empresa', fontsize=12)

# Línea de referencia de los 100€ iniciales
plt.axvline(100, color='red', linestyle='--', label='Inversión Inicial')
plt.legend()

plt.tight_layout()
plt.show()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('S&P_500_Stock_Prices_2014-2017.csv')
df['date'] = pd.to_datetime(df['date'])

# 2. Pivotar la tabla: Fechas en filas, Empresas en columnas
# Esto crea una tabla gigante donde cada columna es una empresa
pivot_df = df.pivot_table(index='date', columns='symbol', values='close')

# 3. Calcular el cambio porcentual diario (Retornos)
returns_df = pivot_df.pct_change()

# --- IMPORTANTE ---
# Una matriz de 500x500 es ilegible. Vamos a seleccionar un sector
# o un grupo de competidores para ver si se mueven igual.
# Ejemplo: Gigantes Tecnológicos y una Petrolera para comparar
mis_acciones = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'FB', 'XOM'] 
subset_corr = returns_df[mis_acciones].corr()

# 4. Visualizar con Pyplot
fig, ax = plt.subplots(figsize=(10, 8))

# 'imshow' crea el mapa de calor
# cmap='RdYlGn': Rojo (negativo), Amarillo (neutro), Verde (positivo)
cax = ax.imshow(subset_corr, cmap='RdYlGn', vmin=-1, vmax=1)

# Añadir la barra de color lateral
fig.colorbar(cax)

# Configurar los ejes
ax.set_xticks(np.arange(len(mis_acciones)))
ax.set_yticks(np.arange(len(mis_acciones)))
ax.set_xticklabels(mis_acciones)
ax.set_yticklabels(mis_acciones)

# Rotar las etiquetas de abajo para que se lean bien
plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

# 5. (Opcional) Añadir los números dentro de los cuadrados
# Esto es un bucle que recorre cada celda y escribe el valor
for i in range(len(mis_acciones)):
    for j in range(len(mis_acciones)):
        valor = subset_corr.iloc[i, j]
        # Escribimos el texto centrado, color negro o blanco según oscuridad del fondo
        color_texto = "white" if abs(valor) > 0.5 else "black"
        text = ax.text(j, i, f"{valor:.2f}",
                       ha="center", va="center", color=color_texto, fontsize=12)

ax.set_title("Matriz de Correlación de Retornos Diarios", fontsize=16)
plt.show()
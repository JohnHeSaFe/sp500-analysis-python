import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Cargar y preparar
df = pd.read_csv('S&P_500_Stock_Prices_2014-2017.csv')
df['date'] = pd.to_datetime(df['date'])
pivot_df = df.pivot_table(index='date', columns='symbol', values='close')
returns_df = pivot_df.pct_change()

# 2. Calcular la matriz completa
full_corr = returns_df.corr()

# 3. ENCONTRAR LOS "PROTAGONISTAS" DE LAS CORRELACIONES NEGATIVAS
# Desglosamos la matriz para encontrar los valores más bajos
pares = full_corr.unstack().sort_values(kind="quicksort")

# Filtramos para quitar duplicados y la auto-correlación
# Tomamos los 20 pares con la correlación más negativa
peores_pares = pares.head(20)

# Extraemos los nombres de las empresas de esos pares
# (Usamos 'set' para que no se repitan si una empresa sale en varios pares)
empresas_conflicto = list(set([x[0] for x in peores_pares.index] + [x[1] for x in peores_pares.index]))

# Si salen demasiadas, limitamos a las primeras 12 para que el gráfico se lea bien
empresas_conflicto = empresas_conflicto[:12]

# 4. CREAR LA SUB-MATRIZ SOLO CON ESAS EMPRESAS
subset_corr = returns_df[empresas_conflicto].corr()

# 5. VISUALIZAR CON PYPLOT
fig, ax = plt.subplots(figsize=(10, 8))

# Usamos un mapa de colores divergente:
# Rojo = Negativo (Opuestos)
# Blanco/Amarillo = Neutro
# Verde/Azul = Positivo (Iguales)
cax = ax.imshow(subset_corr, cmap='RdBu', vmin=-1, vmax=1)

# Barra de color
cbar = fig.colorbar(cax)
cbar.set_label('Coeficiente de Correlación', rotation=270, labelpad=15)

# Etiquetas de los ejes
ax.set_xticks(np.arange(len(empresas_conflicto)))
ax.set_yticks(np.arange(len(empresas_conflicto)))
ax.set_xticklabels(empresas_conflicto)
ax.set_yticklabels(empresas_conflicto)

# Rotar etiquetas para lectura
plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

# Añadir los valores numéricos en cada celda
for i in range(len(empresas_conflicto)):
    for j in range(len(empresas_conflicto)):
        valor = subset_corr.iloc[i, j]
        # Resaltar en negrita si es una correlación negativa fuerte (< -0.2)
        weight = 'bold' if valor < -0.2 else 'normal'
        color = 'white' if abs(valor) > 0.5 else 'black'
        
        ax.text(j, i, f"{valor:.2f}",
                ha="center", va="center", color=color, weight=weight, fontsize=10)

plt.title("Matriz de las Empresas con Mayor Correlación Negativa", fontsize=14)
plt.tight_layout()
plt.show()
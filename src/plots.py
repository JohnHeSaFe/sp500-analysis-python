import matplotlib.pyplot as plt

def plot_histogram(data):
    # Crear el gráfico
    plt.figure(figsize=(10, 6))

    # Crear el histograma
    # bins: número de barras
    plt.hist(data, bins=50, color='skyblue', edgecolor='black')

    # Añadir líneas de referencia
    plt.axvline(x=0, color='red', label='0% Rentabilidad')
    media = data.mean()

    plt.axvline(x=media, color='green', label=f'Media: {media:.2f}%')

    # Textos
    plt.title('Distribución de Rentabilidad Total (2014-2017)', fontsize=14)
    plt.xlabel('Rentabilidad (%)', fontsize=12)
    plt.ylabel('Frecuencia (Nº de empresas)', fontsize=12)
    plt.grid(axis='y', alpha=0.5)
    plt.legend() 

    # Mostrar
    plt.show()
from src.loader import load_and_clean_data, filter_by_period
from src.metrics import calculate_returns, get_global_stats, analyze_by_symbol
from src.plots import plot_stock_evolution, plot_returns_histogram

def main():
    ruta = 'data/S&P_500_Stock_Prices_2014-2017.csv'
    
    print("- Cargando y Limiando datos -")
    df = load_and_clean_data(ruta)
    
    print("- Calculando Rendimientos -")
    df = calculate_returns(df)
    
    
    # 2.3 Mostrar df.head(), df.info(), df.describe() para entender estructura y tipos.
    
    print(df.head())
    
    print("- Información del Dataset -")
    df.info()
    
    print("- Estadísticas Descriptivas -")
    print(df.describe())
    
    # 4.1 Estadísticas globales
    print("\n- Estadísticas Globales -")
    stats = get_global_stats(df)
    for key, value in stats.items():
        print(f"{key}: {value}")
        
    # 4.2 Análisis por símbolo
    print("\n- Ranking de Símbolos (Top 5 por czrecimiento) -")
    summary = analyze_by_symbol(df)
    print(summary.head())
    
if __name__ == "__main__":
    main()
from src.loader import load_and_clean_data, filter_by_period
from src.metrics import calcular_rendimientos

def main():
    ruta = 'data/S&P_500_Stock_Prices_2014-2017.csv'
    
    print("- Cargando y Limiando datos -")
    df = load_and_clean_data(ruta)
    
    print("- Calculando Rendimientos -")
    df = calcular_rendimientos(df)
    
    
    # 2.3 Mostrar df.head(), df.info(), df.describe() para entender estructura y tipos.
    
    print("\n- Primeras filas -")
    print(df.head())
    
    print("\n- Información del Dataset -")
    df.info()
    
    print("\n- Estadísticas Descriptivas -")
    print(df.describe())

if __name__ == "__main__":
    main()
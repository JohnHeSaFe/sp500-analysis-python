import pandas as pd

def calculate_returns(df):
    # 3.5 Rendimiento diario simple
    # Se agrupan por 'symbol'
    df['return_daily'] = df.groupby('symbol')['close'].pct_change()
    
    # 3.6 Rendimiento acumulado: calcular crecimiento de inversión desde inicio
    # Sumar 1 al rendimiento diario, para que por ejemplo se multiplique por 1.05 si 5% de beneficio
    df['growth_factor'] = 1 + df['return_daily'].fillna(0)
    # Usar cumprod() que multiplica: (día 1) * (día 2) * (día 3)...
    df['return_accumulated'] = df.groupby('symbol')['growth_factor'].cumprod()
    # Borrar la columna temporal
    df = df.drop(columns=['growth_factor'])
    
    return df   

def get_global_stats(df):
    # 4.1 Estadísticas globales
    stats = {
        # 4.1.1 Número total de registros, número de símbolos (symbol)
        "total_records": len(df),
        "num_symbols": df['symbol'].nunique(),
        
        # 4.1.2 Estadísticas de rendimiento diario (return_daily): media, mediana, desviación estándar
        "mean_return": df['return_daily'].mean(),
        "median_return": df['return_daily'].median(),
        "standar_deviation": df['return_daily'].std(),
        
        # 4.1.3 Volumen medio de negociación
        "mean_volume": df['volume'].mean()
    }
    return stats

def analyze_by_symbol(df):
    # 4.2 Distribución de rendimientos por símbolo
    
    # 4.2.1 Agrupar por symbol para calcular: rendimiento medio diario, volatilidad (desviación estándar) diaria, crecimiento acumulado al final del periodo
    summary = df.groupby('symbol').agg({
        'return_daily': ['mean', 'std'],
        'return_accumulated': 'last'
    })
    
    # Renombrar columnas para que sean fáciles de leer
    summary.columns = ['mean_return', 'volatility', 'final_growth']
    
    # 4.2.2 Ordenar símbolos por rendimiento acumulado o mayor volatilidad
    return summary.sort_values(by='final_growth', ascending=False)
import pandas as pd

def calculate_returns(df):
    df['return_daily'] = df.groupby('symbol', group_keys=False)['close'].pct_change() * 100
    df['return_cumulative'] = df.groupby('symbol', group_keys=False)['close'].apply(
        lambda x: ((x / x.iloc[0]) - 1) * 100
    )
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
    summary = df.groupby('symbol', group_keys=False).agg({
        'return_daily': ['mean', 'std'],
        'return_cumulative': 'last'
    })
    summary.columns = ['mean_daily_return', 'volatility', 'cumulative_return']
    summary = summary.reset_index()
    return summary.sort_values(by='cumulative_return', ascending=False)
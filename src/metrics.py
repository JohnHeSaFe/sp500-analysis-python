import numpy as np

def get_total_return(df):
    """Calcula el retorno total por empresa (2014-2017)"""
    df_symbol = df.groupby('symbol')
    
    # Precios inicio y fin
    start_price = df_symbol['open'].first()
    end_price = df_symbol['close'].last()
    
    # Fórmula de retorno
    total_return = (end_price - start_price) / start_price * 100
    return total_return.sort_values()
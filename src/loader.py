import pandas as pd
import numpy as np

def load_and_clean_data(filepath):
    # Leer el archivo CSV
    df = pd.read_csv(filepath)

    # Convertir date al tipo datetime
    df['date'] = pd.to_datetime(df['date'])

    # Asegurar que close, open, volume, high y low están como tipos numéricos
    cols_numericas = ['open', 'close', 'volume', 'high', 'low']
    for col in cols_numericas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    # Ordenar los datos por symbol y date
    df = df.sort_values(by=['symbol', 'date'])

    # Crear columna de retorno diario
    df['daily_return'] = df.groupby('symbol')['close'].pct_change()
    
    return df

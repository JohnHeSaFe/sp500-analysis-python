import pandas as pd
import numpy as np

def load_and_clean_data(filepath):
    # 2.1 Leer el archivo CSV (‘symbol’, ‘date’, ‘open’, ‘high’, ‘low’, ‘close’, ‘volume’)
    required_columns = ['symbol', 'date', 'open', 'high', 'low', 'close', 'volume']
    df = pd.read_csv(filepath, usecols=required_columns)
   
    # 2.2 Convertir date al tipo datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # 3.2 Asegurar que close, open, volume, high y low están como tipos numéricos
    num_columns = ['open', 'close', 'volume', 'high', 'low']
    df[num_columns] = df[num_columns].apply(pd.to_numeric, errors='coerce')
    
    # 3.1 Verificar valores nulos o datos faltantes
    null_count = df.isnull().sum().sum()
    if null_count > 0:
        df = df.dropna()
        
    # 3.3 Ordenar los datos por symbol y date
    df = df.sort_values(by=['symbol', 'date'])

    return df

def filter_by_period(df, start_date, end_date):
    # 3.7 Filtrar fechas o periodos para análisis
    filter = (df['date'] >= start_date) & (df['date'] <= end_date)
    return df.loc[filter]
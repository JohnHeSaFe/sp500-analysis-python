import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# La relación entre las empresas del índice S&P 500 y sus sectores económicos
# se ha obtenido a partir del estándar GICS (Global Industry Classification Standard),
# Fuente: https://us500.com/sp500-companies-by-sector

SECTOR_MAPPING = {
    'AAPL': 'Tecnología', 'MSFT': 'Tecnología', 'GOOGL': 'Tecnología', 'GOOG': 'Tecnología',
    'FB': 'Tecnología', 'NVDA': 'Tecnología', 'INTC': 'Tecnología', 'CSCO': 'Tecnología',
    'ADBE': 'Tecnología', 'CRM': 'Tecnología', 'AVGO': 'Tecnología', 'TXN': 'Tecnología',
    'QCOM': 'Tecnología', 'ORCL': 'Tecnología', 'ACN': 'Tecnología', 'IBM': 'Tecnología',
    'NOW': 'Tecnología', 'AMD': 'Tecnología', 'INTU': 'Tecnología', 'ADI': 'Tecnología',
    'AMAT': 'Tecnología', 'MU': 'Tecnología', 'LRCX': 'Tecnología', 'KLAC': 'Tecnología',
    'SNPS': 'Tecnología', 'CDNS': 'Tecnología', 'MCHP': 'Tecnología', 'ADSK': 'Tecnología',
    'PAYX': 'Tecnología', 'ANSS': 'Tecnología', 'MSI': 'Tecnología', 'CTSH': 'Tecnología',
    'FTNT': 'Tecnología', 'WDC': 'Tecnología', 'STX': 'Tecnología', 'AKAM': 'Tecnología',
    'HPQ': 'Tecnología', 'XLNX': 'Tecnología', 'SWKS': 'Tecnología', 'KEYS': 'Tecnología',
    'ZBRA': 'Tecnología', 'FFIV': 'Tecnología', 'NTAP': 'Tecnología', 'JNPR': 'Tecnología',
    
    'JNJ': 'Salud', 'UNH': 'Salud', 'PFE': 'Salud', 'ABBV': 'Salud',
    'TMO': 'Salud', 'ABT': 'Salud', 'MRK': 'Salud', 'DHR': 'Salud',
    'LLY': 'Salud', 'AMGN': 'Salud', 'BMY': 'Salud', 'MDT': 'Salud',
    'GILD': 'Salud', 'CVS': 'Salud', 'CI': 'Salud', 'ISRG': 'Salud',
    'ANTM': 'Salud', 'SYK': 'Salud', 'BSX': 'Salud', 'VRTX': 'Salud',
    'ZTS': 'Salud', 'HUM': 'Salud', 'REGN': 'Salud', 'EW': 'Salud',
    'BIIB': 'Salud', 'BDX': 'Salud', 'ILMN': 'Salud', 'ALGN': 'Salud',
    'IQV': 'Salud', 'IDXX': 'Salud', 'A': 'Salud', 'ALXN': 'Salud',
    'RMD': 'Salud', 'HCA': 'Salud', 'DGX': 'Salud', 'CERN': 'Salud',
    'BAX': 'Salud', 'HOLX': 'Salud', 'COO': 'Salud', 'WAT': 'Salud',
    'CTLT': 'Salud', 'XRAY': 'Salud', 'VAR': 'Salud', 'PKI': 'Salud',
    'TFX': 'Salud', 'ABC': 'Salud', 'CAH': 'Salud', 'MCK': 'Salud',
    'AET': 'Salud', 'ESRX': 'Salud', 'AGN': 'Salud',
    
    'BRK.B': 'Finanzas', 'JPM': 'Finanzas', 'BAC': 'Finanzas', 'WFC': 'Finanzas',
    'V': 'Finanzas', 'MA': 'Finanzas', 'C': 'Finanzas', 'GS': 'Finanzas',
    'MS': 'Finanzas', 'AXP': 'Finanzas', 'BLK': 'Finanzas', 'SPGI': 'Finanzas',
    'USB': 'Finanzas', 'PNC': 'Finanzas', 'SCHW': 'Finanzas', 'CB': 'Finanzas',
    'MMC': 'Finanzas', 'COF': 'Finanzas', 'TFC': 'Finanzas', 'AIG': 'Finanzas',
    'AFL': 'Finanzas', 'MET': 'Finanzas', 'PRU': 'Finanzas', 'ALL': 'Finanzas',
    'TRV': 'Finanzas', 'AMP': 'Finanzas', 'HIG': 'Finanzas', 'TROW': 'Finanzas',
    'BK': 'Finanzas', 'CME': 'Finanzas', 'AON': 'Finanzas', 'MCO': 'Finanzas',
    'ICE': 'Finanzas', 'PGR': 'Finanzas', 'FIS': 'Finanzas', 'FITB': 'Finanzas',
    'AJG': 'Finanzas', 'STT': 'Finanzas', 'BEN': 'Finanzas', 'RF': 'Finanzas',
    'KEY': 'Finanzas', 'CFG': 'Finanzas', 'HBAN': 'Finanzas', 'NTRS': 'Finanzas',
    'DFS': 'Finanzas', 'WRB': 'Finanzas', 'CINF': 'Finanzas', 'L': 'Finanzas',
    'AIZ': 'Finanzas', 'ZION': 'Finanzas', 'PBCT': 'Finanzas', 'IVZ': 'Finanzas',
    
    'AMZN': 'Consumo Discrecional', 'TSLA': 'Consumo Discrecional', 'HD': 'Consumo Discrecional',
    'NKE': 'Consumo Discrecional', 'MCD': 'Consumo Discrecional', 'LOW': 'Consumo Discrecional',
    'SBUX': 'Consumo Discrecional', 'TGT': 'Consumo Discrecional', 'BKNG': 'Consumo Discrecional',
    'TJX': 'Consumo Discrecional', 'CMG': 'Consumo Discrecional', 'ORLY': 'Consumo Discrecional',
    'GM': 'Consumo Discrecional', 'F': 'Consumo Discrecional', 'YUM': 'Consumo Discrecional',
    'EBAY': 'Consumo Discrecional', 'ROST': 'Consumo Discrecional', 'HLT': 'Consumo Discrecional',
    'AZO': 'Consumo Discrecional', 'DHI': 'Consumo Discrecional', 'LEN': 'Consumo Discrecional',
    'BBY': 'Consumo Discrecional', 'DG': 'Consumo Discrecional', 'DLTR': 'Consumo Discrecional',
    'TSCO': 'Consumo Discrecional', 'MAR': 'Consumo Discrecional', 'EXPE': 'Consumo Discrecional',
    'MGM': 'Consumo Discrecional', 'WYNN': 'Consumo Discrecional', 'LVS': 'Consumo Discrecional',
    'CCL': 'Consumo Discrecional', 'RCL': 'Consumo Discrecional', 'NCLH': 'Consumo Discrecional',
    'HAS': 'Consumo Discrecional', 'AAP': 'Consumo Discrecional', 'GPS': 'Consumo Discrecional',
    'KSS': 'Consumo Discrecional', 'M': 'Consumo Discrecional', 'JWN': 'Consumo Discrecional',
    'RL': 'Consumo Discrecional', 'PVH': 'Consumo Discrecional', 'TPR': 'Consumo Discrecional',
    'DRI': 'Consumo Discrecional', 'LB': 'Consumo Discrecional', 'ULTA': 'Consumo Discrecional',
    
    'GOOGL': 'Servicios de Comunicación', 'GOOG': 'Servicios de Comunicación', 'FB': 'Servicios de Comunicación',
    'DIS': 'Servicios de Comunicación', 'CMCSA': 'Servicios de Comunicación', 'NFLX': 'Servicios de Comunicación',
    'VZ': 'Servicios de Comunicación', 'T': 'Servicios de Comunicación', 'TMUS': 'Servicios de Comunicación',
    'CHTR': 'Servicios de Comunicación', 'ATVI': 'Servicios de Comunicación', 'EA': 'Servicios de Comunicación',
    'DISH': 'Servicios de Comunicación', 'FOXA': 'Servicios de Comunicación', 'FOX': 'Servicios de Comunicación',
    'OMC': 'Servicios de Comunicación', 'IPG': 'Servicios de Comunicación', 'NWSA': 'Servicios de Comunicación',
    'NWS': 'Servicios de Comunicación', 'DISCA': 'Servicios de Comunicación', 'DISCK': 'Servicios de Comunicación',
    'TTWO': 'Servicios de Comunicación', 'TWTR': 'Servicios de Comunicación',
    
    'BA': 'Industria', 'HON': 'Industria', 'UPS': 'Industria', 'RTX': 'Industria',
    'UNP': 'Industria', 'LMT': 'Industria', 'CAT': 'Industria', 'DE': 'Industria',
    'MMM': 'Industria', 'GE': 'Industria', 'FDX': 'Industria', 'CSX': 'Industria',
    'NOC': 'Industria', 'WM': 'Industria', 'ITW': 'Industria', 'EMR': 'Industria',
    'ETN': 'Industria', 'GD': 'Industria', 'NSC': 'Industria', 'PCAR': 'Industria',
    'JCI': 'Industria', 'CMI': 'Industria', 'ROK': 'Industria', 'CARR': 'Industria',
    'OTIS': 'Industria', 'IR': 'Industria', 'PH': 'Industria', 'AME': 'Industria',
    'FAST': 'Industria', 'RSG': 'Industria', 'VRSK': 'Industria', 'DAL': 'Industria',
    'UAL': 'Industria', 'AAL': 'Industria', 'LUV': 'Industria', 'ALK': 'Industria',
    'JBHT': 'Industria', 'SWK': 'Industria', 'CHRW': 'Industria', 'EXPD': 'Industria',
    'URI': 'Industria', 'ODFL': 'Industria', 'PWR': 'Industria', 'ALLE': 'Industria',
    'TXT': 'Industria', 'HWM': 'Industria', 'DOV': 'Industria', 'FTV': 'Industria',
    'XYL': 'Industria', 'IEX': 'Industria', 'ROP': 'Industria', 'AOS': 'Industria',
    
    'PG': 'Consumo Básico', 'KO': 'Consumo Básico', 'PEP': 'Consumo Básico',
    'WMT': 'Consumo Básico', 'COST': 'Consumo Básico', 'PM': 'Consumo Básico',
    'MO': 'Consumo Básico', 'MDLZ': 'Consumo Básico', 'CL': 'Consumo Básico',
    'KMB': 'Consumo Básico', 'GIS': 'Consumo Básico', 'KHC': 'Consumo Básico',
    'STZ': 'Consumo Básico', 'SYY': 'Consumo Básico', 'ADM': 'Consumo Básico',
    'HSY': 'Consumo Básico', 'K': 'Consumo Básico', 'CLX': 'Consumo Básico',
    'TSN': 'Consumo Básico', 'MKC': 'Consumo Básico', 'CHD': 'Consumo Básico',
    'CAG': 'Consumo Básico', 'CPB': 'Consumo Básico', 'SJM': 'Consumo Básico',
    'HRL': 'Consumo Básico', 'TAP': 'Consumo Básico', 'KR': 'Consumo Básico',
    'WBA': 'Consumo Básico', 'DGX': 'Consumo Básico', 'EL': 'Consumo Básico',
    
    'XOM': 'Energía', 'CVX': 'Energía', 'COP': 'Energía', 'SLB': 'Energía',
    'EOG': 'Energía', 'PXD': 'Energía', 'MPC': 'Energía', 'PSX': 'Energía',
    'VLO': 'Energía', 'KMI': 'Energía', 'WMB': 'Energía', 'OKE': 'Energía',
    'HAL': 'Energía', 'DVN': 'Energía', 'HES': 'Energía', 'FANG': 'Energía',
    'BKR': 'Energía', 'APA': 'Energía', 'NOV': 'Energía', 'HP': 'Energía',
    'MRO': 'Energía', 'NBL': 'Energía', 'COG': 'Energía', 'APC': 'Energía',
    
    'LIN': 'Materiales', 'APD': 'Materiales', 'SHW': 'Materiales', 'ECL': 'Materiales',
    'DD': 'Materiales', 'NEM': 'Materiales', 'FCX': 'Materiales', 'DOW': 'Materiales',
    'PPG': 'Materiales', 'NUE': 'Materiales', 'VMC': 'Materiales', 'MLM': 'Materiales',
    'CTVA': 'Materiales', 'ALB': 'Materiales', 'FMC': 'Materiales', 'IFF': 'Materiales',
    'BALL': 'Materiales', 'AVY': 'Materiales', 'EMN': 'Materiales', 'CF': 'Materiales',
    'LYB': 'Materiales', 'MOS': 'Materiales', 'PKG': 'Materiales', 'IP': 'Materiales',
    'WRK': 'Materiales', 'SEE': 'Materiales', 'ARNC': 'Materiales',
    
    'AMT': 'Inmobiliario', 'PLD': 'Inmobiliario', 'CCI': 'Inmobiliario', 'EQIX': 'Inmobiliario',
    'PSA': 'Inmobiliario', 'SPG': 'Inmobiliario', 'WELL': 'Inmobiliario', 'DLR': 'Inmobiliario',
    'O': 'Inmobiliario', 'AVB': 'Inmobiliario', 'EQR': 'Inmobiliario', 'SBAC': 'Inmobiliario',
    'VTR': 'Inmobiliario', 'ARE': 'Inmobiliario', 'PEAK': 'Inmobiliario', 'EXR': 'Inmobiliario',
    'MAA': 'Inmobiliario', 'INVH': 'Inmobiliario', 'ESS': 'Inmobiliario', 'UDR': 'Inmobiliario',
    'HST': 'Inmobiliario', 'VICI': 'Inmobiliario', 'KIM': 'Inmobiliario', 'REG': 'Inmobiliario',
    'BXP': 'Inmobiliario', 'FRT': 'Inmobiliario', 'VNO': 'Inmobiliario', 'AIV': 'Inmobiliario',
    
    'NEE': 'Servicios Públicos', 'DUK': 'Servicios Públicos', 'SO': 'Servicios Públicos', 'D': 'Servicios Públicos',
    'AEP': 'Servicios Públicos', 'EXC': 'Servicios Públicos', 'SRE': 'Servicios Públicos', 'XEL': 'Servicios Públicos',
    'PEG': 'Servicios Públicos', 'ED': 'Servicios Públicos', 'WEC': 'Servicios Públicos', 'ES': 'Servicios Públicos',
    'DTE': 'Servicios Públicos', 'PPL': 'Servicios Públicos', 'AWK': 'Servicios Públicos', 'AEE': 'Servicios Públicos',
    'CMS': 'Servicios Públicos', 'ETR': 'Servicios Públicos', 'CNP': 'Servicios Públicos', 'FE': 'Servicios Públicos',
    'AES': 'Servicios Públicos', 'LNT': 'Servicios Públicos', 'EVRG': 'Servicios Públicos', 'NI': 'Servicios Públicos',
    'PNW': 'Servicios Públicos', 'NRG': 'Servicios Públicos',
}

def load_data(csv_path):
    df = pd.read_csv(csv_path)
    df['date'] = pd.to_datetime(df['date'])
    return df


def get_companies_by_sector(df):
    companies = df['symbol'].unique()
    sector_dict = {}

    for company in companies:
        sector = SECTOR_MAPPING.get(company, 'Unknown')
        sector_dict.setdefault(sector, []).append(company)

    return sector_dict


def calculate_sector_growth(df, sector_dict):
    results = []

    for sector, companies in sector_dict.items():
        if sector == 'Unknown':
            continue

        sector_df = df[df['symbol'].isin(companies)].copy()
        if sector_df.empty:
            continue

        sector_df['weighted_close'] = sector_df['close'] * sector_df['volume']

        sector_daily = (
            sector_df
            .groupby('date', as_index=False)
            .agg(
                weighted_sum=('weighted_close', 'sum'),
                total_volume=('volume', 'sum')
            )
        )

        sector_daily['weighted_price'] = (
            sector_daily['weighted_sum'] / sector_daily['total_volume']
        )

        sector_daily = (
            sector_daily[['date', 'weighted_price']]
            .sort_values('date')
        )

        start_price = sector_daily.iloc[0]['weighted_price']
        end_price = sector_daily.iloc[-1]['weighted_price']

        growth = ((end_price - start_price) / start_price) * 100

        results.append({
            'sector': sector,
            'start_price': start_price,
            'end_price': end_price,
            'growth_percent': growth,
            'num_companies': len(companies),
            'daily_data': sector_daily
        })

    return pd.DataFrame(results).sort_values('growth_percent', ascending=False)



def plot_sector_growth(sector_growth):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

    colors = ['green' if x > 0 else 'red' for x in sector_growth['growth_percent']]
    ax1.barh(sector_growth['sector'], sector_growth['growth_percent'], color=colors, alpha=0.7)
    ax1.set_xlabel('Crecimiento (%)')
    ax1.set_ylabel('Sector')
    ax1.set_title('Crecimiento por Sector del S&P 500 (2014–2017)')
    ax1.axvline(0, color='black', linestyle='--', linewidth=0.8)
    ax1.grid(axis='x', alpha=0.3)

    for _, row in sector_growth.iterrows():
        ax1.text(row['growth_percent'], row['sector'],
                f" {row['growth_percent']:.1f}%", va='center', fontsize=9)

    for _, row in sector_growth.iterrows():
        daily = row['daily_data']
        normalized = daily['weighted_price'] / daily['weighted_price'].iloc[0] * 100
        ax2.plot(daily['date'], normalized, label=row['sector'], linewidth=2)

    ax2.set_xlabel('Fecha')
    ax2.set_ylabel('Índice (Base 100)')
    ax2.set_title('Evolución Temporal por Sector')
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax2.grid(alpha=0.3)
    ax2.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    return fig


def plot_sector_composition(sector_dict):
    sector_counts = {s: len(c) for s, c in sector_dict.items() if s != 'Unknown'}

    labels = list(sector_counts.keys())
    sizes = list(sector_counts.values())

    explode = [0.05] * len(labels) 

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        startangle=90,
        explode=explode
    )

    ax.set_title('Composición del Dataset S&P 500 por Sector')
    plt.tight_layout()
    return fig



def main():
    base_dir = Path(__file__).parent.parent
    data_path = base_dir / 'data' / 'S&P_500_Stock_Prices_2014-2017.csv'

    df = load_data(data_path)
    sector_dict = get_companies_by_sector(df)
    sector_growth = calculate_sector_growth(df, sector_dict)

    output_path = base_dir / 'data' / 'sector_analysis.csv'
    sector_growth[['sector', 'growth_percent', 'num_companies', 'start_price', 'end_price']] \
        .to_csv(output_path, index=False)

    plot_sector_growth(sector_growth)
    plot_sector_composition(sector_dict)
    plt.show()


if __name__ == '__main__':
    main()

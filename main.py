from src.loader import load_and_clean_data
from src.metrics import get_total_return
from src.plots import plot_histogram

FILE_PATH = 'data/S&P_500_Stock_Prices_2014-2017.csv'

def main():
    df = load_and_clean_data(FILE_PATH)
    total_returns = get_total_return(df)
    plot_histogram(total_returns)
    
if __name__ == "__main__":
    main()
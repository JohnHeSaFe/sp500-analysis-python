import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def simulate_daily_investment(df, daily_investment=10):
    results = []
    
    for symbol, group in df.groupby('symbol'):
        group = group.sort_values('date')
        
        total_invested = 0
        total_shares = 0
        
        for _, row in group.iterrows():
            price = row['close']
            if pd.notna(price) and price > 0:
                shares_bought = daily_investment / price
                total_shares += shares_bought
                total_invested += daily_investment
        
        final_price = group.iloc[-1]['close']
        if pd.notna(final_price):
            final_value = total_shares * final_price
            profit = final_value - total_invested
            profit_percentage = (profit / total_invested * 100) if total_invested > 0 else 0
            
            results.append({
                'symbol': symbol,
                'total_invested': total_invested,
                'final_value': final_value,
                'profit': profit,
                'profit_percentage': profit_percentage,
                'total_shares': total_shares,
                'avg_price': total_invested / total_shares if total_shares > 0 else 0,
                'final_price': final_price
            })
    
    return pd.DataFrame(results)

def plot_top_winners_losers(results_df):
    top_winners = results_df.nlargest(10, 'profit')
    top_losers = results_df.nsmallest(10, 'profit')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    colors_winners = ['green' if x > 0 else 'red' for x in top_winners['profit']]
    ax1.barh(top_winners['symbol'], top_winners['profit'], color=colors_winners)
    ax1.set_xlabel('Ganancia (€)', fontsize=12)
    ax1.set_ylabel('Empresa', fontsize=12)
    ax1.set_title('Top 10 Empresas - Mayores Ganancias\n(Invirtiendo 10€ diarios 2014-2017)', 
                  fontsize=14, fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)
    
    for i, (idx, row) in enumerate(top_winners.iterrows()):
        ax1.text(row['profit'], i, f"  {row['profit']:.0f}€ ({row['profit_percentage']:.1f}%)", 
                va='center', fontsize=9)
    
    colors_losers = ['red' if x < 0 else 'green' for x in top_losers['profit']]
    ax2.barh(top_losers['symbol'], top_losers['profit'], color=colors_losers)
    ax2.set_xlabel('Pérdida (€)', fontsize=12)
    ax2.set_ylabel('Empresa', fontsize=12)
    ax2.set_title('Top 10 Empresas - Mayores Pérdidas\n(Invirtiendo 10€ diarios 2014-2017)', 
                  fontsize=14, fontweight='bold')
    ax2.grid(axis='x', alpha=0.3)
    
    for i, (idx, row) in enumerate(top_losers.iterrows()):
        ax2.text(row['profit'], i, f"  {row['profit']:.0f}€ ({row['profit_percentage']:.1f}%)", 
                va='center', fontsize=9)
    
    plt.tight_layout()
    return fig

def main():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'S&P_500_Stock_Prices_2014-2017.csv')
    df = pd.read_csv(data_path)
    df['date'] = pd.to_datetime(df['date'])
    
    results = simulate_daily_investment(df, daily_investment=10)
    
    results = results.sort_values('profit', ascending=False)
    
    output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'investment_results.csv')
    results.to_csv(output_path, index=False)
    
    fig = plot_top_winners_losers(results)
    
    plot_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'investment_comparison.png')
    fig.savefig(plot_path, dpi=300, bbox_inches='tight')
    
    plt.show()

if __name__ == "__main__":
    main()

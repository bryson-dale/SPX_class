# stats_calculator.py

import pandas as pd
from scipy.stats import skew
import numpy as np

def calculate_statistics(returns, turnover=None, trading_frequency='M'):
    stats = {}
    # Determine periods per year based on trading frequency
    freq_map = {
        'D': 252,
        'W': 52,
        '2W': 26,
        'M': 12
    }
    periods_per_year = freq_map.get(trading_frequency.upper())
    if not periods_per_year:
        raise ValueError("Invalid trading frequency.")

    # Annualized Geometric Return
    total_return = (1 + returns).prod()
    num_periods = len(returns)
    num_years = num_periods / periods_per_year
    annualized_return = total_return ** (1 / num_years) - 1
    stats['Annualized Return (%)'] = annualized_return * 100

    # Annualized Standard Deviation
    annualized_std = returns.std() * np.sqrt(periods_per_year)

    # Annualized Sharpe Ratio (Assuming risk-free rate = 0)
    sharpe_ratio = annualized_return / annualized_std if annualized_std != 0 else np.nan
    stats['Annualized Sharpe Ratio'] = sharpe_ratio

    # Skewness
    stats['Skewness'] = skew(returns)

    # Maximum Drawdown
    cumulative = (1 + returns).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    max_drawdown = drawdown.min()
    stats['Max Drawdown (%)'] = max_drawdown * 100

    # Average Turnover
    if turnover is not None:
        avg_turnover = turnover.mean()
        stats['Average Turnover (%)'] = avg_turnover * 100
    else:
        stats['Average Turnover (%)'] = np.nan

    return stats

def round_to_sig_figs(value, sig_figs):
    if pd.isnull(value) or value == 0:
        return value
    else:
        return round(value, sig_figs - int(np.floor(np.log10(abs(value)))) - 1)

def display_statistics(returns_dict, sig_figs=4):
    stats_list = []
    for label, data in returns_dict.items():
        returns = data['returns']
        turnover = data.get('turnover', None)
        trading_freq = data.get('trading_frequency', 'monthly')

        stats = calculate_statistics(returns, turnover, trading_frequency=trading_freq)
        stats['Strategy'] = label
        stats_list.append(stats)

    stats_df = pd.DataFrame(stats_list).set_index('Strategy')

    # Round statistics to the specified number of significant figures
    stats_df = stats_df.applymap(lambda x: round_to_sig_figs(x, sig_figs))

    from IPython.display import display, HTML
    display(HTML(stats_df.to_html()))

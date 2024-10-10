# strategy/momentum_sector_LS.py

import pandas as pd
import numpy as np
from .strategy_base import Strategy  # Relative import from strategy_base
from scipy.stats import skew

class MomentumSectorLongShortStrategy(Strategy):
    def __init__(self, data_loader, config):
        self.data_loader = data_loader
        self.config = config
        self.set_parameters()
        self.long_returns = None
        self.short_returns = None
        self.combined_returns = None
        self.long_turnover = None
        self.short_turnover = None
        self.combined_turnover = None

    def set_parameters(self, num_sectors=5, trading_frequency='M', start_date='1980-01-01', end_date=None):
        self.num_sectors = num_sectors
        self.trading_frequency = trading_frequency.upper()  # Ensure frequency is uppercase
        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date) if end_date else None

    def generate_signals(self):
        # Get data from DataLoader
        prices = self.data_loader.get_prices()
        presence_matrix = self.data_loader.get_presence_matrix()

        # Resample data based on trading frequency
        freq = self.trading_frequency  # Use the pandas frequency string directly

        # Resample and compute returns
        spx_returns = prices.resample(freq).last().pct_change()
        presence_matrix_resampled = presence_matrix.resample(freq).last()

        # Filter data by date range
        if self.end_date:
            date_mask = (spx_returns.index >= self.start_date) & (spx_returns.index <= self.end_date)
        else:
            date_mask = spx_returns.index >= self.start_date
        spx_returns = spx_returns.loc[date_mask]
        presence_matrix_resampled = presence_matrix_resampled.loc[date_mask]

        # Apply presence matrix to returns
        spx500_returns = spx_returns.copy()
        for level in spx500_returns.columns.levels[0]:
            if level in presence_matrix_resampled.columns:
                spx500_returns.loc[:, (level, slice(None))] *= presence_matrix_resampled[level].values.reshape(-1, 1)
            else:
                spx500_returns.drop(level=0, labels=level, axis=1, inplace=True)

        # Remove columns with all NaNs
        spx500_returns = spx500_returns.dropna(axis=1, how='all')

        # Store for later use
        self.spx500_returns = spx500_returns

        # Calculate sector average returns
        sector_avg_returns = spx500_returns.groupby(axis=1, level='sector').mean()

        # Calculate sector momentum
        # Adjust window size based on trading frequency
        window_size = self._determine_window_size()

        sector_return_momentum = sector_avg_returns.shift(1).rolling(window=window_size, min_periods=1).mean()

        # Create presence matrices for top and bottom sectors
        top_presence_matrix = pd.DataFrame(0, index=sector_return_momentum.index, columns=sector_return_momentum.columns)
        bottom_presence_matrix = pd.DataFrame(0, index=sector_return_momentum.index, columns=sector_return_momentum.columns)

        for date, momentum in sector_return_momentum.iterrows():
            valid_momentum = momentum.dropna()
            num_available_sectors = len(valid_momentum)
            num_selected_sectors = min(self.num_sectors, num_available_sectors // 2)
            if num_selected_sectors == 0:
                continue
            top_sectors = valid_momentum.nlargest(num_selected_sectors).index
            bottom_sectors = valid_momentum.nsmallest(num_selected_sectors).index

            top_presence_matrix.loc[date, top_sectors] = 1
            bottom_presence_matrix.loc[date, bottom_sectors] = 1

        self.top_presence_matrix = top_presence_matrix
        self.bottom_presence_matrix = bottom_presence_matrix
        self.sector_avg_returns = sector_avg_returns

    def _determine_window_size(self):
        # Define a mapping from frequency to approximate number of periods per year
        freq_to_periods = {
            'D': 252,   # Trading days in a year
            'W': 52,    # Weeks in a year
            '2W': 26,   # Bi-weekly periods in a year
            'M': 12     # Months in a year
        }
        periods_per_year = freq_to_periods.get(self.trading_frequency)
        if not periods_per_year:
            raise ValueError("Invalid trading frequency.")

        # For an 11-month window, calculate the equivalent number of periods
        window_size = int((11 / 12) * periods_per_year)
        if window_size < 1:
            window_size = 1  # Ensure at least a window size of 1
        return window_size

    def calculate_returns(self):
        # Align sector returns with presence matrices
        aligned_sector_returns = self.sector_avg_returns.loc[self.top_presence_matrix.index]

        # Calculate long and short returns
        long_returns = (aligned_sector_returns * self.top_presence_matrix).sum(axis=1) / self.top_presence_matrix.sum(axis=1)
        short_returns = (aligned_sector_returns * self.bottom_presence_matrix).sum(axis=1) / self.bottom_presence_matrix.sum(axis=1)

        # Replace NaNs with zero
        long_returns = long_returns.fillna(0)
        short_returns = short_returns.fillna(0)

        # Invert short returns
        short_returns = -short_returns

        # Combined returns
        combined_returns = long_returns + short_returns

        # Calculate positions
        long_positions = self.top_presence_matrix.div(self.top_presence_matrix.sum(axis=1), axis=0).fillna(0)
        short_positions = -self.bottom_presence_matrix.div(self.bottom_presence_matrix.sum(axis=1), axis=0).fillna(0)
        combined_positions = long_positions + short_positions

        # Adjust returns for transaction costs
        long_returns_adj, long_turnover = self.adjust_returns_for_transaction_costs(long_positions, long_returns)
        short_returns_adj, short_turnover = self.adjust_returns_for_transaction_costs(short_positions, short_returns)
        combined_returns_adj, combined_turnover = self.adjust_returns_for_transaction_costs(combined_positions, combined_returns)

        # Store results
        self.long_returns = long_returns_adj
        self.short_returns = short_returns_adj
        self.combined_returns = combined_returns_adj
        self.long_turnover = long_turnover
        self.short_turnover = short_turnover
        self.combined_turnover = combined_turnover

    def adjust_returns_for_transaction_costs(self, positions, returns):
        # Calculate turnover
        turnover = positions.diff().abs().sum(axis=1)
        turnover.iloc[0] = positions.iloc[0].abs().sum()
        # Calculate transaction costs
        transaction_costs = turnover * (self.config.transaction_cost_bps / 10000)
        # Adjust returns
        adjusted_returns = returns - transaction_costs
        return adjusted_returns, turnover

    def get_results(self):
        # Method to retrieve the calculated returns and turnover
        return {
            'long_returns': self.long_returns,
            'short_returns': self.short_returns,
            'combined_returns': self.combined_returns,
            'long_turnover': self.long_turnover,
            'short_turnover': self.short_turnover,
            'combined_turnover': self.combined_turnover
        }

    def calculate_statistics(self):
        # Method to calculate and return statistics for the strategy
        stats = {}
        # For long_returns
        stats['Long Strategy'] = self._calculate_individual_statistics(self.long_returns, self.long_turnover)
        # For short_returns
        stats['Short Strategy'] = self._calculate_individual_statistics(self.short_returns, self.short_turnover)
        # For combined_returns
        stats['Combined Strategy'] = self._calculate_individual_statistics(self.combined_returns, self.combined_turnover)
        return stats

    def _calculate_individual_statistics(self, returns, turnover):
        stats = {}
        # Determine periods per year based on trading frequency
        freq_map = {
            'D': 252,
            'W': 52,
            '2W': 26,
            'M': 12
        }
        periods_per_year = freq_map.get(self.trading_frequency)
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
        avg_turnover = turnover.mean()
        stats['Average Turnover (%)'] = avg_turnover * 100

        return stats

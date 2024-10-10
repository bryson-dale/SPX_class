# benchmark.py

import pandas as pd
import numpy as np

class Benchmark:
    def __init__(self, data_loader, config, benchmark_type='Equally Weighted'):
        self.data_loader = data_loader
        self.config = config
        self.benchmark_type = benchmark_type
        self.returns = None
        self.turnover = None

    def calculate_returns(self, trading_frequency='M', start_date='1980-01-01', end_date=None):
        # Get data
        prices = self.data_loader.get_prices()
        presence_matrix = self.data_loader.get_presence_matrix()

        # Use the pandas frequency string directly
        freq = trading_frequency.upper()

        # Resample and compute returns
        index_prices = prices.resample(freq).last()
        index_returns = index_prices.pct_change()
        presence_matrix_resampled = presence_matrix.resample(freq).last()

        # Filter data by date range
        start_date = pd.to_datetime(start_date)
        if end_date:
            end_date = pd.to_datetime(end_date)
            date_mask = (index_returns.index >= start_date) & (index_returns.index <= end_date)
        else:
            date_mask = index_returns.index >= start_date
        index_returns = index_returns.loc[date_mask]
        presence_matrix_resampled = presence_matrix_resampled.loc[date_mask]

        # Apply presence matrix to returns
        index_returns = index_returns.copy()
        for level in index_returns.columns.levels[0]:
            if level in presence_matrix_resampled.columns:
                index_returns.loc[:, (level, slice(None))] *= presence_matrix_resampled[level].values.reshape(-1, 1)
            else:
                index_returns.drop(level=0, labels=level, axis=1, inplace=True)

        # Remove columns with all NaNs
        index_returns = index_returns.dropna(axis=1, how='all')

        # Calculate equally weighted index returns
        benchmark_returns = index_returns.mean(axis=1, skipna=True)

        # Calculate positions: equal weights across all stocks present in the index
        index_positions = index_returns.notna().astype(float)
        index_positions = index_positions.div(index_positions.sum(axis=1), axis=0).fillna(0)

        # Calculate turnover
        index_positions_shifted = index_positions.shift(1).fillna(0)
        turnover = (index_positions - index_positions_shifted).abs().sum(axis=1)
        turnover.iloc[0] = index_positions.iloc[0].abs().sum()

        # Calculate transaction costs
        transaction_costs = turnover * (self.config.transaction_cost_bps / 10000)

        # Adjust returns for transaction costs
        benchmark_returns_adj = benchmark_returns - transaction_costs

        # Store results
        self.returns = benchmark_returns_adj
        self.turnover = turnover

# backtest.py

class Backtest:
    def __init__(self, strategy, benchmark):
        self.strategy = strategy
        self.benchmark = benchmark

    def run_backtest(self):
        # Run strategy
        self.strategy.generate_signals()
        self.strategy.calculate_returns()

        # Run benchmark
        self.benchmark.calculate_returns(
            trading_frequency=self.strategy.trading_frequency,
            start_date=self.strategy.start_date,
            end_date=self.strategy.end_date
        )

    def get_returns(self):
        # Retrieve returns and turnovers from strategy and benchmark
        returns_dict = {
            'Long Strategy': {
                'returns': self.strategy.long_returns,
                'turnover': self.strategy.long_turnover,
                'trading_frequency': self.strategy.trading_frequency
            },
            'Short Strategy': {
                'returns': self.strategy.short_returns,
                'turnover': self.strategy.short_turnover,
                'trading_frequency': self.strategy.trading_frequency
            },
            'Combined Strategy': {
                'returns': self.strategy.combined_returns,
                'turnover': self.strategy.combined_turnover,
                'trading_frequency': self.strategy.trading_frequency
            },
            'Benchmark': {
                'returns': self.benchmark.returns,
                'turnover': self.benchmark.turnover,
                'trading_frequency': self.strategy.trading_frequency
            }
        }
        return returns_dict

# SPX_class

A Python-based backtesting framework to analyze S&P 500 strategies.

## Project Structure

- **data/**: Contains CSV files of data used in the project.
- **strategy/**: Contains different strategy files.
  - **momentum_sector_LS.py**: Implements the momentum sector long-short strategy.
  - **strategy_base.py**: Base class for strategy objects.
- **config.py**: Configurations and settings used globally in the project.
- **data_loader.py**: Loads and preprocesses data from CSV files.
- **benchmark.py**: Calculates benchmark returns for comparison.
- **backtest.py**: Runs the backtest using the strategy.
- **plotter.py**: Functions for visualizing results.
- **stats_calculator.py**: Functions to calculate performance statistics.
- **main.ipynb**: Jupyter Notebook that runs the analysis.

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/your_username/SPX_class.git
   cd SPX_class

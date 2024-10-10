# SPX_class

A Python-based backtesting framework designed to analyze and simulate S&P 500 investment strategies. The project currently features a **Momentum Sector Long-Short Strategy** that uses historical sector data to calculate momentum and generate signals. The framework is modular, making it easy to add new strategies, benchmarks, and data sources.

## Project Structure

```
SPX_class/
│
├── data/                               # Folder containing CSV files with data used in the project
│   ├── permno_industry_map.csv         # Mapping of permno to industry codes
│   ├── permno_sic_map.csv              # Mapping of permno to SIC codes
│   ├── spx_presence.csv                # SPX presence matrix (whether a stock is in the index)
│   ├── spx_prices.csv                  # Daily prices of S&P 500 constituents
│
├── strategy/                           # Contains different strategy files
│   ├── __init__.py                     # Makes `strategy` a Python package for easy imports
│   ├── strategy_base.py                # Base class for strategy objects
│   ├── momentum_sector_LS.py           # Implements the momentum sector long-short strategy
│
├── config.py                           # Configuration settings for the project
├── data_loader.py                      # Loads and preprocesses data from CSV files
├── benchmark.py                        # Code to calculate benchmark returns
├── backtest.py                         # Backtest logic for running the strategy
├── plotter.py                          # Plotting functions for results
├── stats_calculator.py                 # Statistics calculations for strategies
├── main.ipynb                          # Jupyter Notebook that runs the analysis
├── requirements.txt                    # List of dependencies required for the project
├── .gitignore                          # Specifies files and directories ignored by Git
├── README.md                           # Documentation for the project
└── environment.yml                     # Conda environment configuration (if using Conda)
```

## Features

- **Momentum Sector Long-Short Strategy**: Implements a momentum-based sector strategy to generate long and short signals.
- **Benchmarking**: Compare strategy returns against an equally-weighted index benchmark.
- **Backtesting Framework**: Perform historical backtests to analyze strategy performance.
- **Statistical Analysis**: Calculate key statistics such as Sharpe ratio, annualized returns, and maximum drawdown.
- **Interactive Notebook**: Use `main.ipynb` to easily interact with the code and visualize results.

## Installation

1. **Clone the Repository**:

   ```sh
   git clone https://github.com/your_username/SPX_class.git
   cd SPX_class
   ```

2. **Create a Virtual Environment** (Recommended):

   - **With venv**:

     ```sh
     python -m venv venv
     source venv/bin/activate  # On Linux/macOS
     venv\Scripts\activate     # On Windows
     ```

   - **With Conda** (Optional):

     ```sh
     conda env create -f environment.yml
     conda activate spx_class_env
     ```

3. **Install Dependencies**:

   - Using `requirements.txt`:

     ```sh
     pip install -r requirements.txt
     ```

## Usage

### Running the Jupyter Notebook

Open the `main.ipynb` Jupyter Notebook to run the analysis:

```sh
jupyter notebook main.ipynb
```

### Running Backtest and Generating Results

The `main.ipynb` contains the necessary code to:

1. **Load Data** using the `DataLoader` class.
2. **Initialize Strategy** using the `MomentumSectorLongShortStrategy`.
3. **Run Backtests** using the `Backtest` class.
4. **Visualize Results** using the `Plotter`.

## Data Files

The data required for the backtest is included in the `/data` folder:

- **`permno_industry_map.csv`**: Maps permno identifiers to industry codes.
- **`spx_presence.csv`**: Indicates which stocks are present in the S&P 500 index at any given time.
- **`spx_prices.csv`**: Contains daily closing prices of S&P 500 constituents.

> **Note**: Ensure these data files are correctly placed in the `/data` directory before running any scripts.

## Configurations

The project includes a configuration file (`config.py`) where you can define key parameters such as:

- **Transaction Cost** (`transaction_cost_bps`): Default is set to 0 basis points but can be adjusted.
  
Example:

```python
class Config:
    def __init__(self, transaction_cost_bps=0):
        self.transaction_cost_bps = transaction_cost_bps
```

## Strategy Overview

### **Momentum Sector Long-Short Strategy**

This strategy aims to:

- **Long** the top-performing sectors and **short** the worst-performing sectors based on historical momentum.
- It uses a configurable **rolling window** to determine sector momentum, and you can adjust the **number of sectors** and **trading frequency** (e.g., monthly, weekly, biweekly).

#### Strategy Parameters:

- **Number of Sectors (`num_sectors`)**: Controls the number of sectors to be long/short.
- **Trading Frequency (`trading_frequency`)**: Options are `"daily"`, `"weekly"`, `"biweekly"`, or `"monthly"`.
- **Start and End Date (`start_date`, `end_date`)**: Define the analysis period.

### **Benchmark**

An **equally weighted benchmark** is provided for comparison with the long-short strategy to assess its performance.

## Backtesting

The `backtest.py` file allows for systematic backtesting of any strategy developed. To run the backtest:

1. **Create an instance** of the backtest using your strategy and benchmark.
2. **Run the backtest** to generate performance metrics and visualizations.

```python
# Example usage in `main.ipynb`:
from backtest import Backtest

# Run Backtest
backtest = Backtest(strategy, benchmark)
backtest.run_backtest()

# Get Returns
returns_dict = backtest.get_returns()
```

## Display Statistics

The `stats_calculator.py` includes the `display_statistics()` function, which calculates and displays key metrics such as:

- **Annualized Geometric Return**
- **Annualized Sharpe Ratio**
- **Skewness**
- **Maximum Monthly Drawdown**
- **Turnover**

To display statistics with significant figures:

```python
# Display Statistics
display_statistics(returns_dict, 4)  # 4 significant figures will be shown
```

## Contributing

If you wish to contribute:

1. **Fork the repository**.
2. **Create a new branch** for any changes.
3. **Submit a pull request** for review.

Contributions are welcomed and appreciated!

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Acknowledgments

This project was developed as part of a personal initiative to learn and practice systematic trading strategies. Special thanks to the open-source community for providing tools like Pandas, NumPy, and Matplotlib that made this project possible.


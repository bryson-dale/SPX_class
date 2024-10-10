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


## Acknowledgments

This project was developed as part of a personal initiative to learn and practice systematic trading strategies. Special thanks to the open-source community for providing tools like Pandas, NumPy, and Matplotlib that made this project possible.


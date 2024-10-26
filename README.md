# High-Frequency Trading Strategy with Kalman Filter

This project implements a high-frequency trading (HFT) strategy using a **Kalman Filter** for price prediction and a **threshold-based trading strategy** to execute buy/sell actions. The system fetches data from Binance and provides interactive control over parameters through a **Streamlit dashboard**.

## Features

- **Kalman Filter-based Predictions**: Smooths price data to capture true trends and signal meaningful price changes.
- **Configurable Trading Parameters**: Set thresholds, balance, and trading pair in a Streamlit dashboard.
- **Multiple Position Management**: Supports multiple positions to diversify trades and control risk.
- **Real-Time Visualization**: Visualizes price movements, buy/sell signals, and balance changes over time.

## Table of Contents

- [Project Structure](#project-structure)
- [Algorithm Overview](#algorithm-overview)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [License](#license)

## Project Structure

```plaintext
.
├── main.py                    # Main file to run the Streamlit app
├── kalman_filter.py           # Kalman Filter implementation
├── data_fetcher.py            # Module for fetching data from Binance
├── trading_strategy.py        # Trading strategy implementation
├── plotter.py                 # Plotting functions for Streamlit visualization
├── .env                       # Configuration file for environment variables
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## Algorithm Overview

### 1. Kalman Filter for Price Prediction

The **Kalman Filter** estimates future prices by filtering out noise. Each time step includes:
- **Prediction**: Forecasts the next price based on the current state.
- **Update**: Adjusts the prediction with observed data, refining the estimate.

This approach smooths out minor price fluctuations and helps the strategy focus on significant price changes.

### 2. Threshold-Based Trading Strategy

The algorithm evaluates the percentage change in the estimated price and compares it to defined buy/sell thresholds:
- **Buy Signal**: Opens a new position if the price increase exceeds the buy threshold.
- **Sell Signal**: Closes open positions if the price decrease meets the sell threshold.


### 3. Visualization

The Streamlit dashboard provides interactive control and visualizations:
- **Price and Signals Plot**: Shows real-time price, buy/sell signals, and estimated prices.
- **Balance Over Time**: Tracks balance changes, allowing users to assess performance.

## Setup and Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Pouryazv/high-frequency-trading-kalmanfilter.git
   cd Breadcrumbshigh-frequency-trading-kalmanfilter
   ```

2. **Install Dependencies**:
   Install required packages using `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
   
3. **Run the Streamlit Application**:
   Start the dashboard with:
   ```bash
   streamlit run main.py
   ```
   Open the URL provided in the terminal to view the dashboard.

## Usage

1. **Configure Parameters in the Dashboard**:
   - Set trading pair, time interval, start/end dates, and thresholds.
   - Adjust balance, Kalman Filter settings, and other parameters.

2. **Run and Monitor the Strategy**:
   - View price movements and buy/sell signals.
   - Track balance changes over time in response to trade performance.

3. **Analyze Performance**:
   - Use the balance and signals plots to evaluate trading strategy effectiveness.

## Configuration

- **Trading Settings**:
  - `TRADING_PAIR`: Trading pair symbol (e.g., `BTCUSDT`).
  - `INTERVAL`: Data interval (e.g., `1m`).
  - `START_DATE`, `END_DATE`: Trading period.

- **Kalman Filter Parameters**:
  - `PROCESS_NOISE_COVARIANCE` (Q)
  - `MEASUREMENT_NOISE_COVARIANCE` (R)
  - `INITIAL_ESTIMATE_ERROR` (P)
  - `INITIAL_STATE_ESTIMATE` (x)

- **Trading Thresholds**:
  - `BUY_THRESHOLD`: Minimum price change to trigger a buy (e.g., 0.005 for 0.5%).
  - `SELL_THRESHOLD`: Minimum price change to trigger a sell (e.g., -0.005 for -0.5%).


## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

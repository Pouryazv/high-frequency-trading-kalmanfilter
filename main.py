# main.py
import streamlit as st
from datetime import datetime, timezone
import numpy as np
import os
from kalman_filter import KalmanFilter
from data_fetcher import fetch_binance_data
from trading_strategy import run_trading_strategy
from plotter import plot_price_and_signals, plot_balance_over_time
import plotly.graph_objs as go





st.title("Trading Strategy Dashboard")


st.sidebar.header("Trading Parameters")

# Trading pair and date settings
trading_pair = st.sidebar.text_input("Trading Pair", os.getenv("TRADING_PAIR", "BTCUSDT"))
interval = st.sidebar.selectbox("Interval", ["1s","1m","3m", "5m", "15m"], index=0)
start_date = st.sidebar.text_input("Start Date (YYYY-MM-DDTHH:MM:SS)", os.getenv("START_DATE", "2024-10-01T00:00:00"))
end_date = st.sidebar.text_input("End Date (YYYY-MM-DDTHH:MM:SS)", os.getenv("END_DATE", "2024-11-01T00:00:00"))

# Trading thresholds
initial_balance = st.sidebar.number_input("Initial Balance (USD)", value=float(os.getenv("INITIAL_BALANCE", 10000)))
buy_threshold = st.sidebar.number_input("Buy Threshold (%)", min_value=0.0001, step=0.0001, value=0.005, format="%.3f")
sell_threshold = st.sidebar.number_input("Sell Threshold (%)", min_value=-0.9, step=0.0001, value=-0.005, format="%.3f")
max_positions = st.sidebar.number_input("Max Positions", min_value=1, value=5)

# Kalman Filter parameters
process_noise_cov = st.sidebar.number_input("Process Noise Covariance (Q)", value=float(os.getenv("PROCESS_NOISE_COVARIANCE", 1e-5)),format="%.5f")
measurement_noise_cov = st.sidebar.number_input("Measurement Noise Covariance (R)", value=float(os.getenv("MEASUREMENT_NOISE_COVARIANCE", 1e-2)),format="%.3f")
initial_estimate_error = st.sidebar.number_input("Initial Estimate Error (P)", value=float(os.getenv("INITIAL_ESTIMATE_ERROR", 1)))
initial_state_estimate = st.sidebar.number_input("Initial State Estimate (x)", value=float(os.getenv("INITIAL_STATE_ESTIMATE", 0)))


if st.sidebar.button("Run Trading Strategy"):
    try:
        start = datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc)
        end = datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc)

        # Fetch data from Binance
        ohlc_data = fetch_binance_data(trading_pair, interval, start, end)

        # Initialize Kalman Filter with user-defined parameters
        A = np.array([[1]])
        B = np.array([[0]])
        H = np.array([[1]])
        Q = np.array([[process_noise_cov]])
        R = np.array([[measurement_noise_cov]])
        P = np.array([[initial_estimate_error]])
        x = np.array([[initial_state_estimate]])

        kf = KalmanFilter(A, B, H, Q, R, P, x)
        
        # Run trading strategy and retrieve data for plotting
        actual_prices, estimated_prices, buy_signals, sell_signals, balance_history = run_trading_strategy(
            ohlc_data, kf, initial_balance, buy_threshold, sell_threshold, max_positions
        )

        # Display the price and signals plot
        st.subheader("Price and Signals")
        price_fig = plot_price_and_signals(ohlc_data, actual_prices, estimated_prices, buy_signals, sell_signals, trading_pair)
        st.plotly_chart(price_fig, use_container_width=True)

        # Display the balance over time plot
        st.subheader("Balance Over Time")
        balance_fig = plot_balance_over_time(balance_history)
        st.plotly_chart(balance_fig, use_container_width=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")

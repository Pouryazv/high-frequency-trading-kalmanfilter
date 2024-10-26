# trading_strategy.py
import numpy as np

def run_trading_strategy(ohlc_data, kalman_filter, initial_balance, buy_threshold, sell_threshold, max_positions=5, trade_percentage=0.2):
    balance = initial_balance
    total_profit = 0
    active_positions = []  
    trade_history = []


    actual_prices = []
    estimated_prices = []
    buy_signals = []
    sell_signals = []
    balance_history = [(ohlc_data.index[0], balance)]  
    previous_estimated_price = None

    for index, row in ohlc_data.iterrows():
        current_price = row['close']
        actual_prices.append(current_price)

        # Kalman filter prediction and update
        kalman_filter.predict()
        estimated_price = kalman_filter.update(np.array([[current_price]]))[0][0]
        estimated_prices.append(estimated_price)

        # Calculate price change estimate
        if previous_estimated_price is not None:
            price_change_estimate = ((estimated_price - previous_estimated_price) / previous_estimated_price) * 100
        else:
            price_change_estimate = 0
        previous_estimated_price = estimated_price

        # Buy logic: Open a new long position if below max_positions and buy signal is met
        if price_change_estimate > buy_threshold and len(active_positions) < max_positions:
            trade_amount = balance * trade_percentage
            if trade_amount > balance:
                trade_amount = balance 

            quantity = trade_amount / current_price
            entry_price = current_price
            position = {
                'type': 'long',
                'entry_price': entry_price,
                'quantity': quantity,
                'time': index
            }

            balance -= trade_amount
            active_positions.append(position)
            buy_signals.append((index, current_price))
            print(f"Opened Long Position: {quantity:.6f} units at {entry_price:.2f} on {index}")

        # Sell logic: Close long positions if sell signal is met
        if price_change_estimate < sell_threshold:
            for position in active_positions[:]:  
                if position['type'] == 'long':
    
                    exit_price = current_price
                    profit = (exit_price - position['entry_price']) * position['quantity']
                    total_profit += profit
                    balance += position['quantity'] * exit_price  
                    sell_signals.append((index, current_price))
                    active_positions.remove(position) 
                    trade_history.append({
                        'action': 'sell',
                        'entry_price': position['entry_price'],
                        'exit_price': exit_price,
                        'quantity': position['quantity'],
                        'profit': profit,
                        'time': index
                    })
                    print(f"Closed Long Position: {position['quantity']:.6f} units at {exit_price:.2f} on {index}, Profit: {profit:.2f}")

            balance_history.append((index, balance))

    final_balance = balance + sum([p['quantity'] * current_price for p in active_positions])
    print(f"\nFinal Results: Total Profit: {total_profit:.2f} USD, Final Balance: {final_balance:.2f} USD")

    return actual_prices, estimated_prices, buy_signals, sell_signals, balance_history

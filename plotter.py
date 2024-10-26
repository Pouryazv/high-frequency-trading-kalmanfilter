# plotter.py
import plotly.graph_objs as go

def plot_price_and_signals(ohlc_data, actual_prices, estimated_prices, buy_signals, sell_signals, symbol):
    fig = go.Figure()

    # Plot actual prices
    fig.add_trace(
        go.Scatter(
            x=ohlc_data.index,
            y=actual_prices,
            mode='lines',
            name='Actual Price',
            line=dict(color='blue')
        )
    )

    # Plot estimated prices
    fig.add_trace(
        go.Scatter(
            x=ohlc_data.index,
            y=estimated_prices,
            mode='lines',
            name='Estimated Price',
            line=dict(color='orange', dash='dot')
        )
    )

    # Plot buy signals as green triangles
    if buy_signals:
        buy_times, buy_prices = zip(*buy_signals)
        fig.add_trace(
            go.Scatter(
                x=buy_times,
                y=buy_prices,
                mode='markers',
                name='Buy Signal',
                marker=dict(symbol="triangle-up", color="green", size=10)
            )
        )

    # Plot sell signals as red triangles
    if sell_signals:
        sell_times, sell_prices = zip(*sell_signals)
        fig.add_trace(
            go.Scatter(
                x=sell_times,
                y=sell_prices,
                mode='markers',
                name='Sell Signal',
                marker=dict(symbol="triangle-down", color="red", size=10)
            )
        )

    # Customize layout
    fig.update_layout(
        title=f"Trading Strategy on {symbol}",
        xaxis_title="Time",
        yaxis_title="Price",
        template="plotly_dark",
        hovermode="x unified"
    )

    return fig

def plot_balance_over_time(balance_history):
    fig = go.Figure()


    if balance_history:
        balance_times, balances = zip(*balance_history)
        fig.add_trace(
            go.Scatter(
                x=balance_times,
                y=balances,
                mode='lines+markers',
                name='Balance After Trade',
                line=dict(color='purple'),
                marker=dict(symbol="circle", size=6)
            )
        )


    fig.update_layout(
        title="Balance Over Time",
        xaxis_title="Time",
        yaxis_title="Balance (USD)",
        template="plotly_dark",
        hovermode="x unified"
    )

    return fig

import streamlit as st
import os
import pandas as pd
import plotly.graph_objects as go
import json
from datetime import datetime, timedelta

import settings

def add_chart(records):
    with st.beta_expander("Chart"):
        fig = go.Figure()

        lines = st.multiselect("", records.columns, key="lines")
        marker = st.multiselect("", records.columns, key="markers")

        for col in lines:
            trace = go.Scatter(x=records.index, y=records[col], name=col, mode='lines')
            fig.add_trace(trace)

        for col in marker:
            trace = go.Scatter(x=records.index, y=records[col], name=col, mode='markers')
            fig.add_trace(trace)

        st.plotly_chart(fig, use_container_width=True)

def equity_chart(quity_data):
    fig = go.Figure()
    trace = go.Scatter(x=quity_data.index, y=quity_data, name="equity", mode='lines')
    fig.add_trace(trace)
    st.plotly_chart(fig, use_container_width=True)

def trades_chart(trades, price_data):
    
    fig = go.Figure()
    data = pd.DataFrame()
    symbols = set()

    for trade in trades:
        symbol = trade["symbol"]
        time = datetime.fromisoformat(trade["time"])

        # parse the trades into dataframe
        if trade["qty"] > 0:
            data.loc[time, f"buy {symbol}"] = trade["price"]
        else:
            data.loc[time, f"sell {symbol}"] = trade["price"]

        if symbol not in symbols:
            # plot the asset prices
            symbols.add(symbol)
            trades = go.Scatter(x=price_data.index, y=price_data[symbol], name=symbol, mode='lines')
            fig.add_trace(trades)

    for col in data.columns:

        if "buy" in col:
            trades = go.Scatter(x=data.index, y=data[col], name=col, mode='markers', marker={"color": "green"})
        else:
            trades = go.Scatter(x=data.index, y=data[col], name=col, mode='markers', marker={"color": "red"})

        fig.add_trace(trades)

    st.plotly_chart(fig, use_container_width=True)


def display_statistics(stats):
    st.json(stats)

def app():
    st.title("Backtest Results")
    
    result_path = settings.get_value("backtest_path")
    options = os.listdir(result_path)

    file = st.selectbox("Select Result", options)
    result_folder = os.path.join(result_path, file)

    records = pd.read_csv(os.path.join(result_folder, "records.csv"), index_col=0)

    with open(os.path.join(result_folder, "trades.json"), "r") as f:
        trades = json.load(f)

    with open(os.path.join(result_folder, "statistics.json"), "r") as f:
        statistics = json.load(f)

    equity_chart(records.equity)
    trades_chart(trades, records)
    display_statistics(statistics)



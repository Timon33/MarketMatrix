import streamlit as st
import os
import sys
from importlib import import_module, reload
from datetime import datetime, timedelta
import multiprocessing
import shutil
import json

from market import simulation
import settings

interval_options = [
    "1m",
    "15m",
    "30m",
    "1h",
    "1d",
    "1wk"
]

def load_strategy(name):
    source = import_module(name)
    # might been changed and rerun
    reload(source)
    return getattr(source, name)

def create_statistics(strategy) -> dict:
    return {
        "net-liq": strategy.net_liq
    }

# executed by seperate process
def run_backtest(name, strategy, start_date, end_date, starting_cash, interval):
    sim = simulation.BacktestSimulation(strategy, start_date, end_date=end_date, starting_cash=starting_cash, interval=interval)
    sim.strategy.fee = float(settings.get_value("stock_fee")) / 100
    strategy = sim.run()

    backtest_folder = settings.get_value("backtest_path")
    result_folder = os.path.join(backtest_folder, name)

    # clear folder
    if not os.path.isfile(result_folder):
        if os.path.isdir(result_folder):
            shutil.rmtree(result_folder)
        os.mkdir(result_folder)

    else:
        raise FileExistsError()

    with open(os.path.join(result_folder, "records.csv"), "w") as f:
        strategy.recordings.to_csv(f)

    statistics = create_statistics(strategy)
    with open(os.path.join(result_folder, "statistics.json"), "w") as f:
        json.dump(statistics, f)

# entry
def app():

    # file selector
    st.title("Lauch new Strategy")
    strategys_path = settings.get_value("strategys_path")
    
    sys.path.append(strategys_path)
    files = []
    for f in os.listdir(strategys_path):
        if not os.path.isfile(os.path.join(strategys_path, f)):
            continue

        try:
            name, ext = f.split(".")[:2]
        except AttributeError():
            continue

        if ext == "py":
            files.append(name)

    st.subheader("Select file")
    file = st.radio("", files)

    with st.beta_expander("Backtest"):

        # parameter selector
        name = st.text_input("Strategy Name")

        c1, c2 = st.beta_columns(2)
        with c1: start_date = st.date_input("From", value=datetime.today() - timedelta(weeks=208))
        with c2: end_date = st.date_input("To", value=datetime.today())

        with c1: interval = st.selectbox("Data interval", interval_options, index=4)
        with c2: starting_cash = int(st.text_input("starting cash", value=100000))

        if st.button("Run", key="backtest"):
            # run backtest process
            strategy = load_strategy(file)
            proc = multiprocessing.Process(target=run_backtest, args=(name, strategy, start_date, end_date, starting_cash, interval))
            proc.start()

            with st.spinner("Running Backtest"):
                proc.join()
            
            st.success("Backtest complete")

    with st.beta_expander("Live"):
        
        if st.button("Run", key="live"):
            # run thread
            pass
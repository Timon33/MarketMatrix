import streamlit as st
import os
import pandas as pd

import settings

def app():
    st.title("Backtest Results")
    
    result_folder = settings.get_value("backtest_path")
    options = os.listdir(result_folder)

    file = st.radio("Select Result", options)



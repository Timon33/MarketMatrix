import streamlit as st
import os

import algo_laucher, settings, backtest_viewer, live_viewer

st.set_page_config(
    page_title="LEAN Webapp",
    layout="wide",
    initial_sidebar_state="expanded"
)

pages = {
    "Live": live_viewer,
    "Backtest": backtest_viewer,
    "Lauch": algo_laucher,
    "Settings": settings,
}

# simple selection to call the coresponding file for each page
def app(index=0):
    st.sidebar.title('Navigation')

    selection = st.sidebar.radio("", list(pages.keys()), index=index)
    page = pages[selection]
    page.app()

app()

"""
Dans ce fichier, nous avons crée le dashboard qui nous permettra d'analyser 
les données recueilli dans notre fichier des donnés sur les achats de Tecno FP.
"""
# Librairies
import pandas as pd
import streamlit as st
import plotly.express as px
import altair as alt
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.metric_cards import style_metric_cards

# Config page
st.set_page_config(
    page_title="Tecno FP Business", 
    layout="wide", 
    page_icon=":material/bar_chart:"
)

# Page Setup

dashboard = st.Page(
    page="dashboard.py",
    title="ST DashBoard",
    icon=":material/bar_chart:",
    default= True
)

dashboard2 = st.Page(
    page = "dashboard_sd.py",
    title = "SD DashBoard",
    icon = ":material/bar_chart:"
)

report = st.Page(
    page = "report.py",
    title = "TECNO FP REPORT",
    icon = ":material/bar_chart:"
)

about_me = st.Page(
    page = "about_me.py",
    title = "About Me",
    icon = ":material/account_circle:" 
)

# Navigation betwen pages
page = st.navigation(
    {
        "Dashboard":[dashboard, dashboard2],
        "Report":[report],
        "Info":[about_me]

    }
    
)


# --- SHARED ON ALL PAGES ---
st.logo("./images/easy-logo.jpg")
st.sidebar.text("Made with ❤ by RodrigueN")

# --- RUN NAVIGATION ---
page.run()

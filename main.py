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
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly

# Config page
st.set_page_config(
    page_title="Tecno Business Analytics", 
    layout="wide", 
    page_icon=":material/bar_chart:"
)

# Page Setup

about_me = st.Page(
    page = "about_me.py",
    title = "About Me",
    icon = ":material/account_circle:",
    default= True
)

dashboard = st.Page(
    page="dashboard.py",
    title="ST DashBoard for FP",
    icon=":material/bar_chart:"
    
)


dashboard2 = st.Page(
    page = "dashboard_sd.py",
    title = "SD DashBoard for FP",
    icon = ":material/bar_chart:"
)

dashboard3 = st.Page(
    page = "dashboard_so.py",
    title = "SO DashBoard for FP",
    icon = ":material/bar_chart:"
)

dashboard4 = st.Page(
    page="SP_dashboard_ST.py",
    title="ST DashBoard for SP",
    icon=":material/bar_chart:",
   
)

dashboard5 = st.Page(
    page="SP_dashboard_sd.py",
    title="SD DashBoard for SP",
    icon=":material/bar_chart:",
)


dashboard6 = st.Page(
    page = "dashboard_retail.py",
    title = "TECNO RETAIL BUSINESS",
    icon = ":material/bar_chart:"
)

report = st.Page(
    page = "report.py",
    title = "TECNO BUSINESS REPORT",
    icon = ":material/bar_chart:"
)

converter = st.Page(
    page = "csv_converter.py",
    title = "Excel to CSV Converter",
    icon = ":material/file_download:"
)

fusion_file = st.Page(
    page= "fusion_excel_to_csv.py",
    title= "Combine multiple Excel files",
    icon= ":material/file_download:"
)

# Navigation betwen pages
page = st.navigation(
    {
        "Info":[about_me],
        "Dashboard FP":[dashboard, dashboard2, dashboard3],
        "Dashboard SP":[dashboard4, dashboard5],
        "Retail Dashboard":[dashboard6],
        "Fusion Excel to CSV":[fusion_file],
        "Converter":[converter],
        "Report":[report]

    }
    
)


# --- SHARED ON ALL PAGES ---
st.logo("./images/easy-logo.jpg")
st.sidebar.text("Made with ❤ by RodrigueN")

# --- RUN NAVIGATION ---
page.run()

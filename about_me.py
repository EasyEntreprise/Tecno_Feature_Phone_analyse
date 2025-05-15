# IMPORTATION LIBRAIRIES
import pandas as pd
import plotly.express as px
import streamlit as st


# DETAILS
#"""
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
    st.image("./images/rodrigue-N.png", width=380)

with col2:
    st.title("Rodrigue NSINSULU", anchor=False)
    st.write(
        "Junior Data Analyst, Data Engener, Data Scientist, Machine and Deep Learning and  IT Cyber-security.",
        "C.E.O at Easy Holding"
    )
#"""

# --- EXPERIENCE AND QUALIFICATION ---
st.write("\n")
st.subheader("Experience and Qualifications", anchor=False)
st.write(
    """
    - 6 Years experience in sell's phone domain,
    - 2 Years experience extracting actionable insights from data
    - Strong hands-on experience and knowledge in Python and Excel
    - Good understanding of statistical principles and their respective application
    - Excellent team-player and displaying a strong sense of initiative on tasks
    - 2 Years in Cyber-security domain
    """
)

# --- SKILLS ---
st.write("\n")
st.subheader("Hard Skills", anchor=False)
st.write(
    """
    - Programming : Python (Scikit-learn, Pandas, Numpy, PySide), SQL
    - Data Visualisation : Plotly, Dash, Streamlit, PowerBI, Ms Excel
    - Modeling : Logistic regression, linear regression, decision trees
    - Databases : MySQL, MongoDB, Postgres
    """
)

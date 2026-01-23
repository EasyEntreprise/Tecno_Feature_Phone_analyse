# IMPORTATION LIBRAIRIES
import pandas as pd
import plotly.express as px
import streamlit as st
import time
import os
import sys
from PIL import Image, ImageTk
from tkinter import *



# DETAILS
#"""
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
    st.image("./images/Rodrigue folio-1.png", width=380)
    

with col2:
    st.title("Rodrigue NSINSULU MAYANZA", anchor=False)
    st.write(
        "Junior Data Analyst, Data Engener, Data Scientist, Machine and Deep Learning and  IT Cyber-security.",
        "C.E.O at Easy Holding"
    )
    st.markdown("[GMAIL](https://www.gmail.com)")
#"""

# --- EXPERIENCE AND QUALIFICATION ---
st.write("\n")

col3, col4 = st.columns(2)

with col3 :
    st.subheader("Experience and Qualifications", anchor=False)
    st.write(
        """
        - 7 Years of experience in  the business of selling Tecno brand phone ;
        - 3 Years experience extracting actionable insights from data ;
        - Strong hands-on experience and knowledge in Python and Excel ;
        - Good understanding of statistical principles and their respective application ;
        - Excellent team-player and displaying a strong sense of initiative on tasks ;
        - 2 Years in CyberSecurity domain.
        """
    )
with col4 :
    # --- SKILLS ---
    #st.write("\n")
    st.subheader("Hard Skills", anchor=False)
    st.write(
        """
        - Software Engineer      : Python (Scikit-learn, Pandas, Numpy, PySide, django), C++, Desktop, Mobile and full-stack developer ;
        - Data Visualisation     : Plotly, Dash, Streamlit, PowerBI, Ms Excel ;
        - Modeling               : Logistic regression, linear regression, decision trees ;
        - Database Administrator : MySQL, MongoDB, Postgres and NO-SQL ;
        - Data Engineer          : Data Engineer, Data Analyst, Data Science and Machine-Deep Learning ;
        - Security               : CyberSecurity Engineer.
        """
    )

st.markdown("___")
# Boutons fermeture et rederamarrage
null, ferm, rederm = st.columns(3)

with null:
    pass

with ferm:
    # ------------------------------
    # 🔴 Bouton Fermer (avec confirmation)
    # ------------------------------
    if "confirm_exit" not in st.session_state:
        st.session_state.confirm_exit = False

    if st.session_state.confirm_exit:
        st.warning("❗ Are you sure you want to stop using the application altogether ?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes, stop "):
                st.error("🛑 Closing the application... ")
                time.sleep(1)
                os._exit(0)
        with col2:
            if st.button("❌ No, cancel "):
                st.session_state.confirm_exit = False
    else:
        if st.button("🛑 Close application "):
            st.session_state.confirm_exit = True

with rederm:
    pass

st.markdown("___")

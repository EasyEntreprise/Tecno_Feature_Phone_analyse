import streamlit as st
import pandas as pd
from io import StringIO

#############################
### Title 
####################
st.markdown("<h1 style='text-align: center; color: blue;'> Excel Converter ➜ CSV </h1>", unsafe_allow_html= True)
st.markdown("<br/>", unsafe_allow_html= True)
st.markdown("<br/>", unsafe_allow_html= True)

st.markdown("___")
st.title("Excel Converter ➜ CSV")

# Upload du fichier Excel
uploaded_file = st.file_uploader(
    "Select an Excel file (.xlsx, .xls)",
    type=["xlsx", "xls"]
)

if uploaded_file is not None:
    # Optionnel : choisir la feuille
    try:
        xls = pd.ExcelFile(uploaded_file)
        sheet_name = st.selectbox(
            "Select the sheet to convert",
            xls.sheet_names
        )

        # Lecture de la feuille choisie
        df = pd.read_excel(xls, sheet_name=sheet_name)

        st.subheader("Data overview")
        st.dataframe(df.head())

        # Conversion en CSV (en mémoire)
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_bytes = csv_buffer.getvalue().encode("utf-8")

        # Bouton de téléchargement
        st.download_button(
            label="📥 Download as CSV",
            data=csv_bytes,
            file_name=f"{sheet_name}.csv",
            mime="text/csv"
        )
    except Exception as e:
        st.error(f"Error reading file : {e}")
else:
    st.info("Please import an Excel file to get started..")

import streamlit as st
import pandas as pd
from io import BytesIO, StringIO

#############################
### Title 
####################
st.markdown("<h1 style='text-align: center; color: blue;'> Merge multiple Excel files ➜ 1 Excel + CSV </h1>", unsafe_allow_html= True)
st.markdown("<br/>", unsafe_allow_html= True)
st.markdown("<br/>", unsafe_allow_html= True)
st.markdown("___")

st.title("Merge multiple Excel files ➜ 1 Excel + CSV")

st.write("""
Load multiple Excel files with the same columns.
They will be merged into a single table, which you can download in:
- 📄 Excel file (.xlsx)
- 📄 Fichier CSV (.csv)
""")

# Upload multiple Excel files
uploaded_files = st.file_uploader(
    "Select multiple Excel files",
    type=["xlsx", "xls"],
    accept_multiple_files=True
)

if uploaded_files:
    dataframes = []

    for file in uploaded_files:
        try:
            # Lecture du premier onglet (sheet) par défaut
            df = pd.read_excel(file)
            df["__Source_File__"] = file.name  # Optionnel : garder la source
            dataframes.append(df)
        except Exception as e:
            st.error(f"Error reading {file.name} : {e}")

    if dataframes:
        # Fusion de tous les DataFrames
        merged_df = pd.concat(dataframes, ignore_index=True)

        st.subheader("Overview of merged data")
        st.dataframe(merged_df.head())

        st.write(f"Total number of merged lines : **{len(merged_df)}**")

        # ====== Téléchargement en Excel ======
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
            merged_df.to_excel(writer, index=False, sheet_name="Fusion")
        excel_buffer.seek(0)

        st.download_button(
            label="📥 Download the merged Excel file",
            data=excel_buffer,
            file_name="Fusion files.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # ====== Téléchargement en CSV ======
        csv_buffer = StringIO()
        merged_df.to_csv(csv_buffer, index=False)
        csv_bytes = csv_buffer.getvalue().encode("utf-8")

        st.download_button(
            label="📥 Download the merged CSV file",
            data=csv_bytes,
            file_name="Fusion files.xlsx",
            mime="text/csv"
        )
    else:
        st.warning("No valid file could be read.")
else:
    st.info("Import at least two Excel files to get started.")

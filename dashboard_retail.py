# Librairies
import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.metric_cards import style_metric_cards
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import os
import time


#############################
### Title 
####################
st.markdown("<h1 style='text-align: center; color: blue;'> TECNO BUSINESS DASHBOARD </h1>", unsafe_allow_html= True)
st.markdown("<br/>", unsafe_allow_html= True)
st.markdown("<br/>", unsafe_allow_html= True)
st.markdown("<h6 style='text-align: center; color: red;'> Welcome in our feature phone dashboard for Tecno brand DRC. This dashboard is important for following the ST purchase of customers."
"In this "
"</h6>", unsafe_allow_html= True)

st.markdown("___")

######################################
## Boutons fermeture et rederamarrage
#####################################
ferm, rederm = st.columns(2)
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
    # ------------------------------
    # 🔄 Bouton Redémarrer (avec confirmation)
    # ------------------------------
    if "confirm_restart" not in st.session_state:
        st.session_state.confirm_restart = False

    if st.session_state.confirm_restart:
        st.warning("❗ Are you sure you want to restart the application ? ")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes, restart "):
                st.info("🔄 Restarting the application...")
                time.sleep(1)
                st.experimental_rerun()
        with col2:
            if st.button("❌ No, cancel"):
                st.session_state.confirm_restart = False
    else:
        if st.button("🔄 Restart application "):
            st.session_state.confirm_restart = True

st.markdown("___")

##############################
### Fonction de lecture de fichier
###############################

def read_file(file):
    """Lit automatiquement Excel ou CSV selon le type du fichier."""
    if file is None:
        return None
    
    filename = file.name.lower()

    if filename.endswith(".csv"):
        return pd.read_csv(file)
    elif filename.endswith(".xlsx") or filename.endswith(".xls"):
        return pd.read_excel(file)
    else:
        st.error("Format not supported. Use Excel. (.xlsx/.xls) ou CSV.")
        return None

# Load dataset
sale = st.file_uploader("📂 Insert your Excel Sale file by pressing the 'Browse files' button", type=["xlsx","xls"])
coverage = st.file_uploader("Insert your Excel Inventory file by pressing the 'Browse files' button", type=["xlsx", "xls"])

if sale is not None:

    #achat_1 = pd.read_excel(sale)
    achat_1 = read_file(sale)
    achat = achat_1.dropna(subset="Sales Qty") # On supprime les lignes qui n'ont pas de vente ou de quantite de vente

    couverture_1 = pd.read_excel(coverage, sheet_name="Shop Inventory Query")
    couverture = couverture_1.dropna(subset="Available Quantity") # On supprime les lignes qui n'ont pas de quantite disponible

    #######################################
    ###### Traitement du fichier ##########
    # ##################################### 
    
    # Suppresionn des colonnes de l'achat
    cols_to_drop_inv = ["Brand", "Series",	"First Category", "Item", "Market Name", "Color", "Memory",	"Manpower Type", "Retailer ID",	"Retailer Name", "Public ID", "Shop Type",	"Shop Grade",	"Image Type", "Sales Region 1",	"Sales Region 4", "Sales Region 5", "Remark"] # Suppresion des colonnes de la couverture
    
    # Ne garder que les colonnes qui existent réellement pour la couverture :
    cols_to_drop_inv = [inv for inv in cols_to_drop_inv if inv in couverture.columns]
    couverture_drop = couverture.drop(cols_to_drop_inv, axis=1)

    # Renommer une colonne
    couverture_dr = couverture_drop.rename(columns={"Sales Region 2":"Sales Region", "State":"Region", "City":"Market"}) # Renomer la colonne 'Sales Region'
    
    # Convertir en datetime
    achat["Sales Date"] = pd.to_datetime(achat["Sales Date"], errors="coerce") # Mettre la colonne 'Sales Date' en format date
    
    
    # Renommer les elements des colonnes
  
    couverture_dr["Region"] = np.where(couverture_dr["Region"] == "Haut- Katanga", "BIG KATANGA", couverture_dr["Region"])
    couverture_dr["Region"] = np.where(couverture_dr["Region"] == "Lualaba", "BIG KATANGA", couverture_dr["Region"])
    couverture_dr["Region"] = np.where(couverture_dr["Region"] == "Kasai", "BIG KASAI", couverture_dr["Region"])
    couverture_dr["Region"] = np.where(couverture_dr["Region"] == "Kasai Centrale", "BIG KASAI", couverture_dr["Region"])
    couverture_dr["Region"] = np.where(couverture_dr["Region"] == "Kasai Orientale", "BIG KASAI", couverture_dr["Region"])
    couverture_dr["Region"] = np.where(couverture_dr["Region"] == "Kwilu", "BIG EQUATOR", couverture_dr["Region"])
    couverture_dr["Region"] = np.where(couverture_dr["Region"] == "Sud-Ubangi", "BIG EQUATOR", couverture_dr["Region"])
    couverture_dr["Region"] = np.where(couverture_dr["Region"] == "Kongo Centrale", "KONGO CENTRAL", couverture_dr["Region"])
    couverture_dr["Region"] = np.where(couverture_dr["Region"] == "Big Equateur", "BIG EQUATOR", couverture_dr["Region"])
    couverture_dr["SP/FP"]  = np.where(couverture_dr["SP/FP"] == "PAD", "Smart", couverture_dr["SP/FP"])
    couverture_dr["SP/FP"]  = np.where(couverture_dr["SP/FP"] == "Pad", "Smart", couverture_dr["SP/FP"])
    couverture_dr["SP/FP"]  = couverture_dr["SP/FP"].fillna("Accessories")

    
    # Select Date
    col1, col2 = st.columns(2)
            
    with col1:
        st.text("Select Date Range")
        start_date = st.date_input(label="Start Dates")

    with col2:
        st.text("Select Date Range")
        en_date = st.date_input(label="End Dates")

    # Provide a message for selected date range 
    st.success(" you have choosen analytics from: "+str(start_date)+" to "+str(en_date))
    
    
    # Choisir entre FSM Shops, PR Shops ou TPR Shops
    st.markdown("___")
    category = ["FSM", "PR", "TPR"]
    category.insert(0, "ALL") # On ajoute l’option "Tous"
    select_categories = st.selectbox("Chose your category between :", category)

    st.markdown("___")

    # Filtre dates

    select_date = achat[(achat["Sales Date"]>=str(start_date)) & (achat["Sales Date"]<=str(en_date))]
    
    if select_categories == "ALL":
        date_frame = select_date
    else:
        date_frame = select_date[select_date["Shop Type"] == select_categories]
    
    date_frame_all = select_date.copy()
    

    with st.expander("Filter dates"):
        filter_date = dataframe_explorer(date_frame, case=False)
        st.dataframe(filter_date, use_container_width= True)

    
    ##############################
    ####### DATA METRIC ##########
    ##############################

    col1, col2 = st.columns(2)

    with col1 :
        sales_sp = date_frame[date_frame["SP/FP"] == "Smart"]
        sales_fp = date_frame[date_frame["SP/FP"] == "Feature"]
        gen_sales_sp = sales_sp["Sales Qty"].sum()
        gen_sales_fp = sales_fp["Sales Qty"].sum()

        st.metric(label="General Sales Situation", value= f"Smart Phone : {gen_sales_sp}", delta= f"Feature Phone : {gen_sales_fp}")
        

    with col2 :
        coverage_sp = couverture_dr[couverture_dr["SP/FP"] == "Smart"]
        coverage_fp = couverture_dr[couverture_dr["SP/FP"] == "Feature"]
        gen_cov_sp = coverage_sp["Available Quantity"].sum()
        gen_cov_fp = coverage_fp["Available Quantity"].sum()

        st.metric(label="General Coverage Situation", value= f"Coverage Smart Phone {gen_cov_sp}", delta= f"Coverage Feature Phone {gen_cov_fp}")
        

    col3, col4, col5, col6, col7, col8 = st.columns(6)

    with col3 :
        kina_sales = date_frame[date_frame["Region"] == "KINSHASA ZONE A"]
        kina_cover = couverture_dr[couverture_dr["Region"] == "KINSHASA ZONE A"]

        kina_sales["Sales Qty"] = kina_sales["Sales Qty"].fillna(0).astype(int) # Conversion de la colonne "Sales Qty" en entier tout en remplaçant les valeurs manquantes par 0
        kina_cover["Available Quantity"] = kina_cover["Available Quantity"].fillna(0).astype(int)


        if not kina_sales.empty or (not kina_cover.empty) :
            st.metric(label="KINSHASA ZONE A Sales", value= int(kina_sales["Sales Qty"].fillna(0).sum()), delta= f"Coverage KINSHASA ZONE A : {int(kina_cover['Available Quantity'].fillna(0).sum())}") # La Situation de la vente de la region Big Kasai avec situation couverture comme delta

        else :
            st.metric(label="KINSHASA ZONE A Sales", value= 0, delta= "Coverage KINSHASA ZONE A : 0")
        
        

    with col4 :
        kinb_sales = date_frame[date_frame["Region"] == "KINSHASA ZONE B"]
        kinb_cover = couverture_dr[couverture_dr["Region"] == "KINSHASA ZONE B"]

        kinb_sales["Sales Qty"] = kinb_sales["Sales Qty"].fillna(0).astype(int) # Conversion de la colonne "Sales Qty" en entier tout en remplaçant les valeurs manquantes par 0
        kinb_cover["Available Quantity"] = kinb_cover["Available Quantity"].fillna(0).astype(int)


        if not kinb_sales.empty or (not kinb_cover.empty) :
            st.metric(label="KINSHASA ZONE B Sales", value= int(kinb_sales["Sales Qty"].fillna(0).sum()), delta= f"Coverage KINSHASA ZONE B : {int(kinb_cover['Available Quantity'].fillna(0).sum())}") # La Situation de la vente de la region Big Kasai avec situation couverture comme delta

        else :
            st.metric(label="KINSHASA ZONE B Sales", value= 0, delta= "Coverage KINSHASA ZONE B : 0")
        

    with col5 :
        bka_sales = date_frame[date_frame["Region"] == "BIG KATANGA"]
        bka_cover = couverture_dr[couverture_dr["Region"] == "BIG KATANGA"]

        bka_sales["Sales Qty"] = bka_sales["Sales Qty"].fillna(0).astype(int) # Conversion de la colonne "Sales Qty" en entier tout en remplaçant les valeurs manquantes par 0
        bka_cover["Available Quantity"] = bka_cover["Available Quantity"].fillna(0).astype(int)


        if not bka_sales.empty or (not bka_cover.empty) :
            st.metric(label="BIG KATANGA Sales", value= int(bka_sales["Sales Qty"].fillna(0).sum()), delta= f"Coverage BIG KATANGA : {int(bka_cover['Available Quantity'].fillna(0).sum())}") # La Situation de la vente de la region Big Kasai avec situation couverture comme delta

        else :
            st.metric(label="BIG KATANGA Sales", value= 0, delta= "Coverage BIG KATANGA : 0")
        

    with col6 :
        kc_sales = date_frame[date_frame["Region"] == "KONGO CENTRAL"]
        kc_cover = couverture_dr[couverture_dr["Region"] == "KONGO CENTRAL"]

        kc_sales["Sales Qty"] = kc_sales["Sales Qty"].fillna(0).astype(int) # Conversion de la colonne "Sales Qty" en entier tout en remplaçant les valeurs manquantes par 0
        kc_cover["Available Quantity"] = kc_cover["Available Quantity"].fillna(0).astype(int)


        if not kc_sales.empty or (not kc_cover.empty) :
            st.metric(label="Kongo Central Sales", value= int(kc_sales["Sales Qty"].fillna(0).sum()), delta= f"Coverage Kongo Central : {int(kc_cover['Available Quantity'].fillna(0).sum())}") # La Situation de la vente de la region Big Kasai avec situation couverture comme delta

        else :
            st.metric(label="Kongo Central Sales", value= 0, delta= "Coverage Kongo Central : 0")
        

    with col7 :
        bk_sales = date_frame[date_frame["Region"] == "BIG KASAI"]
        bk_cover = couverture_dr[couverture_dr["Region"] == "BIG KASAI"]

        bk_sales["Sales Qty"] = bk_sales["Sales Qty"].fillna(0).astype(int) # Conversion de la colonne "Sales Qty" en entier tout en remplaçant les valeurs manquantes par 0
        bk_cover["Available Quantity"] = bk_cover["Available Quantity"].fillna(0).astype(int)


        if not bk_sales.empty or (not bk_cover.empty) :
            st.metric(label="BIG KASAI Sales", value= int(bk_sales["Sales Qty"].fillna(0).sum()), delta= f"Coverage Big Kasai : {int(bk_cover['Available Quantity'].fillna(0).sum())}") # La Situation de la vente de la region Big Kasai avec situation couverture comme delta

        else :
            st.metric(label="BIG KASAI Sales", value= 0, delta= "Coverage BIG KASAI : 0")
        

    with col8 :
        be_sales = date_frame[date_frame["Region"] == "BIG EQUATOR"]
        be_cover = couverture_dr[couverture_dr["Region"] == "BIG EQUATOR"]

        be_sales["Sales Qty"] = be_sales["Sales Qty"].fillna(0).astype(int) # Conversion de la colonne "Sales Qty" en entier tout en remplaçant les valeurs manquantes par 0
        be_cover["Available Quantity"] = be_cover["Available Quantity"].fillna(0).astype(int)


        if not be_sales.empty or (not be_cover.empty) :
            st.metric(label="Big Equator Sales", value= int(be_sales["Sales Qty"].fillna(0).sum()), delta= f"Coverage Big Equator : {int(be_cover['Available Quantity'].fillna(0).sum())}") # La Situation de la vente de la region Big Kasai avec situation couverture comme delta

        else :
            st.metric(label="Big Equator Sales", value= 0, delta= "Coverage Big Equator : 0")

    
    # Style the metric
    style_metric_cards(background_color="#3c4d66", border_left_color="#99f2c8", border_color="#0006a")    

    
    ###################
    ##################
    # GRAPHIC
    # #################

    st.subheader("I. GRAPHIC EXPLORE", divider="rainbow")

    cola, colb = st.columns(2)

    with cola :

        ###
        st.subheader("1- Yearly Sales for SMART PHONE")
        yearly_sales = date_frame[date_frame["SP/FP"] == "Smart"]
        yearly_sales = yearly_sales.groupby("Years", as_index= False)["Sales Qty"].sum()

        fig_years = px.line(yearly_sales, x="Years", y="Sales Qty", text="Sales Qty")
        fig_years.update_traces(textposition = 'top center')
        st.plotly_chart(fig_years)

        st.markdown("___")

        ###
        st.subheader("3- Monthly Sales for SMART PHONE")

        monthly_sales = date_frame[date_frame["SP/FP"] == "Smart"]
        monthly_sales = monthly_sales.groupby("Month", as_index= False)["Sales Qty"].sum()

        fig_month = px.line(monthly_sales, x="Month", y="Sales Qty", text="Sales Qty")
        fig_month.update_traces(textposition = 'top center')
        st.plotly_chart(fig_month)
        
        st.markdown("___")
        
        ###
        st.subheader("5- Sales by regions for SMART PHONE")
        
        sales = date_frame[date_frame["SP/FP"] == "Smart"]
        regions_sales = sales.groupby("Region", as_index= False)["Sales Qty"].sum()

        fig_region = px.bar(regions_sales, x="Region", y="Sales Qty", text="Sales Qty", color="Region")
        fig_region.update_traces(textposition = 'outside')
        st.plotly_chart(fig_region)
        
        st.markdown("___")
        
        ###
        st.subheader("7- Coverage by regions for SMART PHONE")

        cover = couverture_dr[couverture_dr["SP/FP"] == "Smart"]
        regions_cover = cover.groupby("Region", as_index= False)["Sales Qty"].sum()

        fig_region_cover = px.bar(regions_cover, x="Region", y="Available Quantity", text="Available Quantity", color="Region")
        fig_region_cover.update_traces(textposition = 'outside')
        st.plotly_chart(fig_region_cover)
        
        st.markdown("___")

        ####
        st.subheader("9- Sales by models for SMART PHONE")
        
        smart = date_frame[date_frame["SP/FP"] == "Smart"]
        choose_region = smart["Region"].unique()
        # Selectionner une region
        selected_region = st.selectbox("Choose your region for sales", choose_region) # On selectionne une region
        # Filtrer les donnees par la region choisie
        region_choose = smart[smart["Region"].isin(selected_region)]
        # Grouper par modele et sommer les ventes
        region_models = (
            region_choose
            .groupby(["Models"], as_index= False)["Sales Qty"].sum()
        )

        fig_sept = px.bar(region_models, x="Models", y="Sales Qty", text="Sales Qty", color="Models")
        fig_sept.update_traces(textposition = 'outside')
        st.plotly_chart(fig_sept)
        
        st.markdown("___")

        ####
        st.subheader("11- Coverage by models for SMART PHONE")

        smart_cov = couverture_dr[couverture_dr["SP/FP"] == "Smart"]
        cov_region = smart_cov["Region"].unique()
        select_region_cov = st.selectbox("Choose your region coverage", cov_region) # On selectionne une region
        region_cover = smart_cov[smart_cov["Region"] == select_region_cov]
        cover_region = region_cover.groupby("Model", as_index= False)["Available Quantity"].sum()
        
        fig_neuf = px.bar(cover_region, x="Models", y="Available Quantity", text="Available Quantity", color="Models")
        fig_neuf.update_traces(textposition = 'outside')
        st.plotly_chart(fig_neuf)
        
        st.markdown("___")
        
        ###
        st.subheader("13- Sales by market for SMART PHONE")
        market_choose = smart[smart["Region"].isin(selected_region)]
        choose_market = market_choose.groupby("Market", as_index= False)["Sales Qty"].sum()
        
        fig_onze = px.bar(choose_market, x="Market", y="Sales Qty", text="Sales Qty", color="Market")
        fig_onze.update_traces(textposition = 'outside')
        st.plotly_chart(fig_onze)

        st.markdown("___")
        
        ###
        st.subheader("15- Coverage by market for SMART PHONE")
        market_cover = smart_cov[smart_cov["Region"].isin(cov_region)]
        cover = market_cover.groupby("Market", as_index= False)["Available Quantity"].sum()
        
        fig_treize = px.bar(cover, x="Market", y="Available Quantity", text="Available Quantity", color="Market")
        fig_treize.update_traces(textposition = 'outside')
        st.plotly_chart(fig_treize)

        st.markdown("___")
        
        
        ###
        st.subheader("17- Regional Manager sales for SMART PHONE")
        # Graphic en Pie
        rm = smart.groupby("Regional Manager", as_index= False)["Sales Qty"].sum()
        graph_rm_pie = go.Figure(data=[go.Pie(labels= rm["Regional Manager"], values= rm["Sales Qty"], opacity= 0.5)])
        graph_rm_pie.update_traces (hoverinfo='label+percent', textfont_size=15,textinfo= 'label+percent', pull= [0.05, 0, 0, 0, 0],marker_line=dict(color='#FFFFFF', width=2))
        st.plotly_chart(graph_rm_pie)
        
        st.markdown("___")

        ####
        st.subheader("19- Type Shops sales for SMART PHONE")

        type_shops = smart.groupby("Shop Type", as_index= False)["Sales Qty"].sum()

        fig_dize_sept = px.bar(type_shops, x="Shop Type", y="Sales Qty", text="Sales Qty", color="Shop Type")
        fig_dize_sept.update_traces(textposition = 'outside')
        st.plotly_chart(fig_dize_sept)
        st.markdown("___")

        graph_type_sp = go.Figure(data=[go.Pie(labels= type_shops["Shop Type"], values= type_shops["Sales Qty"], title="Proportion sales by shops type for SP", opacity= 0.5)])
        graph_type_sp.update_traces (hoverinfo='label+percent', textfont_size=15,textinfo= 'label+percent', pull= [0.05, 0, 0, 0, 0],marker_line=dict(color='#FFFFFF', width=2))
        st.plotly_chart(graph_type_sp)
        st.markdown("___")
        

    with colb :
        ###
        st.subheader("2- Yearly Sales for FEATURE PHONE")
        yearly_salesFP = date_frame[date_frame["SP/FP"] == "Feature"]
        yearly_sales_fp = yearly_salesFP.groupby("Years", as_index= False)["Sales Qty"].sum()
        
        fig_years_fp = px.line(yearly_sales_fp, x="Years", y="Sales Qty", text="Sales Qty")
        fig_years_fp.update_traces(textposition = 'top center')
        st.plotly_chart(fig_years_fp)

        st.markdown("___")

        ###
        st.subheader("4- Monthly Sales for FEATURE PHONE")

        monthly_salesFP = date_frame[date_frame["SP/FP"] == "Feature"]
        monthly_sales_fp = monthly_salesFP.groupby("Month", as_index= False)["Sales Qty"].sum()

        fig_month_fp = px.line(monthly_sales_fp, x="Month", y="Sales Qty", text="Sales Qty")
        fig_month_fp.update_traces(textposition = 'top center')
        st.plotly_chart(fig_month_fp)
        
        st.markdown("___")

        ###
        st.subheader("6- Sales by regions for FEATURE PHONE")

        salesFP = date_frame[date_frame["SP/FP"] == "Feature"]
        regions_sales_fp = salesFP.groupby("Region", as_index= False)["Sales Qty"].sum()

        fig_region_fp = px.bar(regions_sales_fp, x="Region", y="Sales Qty", text="Sales Qty", color="Region")
        fig_region_fp.update_traces(textposition = 'outside')
        st.plotly_chart(fig_region_fp)
        
        st.markdown("___")

        ###
        st.subheader("8- Coverage by regions for FEATURE PHONE")

        coverFP = couverture_dr[couverture_dr["SP/FP"] == "Feature"]
        regions_cover_fp = coverFP.groupby("Region", as_index= False)["Sales Qty"].sum()

        fig_region_cover_fp = px.bar(regions_cover_fp, x="Region", y="Available Quantity", text="Available Quantity", color="Region")
        fig_region_cover_fp.update_traces(textposition = 'outside')
        st.plotly_chart(fig_region_cover_fp)
        
        st.markdown("___")

        ###
        st.subheader("10- Sales by models for FEATURE PHONE")

        feature = date_frame[date_frame["SP/FP"] == "Feature"]
        fp_region = feature["Region"].unique()
        selected_regionFP = st.selectbox("Choose your region for sales", fp_region) # On selectionne une region
        region_choose_fp = feature[feature["Region"].isin(selected_regionFP)]
        region_models_fp = (
            region_choose_fp
            .groupby(["Models"], as_index= False)["Sales Qty"].sum()
        )

        fig_huit = px.bar(region_models_fp, x="Models", y="Sales Qty", text="Sales Qty", color="Models")
        fig_huit.update_traces(textposition = 'outside')
        st.plotly_chart(fig_huit)
        
        st.markdown("___")

        ###
        st.subheader("12- Coverage by models for FEATURE PHONE")

        feature_cov_dix = couverture_dr[couverture_dr["SP/FP"] == "Feature"]
        cov_region_fp_dix = feature_cov_dix["Region"].unique()
        fp_region_cov_dix = st.selectbox("Choose your region coverage", cov_region_fp_dix) # On selectionne une region
        region_cover_fp_dix = feature_cov_dix[feature_cov_dix["Region"] == fp_region_cov_dix]
        cover_region_dix = region_cover_fp_dix.groupby("Model", as_index= False)["Available Quantity"].sum()
        
        fig_dix = px.bar(cover_region_dix, x="Models", y="Available Quantity", text="Available Quantity", color="Models")
        fig_dix.update_traces(textposition = 'outside')
        st.plotly_chart(fig_dix)

        st.markdown("___")

        ###
        st.subheader("14- Sales by market for FEATURE PHONE")
        marketFp_choose = feature[feature["Region"].isin(selected_regionFP)]
        fp_market = marketFp_choose.groupby("Market", as_index= False)["Sales Qty"].sum()

        fig_douze = px.bar(choose_market, x="Market", y="Sales Qty", text="Sales Qty", color="Market")
        fig_douze.update_traces(textposition = 'outside')
        st.plotly_chart(fig_douze)
        st.markdown("___")

        ###
        st.subheader("16- Coverage by market for FEATURE PHONE")
        market_cover_14 = feature_cov_dix[feature_cov_dix["Region"].isin(cov_region_fp_dix)]
        cover_14 = market_cover_14.groupby("Market", as_index= False)["Available Quantity"].sum()
        
        fig_14 = px.bar(cover_14, x="Market", y="Available Quantity", text="Available Quantity", color="Market")
        fig_14.update_traces(textposition = 'outside')
        st.plotly_chart(fig_14)

        st.markdown("___")
        
        ###
        st.subheader("18- Regional Manager sales for FEATURE PHONE")
        # Graphic en Pie
        rm_fp = feature.groupby("Regional Manager", as_index= False)["Sales Qty"].sum()
        graph_rmFP_pie = go.Figure(data=[go.Pie(labels= rm_fp["Regional Manager"], values= rm["Sales Qty"], opacity= 0.5)])
        graph_rmFP_pie.update_traces (hoverinfo='label+percent', textfont_size=15,textinfo= 'label+percent', pull= [0.05, 0, 0, 0, 0],marker_line=dict(color='#FFFFFF', width=2))
        st.plotly_chart(graph_rmFP_pie)
        
        st.markdown("___")


        st.subheader("20- Type Shops sales for FEATURE PHONE")

        type_shops_fp = feature.groupby("Shop Type", as_index= False)["Sales Qty"].sum()

        fig_dize_huit = px.bar(type_shops_fp, x="Shop Type", y="Sales Qty", text="Sales Qty", color="Shop Type")
        fig_dize_huit.update_traces(textposition = 'outside')
        st.plotly_chart(fig_dize_huit)

        st.markdown("___")

        graph_type_fp = go.Figure(data=[go.Pie(labels= type_shops_fp["Shop Type"], values= type_shops_fp["Sales Qty"], title="Proportion sales by shops type for FP", opacity= 0.5)])
        graph_type_fp.update_traces (hoverinfo='label+percent', textfont_size=15,textinfo= 'label+percent', pull= [0.05, 0, 0, 0, 0],marker_line=dict(color='#FFFFFF', width=2))
        st.plotly_chart(graph_type_fp)
        st.markdown("___")

    
    #########################
    ########################
    ### PROFIL RM-SR
    ################
    st.subheader("II. PROFIL", divider="rainbow")


    ######################
    ## 1- Regional Manager
    #####

    st.subheader("A- Profil Regional Manager")

    regional_select = date_frame_all["Regional Manager"].unique()

    selected_regional = st.selectbox("Choose your Regional Manager : ", regional_select)
    regional_dataset = date_frame_all[date_frame_all["Regional Manager"].isin(selected_regional)]

    ################
    ## DATA METRIC
    ######
    colc, cold, cole, colf, colg = st.columns(5)

    with colc:
        st.metric(label= "Regional Manager Name", value= selected_regional)
    with cold:
        # Nombre des shops
        rm_nbrShop = regional_dataset.groupby("Shops Name", as_index= False)["Shops Name"].count()
        st.metric(label= "Total Shops", value= rm_nbrShop)
        
    with cole:
        # Nombre des staffs
        rm_nbrStaff = regional_dataset.groupby("Supervisor Name", as_index= False)["Supervisor Name"].count()
        st.metric(label= "Total Staffs", value= rm_nbrStaff)

    with colf:
        # Target
        rm_target = regional_dataset["Target Shop"].sum()
        st.metric(label= "Target", value= rm_target)
        

    with colg :
        # Achievemen
        rm_ach = regional_dataset["Sales Qty"].sum()
        st.metric(label= "Achievemen", value= rm_ach)
    
    
    colx1, colx2 = st.columns(2)
    
    with colx1 :
        sp_dataset = regional_dataset[regional_dataset["SP/FP"] == "Smart"]
        sp = sp_dataset["Sales Qty"].sum()
        st.metric(label = "Sales of SMART PHONE", value= sp)

    with colx2 :
        fp_dataset = regional_dataset[regional_dataset["SP/FP"] == "Feature"]
        fp = fp_dataset["Sales Qty"].sum()
        st.metric(label = "Sales of FEATURE PHONE", value= fp)


    ################
    ## GRAPHIC
    ######

    a1, b2 = st.columns(2)
    with a1 :
        st.subheader("1- Yearly sales for SMART PHONE")
        regional_dataset_sp = regional_dataset[regional_dataset["SP/FP"] == "Smart"]
        rm_yearly = regional_dataset_sp.groupby("Years", as_index= False)["Sales Qty"].sum()
        
        fig_rm_years_sp = px.line(rm_yearly, x="Years", y="Sales Qty", text= "Sales Qty")
        fig_rm_years_sp.update_traces(textposition= 'top center')
        st.plotly_chart(fig_rm_years_sp)
        st.markdown("___")

        st.subheader("3- Monthly sales for SMART PHONE")
        rm_month = regional_dataset_sp.groupby("Month", as_index= False)["Sales Qty"].sum()
        
        fig_rm_month_sp = px.line(rm_month, x="Month", y="Sales Qty", text= "Sales Qty")
        fig_rm_month_sp.update_traces(textposition= 'top center')
        st.plotly_chart(fig_rm_month_sp)
        st.markdown("___")

        st.subheader("5- Sales by models for SMART PHONE")
        rm_model_sp = regional_dataset_sp.groupby("Models", as_index= False)["Sales Qty"].sum()
        
        fig_model_sp = px.bar(rm_model_sp, x="Models", y="Sales Qty", text= "Sales Qty", color= "Models")
        fig_model_sp.update_traces(textposition= 'outside')
        st.plotly_chart(fig_model_sp)
        st.markdown("___")

        st.subheader("7- Sales by Market for SMART PHONE")
        rm_market_sp = regional_dataset_sp.groupby("Market", as_index= False)["Sales Qty"].sum()
        
        fig_market_sp = px.bar(rm_market_sp, x="Market", y="Sales Qty", text= "Sales Qty", color= "Market")
        fig_market_sp.update_traces(textposition= 'outside')
        st.plotly_chart(fig_market_sp)
        st.markdown("___")

        st.subheader("9- Sales by Shops for SMART PHONE")
        rm_shops_sp = regional_dataset_sp.groupby("Shops Name", as_index= False)["Sales Qty"].sum()
        
        fig_shops_sp = px.bar(rm_shops_sp, x="Shops Name", y="Sales Qty", text= "Sales Qty", color= "Shops Name")
        fig_shops_sp.update_traces(textposition= 'outside')
        st.plotly_chart(fig_shops_sp)
        st.markdown("___")

        st.subheader("11- Sales by Staffs for SMART PHONE")
        rm_staffs_sp = regional_dataset_sp.groupby("Supervisor Name", as_index= False)["Sales Qty"].sum()
        
        fig_staffs_sp = px.bar(rm_staffs_sp, x="Supervisor Name", y="Sales Qty", text= "Sales Qty", color= "Supervisor Name")
        fig_staffs_sp.update_traces(textposition= 'outside')
        st.plotly_chart(fig_staffs_sp)
        st.markdown("___")

    with b2 :
        st.subheader("2- Yearly sales for FEATURE PHONE")
        regional_dataset_fp = regional_dataset[regional_dataset["SP/FP"] == "Feature"]
        rm_yearly_fp = regional_dataset_fp.groupby("Years", as_index= False)["Sales Qty"].sum()
        
        fig_rm_years_fp = px.line(rm_yearly_fp, x="Years", y="Sales Qty", text= "Sales Qty")
        fig_rm_years_fp.update_traces(textposition= 'top center')
        st.plotly_chart(fig_rm_years_sp)
        st.markdown("___")

        st.subheader("4- Monthly sales for FEATURE PHONE")
        rm_month_fp = regional_dataset_fp.groupby("Month", as_index= False)["Sales Qty"].sum()
        
        fig_rm_month_fp = px.line(rm_month_fp, x="Month", y="Sales Qty", text= "Sales Qty")
        fig_rm_month_fp.update_traces(textposition= 'top center')
        st.plotly_chart(fig_rm_month_fp)
        st.markdown("___")

        st.subheader("6- Sales by models for FEATURE PHONE")
        rm_model_fp = regional_dataset_fp.groupby("Models", as_index= False)["Sales Qty"].sum()
        
        fig_model_fp = px.bar(rm_model_fp, x="Models", y="Sales Qty", text= "Sales Qty", color= "Models")
        fig_model_fp.update_traces(textposition= 'outside')
        st.plotly_chart(fig_model_fp)
        st.markdown("___")

        st.subheader("8- Sales by Markets for FEATURE PHONE")
        rm_market_fp = regional_dataset_fp.groupby("Market", as_index= False)["Sales Qty"].sum()
        
        fig_market_fp = px.bar(rm_market_fp, x="Market", y="Sales Qty", text= "Sales Qty", color= "Market")
        fig_market_fp.update_traces(textposition= 'outside')
        st.plotly_chart(fig_market_fp)
        st.markdown("___")

        st.subheader("10- Sales by Shops for FEATURE PHONE")
        rm_shops_fp = regional_dataset_fp.groupby("Shops Name", as_index= False)["Sales Qty"].sum()
        
        fig_shops_fp = px.bar(rm_shops_fp, x="Shops Name", y="Sales Qty", text= "Sales Qty", color= "Shops Name")
        fig_shops_fp.update_traces(textposition= 'outside')
        st.plotly_chart(fig_shops_fp)
        st.markdown("___")

        st.subheader("12- Sales by Staffs for FEATURE PHONE")
        rm_staffs_fp = regional_dataset_fp.groupby("Supervisor Name", as_index= False)["Sales Qty"].sum()
        
        fig_staffs_fp = px.bar(rm_staffs_fp, x="Supervisor Name", y="Sales Qty", text= "Sales Qty", color= "Supervisor Name")
        fig_staffs_fp.update_traces(textposition= 'outside')
        st.plotly_chart(fig_staffs_fp)
        st.markdown("___")


    st.markdown("___")

    
    ##############################################
    ## 2- Supervisor, Promoter and Tempory Promoter
    #####
    st.subheader("B- Profil Suppervisors & Promotors")

    supervisor_select = date_frame_all["Supervisor Name"].unique()
    supervisor_selected = st.selectbox("Choose your Supervisor/Promoter and Tempory promoter name : ", supervisor_select)
    supervisor_dataset = date_frame_all[date_frame_all["Supervisor Name"].isin(supervisor_selected)]

    ################
    ## DATA METRIC
    ######
    colg, colh, coli, colj = st.columns(4)

    with colg:
        # Name
        st.metric(label="Staff Name", value= supervisor_selected)
        
    with colh:
        # Nombre des shops
        sr_nbrShop = supervisor_dataset.groupby("Shops Name", as_index= False)["Shops Name"].count()
        st.metric(label="Total Shops", value= sr_nbrShop)
        
    with coli:
        # Target
        sr_target = supervisor_dataset["Target Shop"].sum()
        st.metric(label="Target", value= sr_target)

    with colj:
        # Vente
        sr_ach = supervisor_dataset["Target Shop"].sum()
        st.metric(label="Achie", value= sr_ach)

    
    coly1, coly2 = st.columns(2)
    
    with coly1 :
        sp_dataset_sr = supervisor_dataset[supervisor_dataset["SP/FP"] == "Smart"]
        sp_sr = sp_dataset_sr["Sales Qty"].sum()
        st.metric(label = "Sales of SMART PHONE", value= sp_sr)

    with coly2 :
        fp_dataset_sr = supervisor_dataset[supervisor_dataset["SP/FP"] == "Feature"]
        fp_sr = fp_dataset_sr["Sales Qty"].sum()
        st.metric(label = "Sales of FEATURE PHONE", value= fp_sr)
        


    ################
    ## GRAPHIC
    ######
    c, d = st.columns(2)
    with c :
        st.subheader("1- Yearly sales for SMART PHONE")

        sr_years = sp_dataset_sr.groupby("Years", as_index= False)["Sales Qty"].sum()
        fig_years_sr_sp = px.line(sr_years, x="Years", y="Sales Qty", text= "Sales Qty")
        fig_years_sr_sp.update_traces(textposition = 'top center')
        st.plotly_chart(fig_years_sr_sp)
        st.markdown("___")

        st.subheader("3- Monthly sales for SMART PHONE")

        sr_month = sp_dataset_sr.groupby("Month", as_index= False)["Sales Qty"].sum()
        fig_month_sr_sp = px.line(sr_month, x="Month", y="Sales Qty", text= "Sales Qty")
        fig_month_sr_sp.update_traces(textposition = 'top center')
        st.plotly_chart(fig_month_sr_sp)
        st.markdown("___")

        st.subheader("5- Sales by models for SMART PHONE")

        sr_models = sp_dataset_sr.groupby("Models", as_index= False)["Sales Qty"].sum()
        fig_models_sr_sp = px.bar(sr_models, x="Models", y="Sales Qty", text= "Sales Qty", color="Models")
        fig_models_sr_sp.update_traces(textposition = 'outside')
        st.plotly_chart(fig_models_sr_sp)
        st.markdown("___")

        st.subheader("7- Sales by Markets for SMART PHONE")

        sr_market = sp_dataset_sr.groupby("Market", as_index= False)["Sales Qty"].sum()
        fig_market_sr_sp = px.bar(sr_market, x="Market", y="Sales Qty", text= "Sales Qty", color="Market")
        fig_market_sr_sp.update_traces(textposition = 'outside')
        st.plotly_chart(fig_market_sr_sp)
        st.markdown("___")

        st.subheader("9- Sales by shops for SMART PHONE")

        sr_shops = sp_dataset_sr.groupby("Shops Name", as_index= False)["Sales Qty"].sum()
        fig_shops_sr_sp = px.bar(sr_shops, x="Shops Name", y="Sales Qty", text= "Sales Qty", color="Shops Name")
        fig_shops_sr_sp.update_traces(textposition = 'outside')
        st.plotly_chart(fig_shops_sr_sp)
        st.markdown("___")

        st.subheader("11- Coverage models by shops for SMART PHONE")
        
        select_model = sp_dataset_sr["Models"].unique()
        select_multi = st.multiselect("Choose your differents models", select_model)

        shops_choisi_sp = sp_dataset_sr[sp_dataset_sr["Models"].isin(select_multi)]

        sr_shops_cover_sp = shops_choisi_sp.groupby("Shops Name", as_index= False)["Coverage"].sum()
        fig_shops_models_sp = px.bar(sr_shops_cover_sp, x="Shops Name", y="Coverage", text= "Coverage", color="Shops Name")
        fig_shops_models_sp.update_traces(textposition = 'outside')
        st.plotly_chart(fig_shops_models_sp)
        st.markdown("___")

    with d :
        st.subheader("2- Yearly sales for FEATURE PHONE")

        sr_years_fp = fp_dataset_sr.groupby("Years", as_index= False)["Sales Qty"].sum()
        fig_years_sr_fp = px.line(sr_years_fp, x="Years", y="Sales Qty", text= "Sales Qty")
        fig_years_sr_fp.update_traces(textposition = 'top center')
        st.plotly_chart(fig_years_sr_fp)
        st.markdown("___")

        st.subheader("4- Monthly sales for FEATURE PHONE")

        sr_month_fp = fp_dataset_sr.groupby("Month", as_index= False)["Sales Qty"].sum()
        fig_month_sr_fp = px.line(sr_month_fp, x="Month", y="Sales Qty", text= "Sales Qty")
        fig_month_sr_fp.update_traces(textposition = 'top center')
        st.plotly_chart(fig_month_sr_fp)
        st.markdown("___")

        st.subheader("6- Sales by models for FEATURE PHONE")

        sr_models_fp = fp_dataset_sr.groupby("Models", as_index= False)["Sales Qty"].sum()
        fig_models_sr_fp = px.bar(sr_models_fp, x="Models", y="Sales Qty", text= "Sales Qty", color="Models")
        fig_models_sr_fp.update_traces(textposition = 'outside')
        st.plotly_chart(fig_models_sr_fp)
        st.markdown("___")

        st.subheader("8- Sales by Market for FEATURE PHONE")

        sr_markets_fp = fp_dataset_sr.groupby("Market", as_index= False)["Sales Qty"].sum()
        fig_markets_sr_fp = px.bar(sr_markets_fp, x="Market", y="Sales Qty", text= "Sales Qty", color="Market")
        fig_markets_sr_fp.update_traces(textposition = 'outside')
        st.plotly_chart(fig_markets_sr_fp)
        st.markdown("___")

        st.subheader("10- Sales by shops for FEATURE PHONE")

        sr_shops_fp = fp_dataset_sr.groupby("Shops Name", as_index= False)["Sales Qty"].sum()
        fig_shops_sr_fp = px.bar(sr_shops_fp, x="Shops Name", y="Sales Qty", text= "Sales Qty", color="Shops Name")
        fig_shops_sr_fp.update_traces(textposition = 'outside')
        st.plotly_chart(fig_shops_sr_fp)
        st.markdown("___")

        st.subheader("11- Coverage models by shops for SMART PHONE")
        
        select_model_fp = fp_dataset_sr["Models"].unique()
        select_multi_fp = st.multiselect("Choose your differents models FP :", select_model_fp)

        shops_choisi_fp = fp_dataset_sr[fp_dataset_sr["Models"].isin(select_multi)]

        sr_shops_cover_fp = shops_choisi_fp.groupby("Shops Name", as_index= False)["Coverage"].sum()
        fig_shops_models_fp = px.bar(sr_shops_cover_fp, x="Shops Name", y="Coverage", text= "Coverage", color="Shops Name")
        fig_shops_models_fp.update_traces(textposition = 'outside')
        st.plotly_chart(fig_shops_models_fp)
        st.markdown("___")
    

    st.markdown("___")


    ##############################################
    ## 3- Shops
    #####
    st.subheader("C- Profil Shops")

    shops_select = date_frame["Shops Name"].unique()
    shops_selected = st.selectbox("Choose your ShopsN ame : ", shops_select)
    shops_dataset = date_frame[date_frame["Shops Name"].isin(shops_selected)]

    ################
    ## DATA METRIC
    ######
    colj1, colj2, colj3, colj4, colj5 = st.columns(5)

    with colj1:
        # Name
        st.metric(label="Shop Name", value= shops_selected)
        
    with colj2:
        # Regional Name
        rm_sr = shops_dataset["Regional Manager"]
        st.metric(label="RM name/Responsible", value= rm_sr)
        

    with colj3:
        # Superviseur Name
        fsm_pr = shops_dataset["Supervisor Name"]
        st.metric(label="Manage by", value= fsm_pr)

    with colj4:
        # Target
        shop_target = shops_dataset["Target Shop"].sum()
        st.metric(label="Target", value= shop_target)
        
    with colj5:
        # Vente
        shop_ach = shops_dataset["Target Shop"].sum()
        st.metric(label="Achie", value= shop_ach)
        
        

    coly3, coly4 = st.columns(2)
    
    with coly3 :
        sp_dataset_shops = shops_dataset[shops_dataset["SP/FP"] == "Smart"]
        sp_shops = sp_dataset_shops["Sales Qty"].sum()
        st.metric(label = "Sales of SMART PHONE", value= sp_shops)

    with coly4 :
        fp_dataset_shops = shops_dataset[shops_dataset["SP/FP"] == "Feature"]
        fp_shops = fp_dataset_shops["Sales Qty"].sum()
        st.metric(label = "Sales of FEATURE PHONE", value= fp_shops)
        


    ################
    ## GRAPHIC
    ######
    c1, d1 = st.columns(2)
    with c1 :
        st.subheader("1- Yearly sales for SMART PHONE")

        shops_years_sp = sp_dataset_shops.groupby("Years", as_index= False)["Sales Qty"].sum()
        fig_shops_years_sp = px.line(shops_years_sp,  x="Years", y="Sales Qty", text="Sales Qty")
        fig_shops_years_sp.update_traces(textposition= 'top center')
        st.plotly_chart(fig_shops_years_sp)
        st.markdown("___")

        st.subheader("3- Monthly sales for SMART PHONE")

        shops_month_sp = sp_dataset_shops.groupby("Month", as_index= False)["Sales Qty"].sum()
        fig_shops_month_sp = px.line(shops_month_sp,  x="Month", y="Sales Qty", text="Sales Qty")
        fig_shops_month_sp.update_traces(textposition= 'top center')
        st.plotly_chart(fig_shops_month_sp)
        st.markdown("___")

        st.subheader("5- Sales by models for SMART PHONE")

        shops_models_sp = sp_dataset_shops.groupby("Models", as_index= False)["Sales Qty"].sum()
        fig_shops_models_sp = px.bar(shops_models_sp,  x="Models", y="Sales Qty", text="Sales Qty", color= "Models")
        fig_shops_models_sp.update_traces(textposition= 'outside')
        st.plotly_chart(fig_shops_models_sp)
        st.markdown("___")

    with d1 :
        st.subheader("2- Yearly sales for FEATURE PHONE")
        
        shops_years_fp = fp_dataset_shops.groupby("Years", as_index= False)["Sales Qty"].sum()
        fig_shop_years_fp = px.line(shops_years_fp, x="Years", y="Sales Qty", text="Sales Qty")
        fig_shop_years_fp.update_traces(textposition= 'top center')
        st.plotly_chart(fig_shop_years_fp)
        st.markdown("___")

        st.subheader("4- Monthly sales for FEATURE PHONE")

        shops_month_fp = fp_dataset_shops.groupby("Month", as_index= False)["Sales Qty"].sum()
        fig_shop_month_fp = px.line(shops_month_fp, x="Month", y="Sales Qty", text="Sales Qty")
        fig_shop_month_fp.update_traces(textposition= 'top center')
        st.plotly_chart(fig_shop_month_fp)
        st.markdown("___")

        st.subheader("6- Sales by models for FEATURE PHONE")

        shops_models_fp = fp_dataset_shops.groupby("Models", as_index= False)["Sales Qty"].sum()
        fig_shop_models_fp = px.bar(shops_models_fp, x="Models", y="Sales Qty", text="Sales Qty", color= "Models")
        fig_shop_models_fp.update_traces(textposition= 'outside')
        st.plotly_chart(fig_shop_models_fp)
        st.markdown("___")
    

    st.markdown("___")


    #############################
    ### FIN
    #########################
    st.title("THANKS FOR YOUR ATTENTION !")

         

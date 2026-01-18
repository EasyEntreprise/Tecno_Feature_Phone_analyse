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


st.markdown("<h1 style='text-align: center; color: blue;'> TECNO SO DASHBOARD </h1>", unsafe_allow_html= True)
st.markdown("<br/>", unsafe_allow_html= True)
st.markdown("<br/>", unsafe_allow_html= True)
st.markdown("<h6 style='text-align: center; color: red;'> Welcome in our Sales Out dashboard for Tecno brand DRC. This dashboard is important for following the ST purchase of customers."
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



# Load dataset
sale = st.file_uploader("📂 Insert your Excel Sale file by pressing the 'Browse files' button", type=["xlsx","xls", "csv"])
coverage = st.file_uploader("Insert your Excel Inventory file by pressing the 'Browse files' button", type=["xlsx", "xls", "csv"])

if sale is not None:

    achat_1 = pd.read_excel(sale, sheet_name="Shop Sales Query New1")
    achat = achat_1.dropna(subset="Sales Qty") # On supprime les lignes qui n'ont pas de vente ou de quantite de vente

    couverture_1 = pd.read_excel(coverage, sheet_name="Shop Inventory Query")
    couverture = couverture_1.dropna(subset="Available Quantity") # On supprime les lignes qui n'ont pas de quantite disponible

    #######################################
    ###### Traitement du fichier ##########
    # ##################################### 
            
    # Suppression des colonnes des dataframe
    cols_to_drop = ["Shop Alias", "Status", "Shop Brand", "Public ID", "Shop Type", "Manpower Type", "Shop Grade", "Image Type", "Product Category", "Brand", "Series", "Model Type", "Item", "Market Name", "Item(Market Name)", "Material ID", "Product", "IMEI/SN", "IMEI/SN List", "Booking Activity ID", "Suggested RP", "Unit Price", "Activation City", "7 Days Active", "15 Days Active", "E Warranty Date", "Upload On Other System", "Time Difference", "Achieve or Not", "Reason", "Coupon No", "Achieve Rule", "Free Gift No", "Consumer Phone", "Consumer Name", "Consumer Mail", "Attachments", "Incentive Status", "Incentive Date",	"Country",	"City Tier", "Sales Region 1",	"Sales Region 3",	"Sales Region 4",	"Sales Region 5",	"Business Area",	"Uploader ID", "Uploader", "Upload Date",	"Upload Time",	"Position",	"Upload Type",	"Created By",	"Updater",	"Update Name",	"Updated Time",	"Supervisor Name", "Supervisor ID",	"Area Sales Manager Name",	"Area Sales Manager ID", "Branch Sales Manager Name",	"Branch Sales Manager ID",	"Region Sales Manager Name", "Region Sales Manager ID",	"Remark", "Record ID", "Carlcare Shop Code", "POS ID",	"Consumer Gender",	"Consumer Age",	"Distributor ID",	"Distributor Name",	"Belong MD ID",	"Belong MD Name",	"Customer Price", "Retailer Price",	"MOP",	"Source Type",	"Staff Achieve or Not",	"IMEI Picture",	"Reason of User",	"AI Detection Status",	"Manual Detection Status",	"Fake Status",	"Retailer ID",	"Retailer Name"]
    
    # Ne garder que les colonnes qui existent réellement :
    cols_to_drop = [c for c in cols_to_drop if c in achat.columns]

    achat_drop = achat.drop(cols_to_drop, axis=1)
    
    # Suppresionn des colonnes de l'achat
    cols_to_drop_inv = ["Brand", "Series",	"First Category", "Item", "Market Name", "Color", "Memory",	"Manpower Type", "Retailer ID",	"Retailer Name", "Public ID", "Shop Type",	"Shop Grade",	"Image Type", "Sales Region 1",	"Sales Region 4", "Sales Region 5", "Remark"] # Suppresion des colonnes de la couverture
    
    # Ne garder que les colonnes qui existent réellement pour la couverture :
    cols_to_drop_inv = [inv for inv in cols_to_drop_inv if inv in couverture.columns]
    couverture_drop = couverture.drop(cols_to_drop_inv, axis=1)

    # Renommer une colonne
    achat_dr = achat_drop.rename(columns={"Sales Region 2":"Sales Region", "State":"Region", "City":"Market"}) # Renomer la colonne 'Sales Region' 
    couverture_dr = couverture_drop.rename(columns={"Sales Region 2":"Sales Region", "State":"Region", "City":"Market"}) # Renomer la colonne 'Sales Region'
    
    # Convertir en datetime
    achat_dr["Sales Date"] = pd.to_datetime(achat_dr["Sales Date"], errors="coerce") # Mettre la colonne 'Sales Date' en format date
    
    # Extraire mois + année
    achat_dr["Month"] = achat_dr["Sales Date"].dt.strftime("%Y-%m")
    

    # Renommer les elements des colonnes
    #achat_dr["Region"] = np.where(achat_dr["Region"] == "State", "Kinshasa", achat_dr["Region"])
    achat_dr["Region"] = np.where(achat_dr["Region"] == "Haut- Katanga", "Big Katanga", achat_dr["Region"])
    achat_dr["Region"] = np.where(achat_dr["Region"] == "Lualaba", "Big Katanga", achat_dr["Region"])
    achat_dr["SP/FP"]  = np.where(achat_dr["SP/FP"] == "PAD", "Smart", achat_dr["SP/FP"])
    achat_dr["SP/FP"]  = np.where(achat_dr["SP/FP"] == "Pad", "Smart", achat_dr["SP/FP"])
    achat_dr["SP/FP"] = achat_dr["SP/FP"].fillna("Accessories")



    #couverture_dr["Region"] = np.where(couverture_dr["Region"] == "State", "Kinshasa", couverture_dr["Region"])
    couverture_dr["Region"] = np.where(couverture_dr["Region"] == "Haut- Katanga", "Big Katanga", couverture_dr["Region"])
    couverture_dr["Region"] = np.where(couverture_dr["Region"] == "Lualaba", "Big Katanga", couverture_dr["Region"])
    couverture_dr["Region"] = np.where(couverture_dr["Region"] == "Kasai", "Big Kasai", couverture_dr["Region"])
    couverture_dr["Region"] = np.where(couverture_dr["Region"] == "Kasai Centrale", "Big Kasai", couverture_dr["Region"])
    couverture_dr["Region"] = np.where(couverture_dr["Region"] == "Kasai Orientale", "Big Kasai", couverture_dr["Region"])
    couverture_dr["Region"] = np.where(couverture_dr["Region"] == "Kwilu", "Big Equateur", couverture_dr["Region"])
    couverture_dr["Region"] = np.where(couverture_dr["Region"] == "Sud-Ubangi", "Big Equateur", couverture_dr["Region"])
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
    
    
    # Choisir entre Smart Phone, Feature Phone ou Accessories Tecno
    st.markdown("___")
    category = ["Smart", "Feature", "Accessories"]
    select_categories = st.selectbox("Chose your category between :", category)
    st.markdown("___")

    # Filtre dates
    date_frame = achat_dr[(achat_dr["Sales Date"]>=str(start_date)) & (achat_dr["Sales Date"]<=str(en_date))]
    date_frame = date_frame[date_frame["SP/FP"] == select_categories]

    couverture_dr = couverture_dr[couverture_dr["SP/FP"] == select_categories]

    with st.expander("Filter dates"):
        filter_date = dataframe_explorer(date_frame, case=False)
        st.dataframe(filter_date, use_container_width= True)



    #####################################################################################
    ###### AFFICHAGE RESULTAT ###########################################################
    #####################################################################################

    ##############################
    ####### DATA METRIC ##########
    ##############################

    st.subheader("DATA METRIC", divider="rainbow")
    col3, col4, col5, col6 = st.columns(4, gap= "small")
    col7, col8, col9, col0, col01 = st.columns(5, gap="small")

    with col3:
        shop_sales = date_frame["Shop Name"].nunique()
        st.metric(label="TOTAL SHOPS WITH SALES", value= f"{shop_sales} PCS") # Les nombres total des shops avec vente

    with col4:
        shop_cover = couverture_dr["Shop Name"].nunique()
        st.metric(label="TOTAL SHOPS WITH COVERAGE", value= shop_cover) # Le nombre des shops total avec couverture  

    with col5:
        total_vente = date_frame["Sales Qty"].sum()
        st.metric(label="TOTAL SALES", value= total_vente) # Total vente en general
        
    with col6:
        total_cover = couverture_dr["Available Quantity"].sum()
        st.metric(label="TOTAL COVERAGE", value= total_cover) # La couverture total

    Region = date_frame.groupby(["Region"], as_index= False)["Sales Qty"].sum()
    Region_cover = couverture_dr.groupby(["Region"], as_index= False)["Available Quantity"].sum()
    
    
    with col7:
        kinshasa_sales = Region[Region["Region"] == "Kinshasa"] 
        kinshasa_cover = Region_cover[Region_cover["Region"] == "Kinshasa"]
        
        kinshasa_sales["Sales Qty"] = kinshasa_sales["Sales Qty"].fillna(0).astype(int) # Conversion de la colonne "Sales Qty" en entier
        kinshasa_cover["Available Quantity"] = kinshasa_cover["Available Quantity"].fillna(0).astype(int)

        if not kinshasa_sales.empty or (not kinshasa_cover.empty) :
            st.metric(label="KINSHASA Sales", value= int(kinshasa_sales["Sales Qty"].fillna(0).sum()), delta= f"Coverage Kinshasa : {int(kinshasa_cover['Available Quantity'].fillna(0).sum())}") # La Situation de la vente de la region Kinshasa avec situation couverture comme delta
        else:
            st.metric(label="KINSHASA Sales", value= 0, delta= "Coverage Kinshasa : 0") 


    with col8:
        katanga_sales = Region[Region["Region"] == "Big Katanga"]
        katanga_cover = Region_cover[Region_cover["Region"] == "Big Katanga"] 

        katanga_sales["Sales Qty"] = katanga_sales["Sales Qty"].fillna(0).astype(int) # Conversion de la colonne "Sales Qty" en entier tout en remplaçant les valeurs manquantes par 0
        katanga_cover["Available Quantity"] = katanga_cover["Available Quantity"].fillna(0).astype(int)

        if not katanga_sales.empty or (not katanga_sales.empty):
            st.metric(label="BIG KATANGA Sales", value= int(katanga_sales["Sales Qty"].fillna(0).sum()), delta= f"Coverage Katanga : {int(katanga_cover["Available Quantity"].fillna(0).sum())}") # La Situation de la vente de la region Big Katanga avec situation couverture comme delta

        else :
            st.metric(label="BIG KATANGA Sales", value= 0, delta= "Coverage Katanga : 0")
        

    with col9:
        kongoc_sales = Region[Region["Region"] == "Kongo Centrale"] 
        kongoc_cover = Region_cover[Region_cover["Region"] == "Kongo Centrale"] 

        kongoc_sales["Sales Qty"] = kongoc_sales["Sales Qty"].fillna(0).astype(int) # Conversion de la colonne "Sales Qty" en entier tout en remplaçant les valeurs manquantes par 0
        kongoc_cover["Available Quantity"] = kongoc_cover["Available Quantity"].fillna(0).astype(int)

        if not kongoc_sales.empty or (not kongoc_cover.empty) :
            st.metric(label="CENTRAL KONGO's Sales ", value= int(kongoc_sales["Sales Qty"].fillna(0).sum()), delta= f"Coverage Kongo Central : {int(kongoc_cover["Available Quantity"].fillna(0).sum())}") # La Situation de la vente de la region Kongo Central avec situation couverture comme delta

        else :
            st.metric(label="CENTRAL KONGO Sales ", value= 0, delta= "Coverage Central Kongo : 0")
        

    with col0:
        kasai_sales = Region[Region["Region"] == "Big Kasai"] 
        kasai_cover = Region_cover[Region_cover["Region"] == "Big Kasai"] 

        kasai_sales["Sales Qty"] = kasai_sales["Sales Qty"].fillna(0).astype(int) # Conversion de la colonne "Sales Qty" en entier tout en remplaçant les valeurs manquantes par 0
        kasai_cover["Available Quantity"] = kasai_cover["Available Quantity"].fillna(0).astype(int)


        if not kasai_sales.empty or (not kasai_cover.empty) :
            st.metric(label="BIG KASAI Sales", value= int(kasai_sales["Sales Qty"].fillna(0).sum()), delta= f"Coverage Big Kasai : {int(kasai_cover['Available Quantity'].fillna(0).sum())}") # La Situation de la vente de la region Big Kasai avec situation couverture comme delta

        else :
            st.metric(label="BIG KASAI Sales", value= 0, delta= "Coverage BIG KASAI : 0")

        

    with col01:
        equator_sales = Region[Region["Region"] == "Big Equateur"] 
        equator_cover = Region_cover[Region_cover["Region"] == "Big Equateur"] 

        equator_sales["Sales Qty"] = equator_sales["Sales Qty"].fillna(0).astype(int) # Conversion de la colonne "Sales Qty" en entier tout en remplaçant les valeurs manquantes par 0
        equator_cover["Available Quantity"] = equator_cover["Available Quantity"].fillna(0).astype(int)

        if not equator_sales.empty or (not equator_cover.empty) :
            st.metric(label="BIG EQUATOR Sales", value= int(equator_sales["Sales Qty"].fillna(0).sum()), delta= f"Coverage Big Equator : {int(equator_cover["Available Quantity"].fillna(0).sum())}") # La Situation de la vente de la region Big Equa avec situation couverture comme delta

        else :
            st.metric(label="BIG EQUATOR Sales", value= 0, delta= "Coverage BIG EQUATOR : 0")
        

    # Style the metric
    style_metric_cards(background_color="#3c4d66", border_left_color="#99f2c8", border_color="#0006a")

    zcol1, zcol2 = st.columns(2, gap="small")

    with zcol1 :

        nbr_shop_region = (date_frame.groupby("Region")["Shop Name"].unique().reset_index()) # On recupere les shops avec vente par region
        nbr_shop_region["count"] = nbr_shop_region["Shop Name"].apply(len) # On creer une colonne qui aura le nombre des shops par regions

        fig_nbr_shop_region = px.line(nbr_shop_region, x="Region", y="count", text= "count", title="Number of shop with sales by regions")
        fig_nbr_shop_region.update_traces(textposition = 'top center')
        st.plotly_chart(fig_nbr_shop_region)
    
    with zcol2 :
        nbr_cover_region = (couverture_dr.groupby("Region")["Shop Name"].unique().reset_index()) # On recupere les shops avec couverture par region
        nbr_cover_region["count"] = nbr_cover_region["Shop Name"].apply(len) # On creer une colonne qui aura le nombre des shops par regions

        fig_cover_shop_region = px.line(nbr_cover_region, x="Region", y="count", text= "count", title="Quantity of shop with coverage by regions")
        fig_cover_shop_region.update_traces(textposition = 'top center')
        st.plotly_chart(fig_cover_shop_region)


            
    ##########################################
    ### VENTE MENSUELLE ET SEMESTRIELLE ######
    ##########################################
            
    st.subheader("MONTHLY SALES", divider="gray")

    # Graph 2 : Situation de la vente mensuelle
    # Graphique en line avec comme argument (Month et Sale Qty)
    monthly_sale = date_frame.groupby("Month", as_index= False)["Sales Qty"].sum()
    
    fig_monthly_sale = px.line(monthly_sale, x="Month", y="Sales Qty", text= "Sales Qty", title= "Monthly retail sales")
    fig_monthly_sale.update_traces(textposition = 'top center')
    st.plotly_chart(fig_monthly_sale)

    # Monthly by Regions and City
    st.markdown("___")
    a, b = st.columns(2)

    with a :
        monthly_region = date_frame.groupby(["Region", "Month"], as_index= False)["Sales Qty"].sum()
        
        fig_month_region = px.bar(monthly_region, x="Region", y="Sales Qty", text="Sales Qty", title= "Monthly sales by regions", color="Region")
        fig_month_region.update_traces(textposition = 'outside')
        st.plotly_chart(fig_month_region)

        # Pie Chart
        fig_month_region_pie = go.Figure(data=[go.Pie(labels= monthly_region["Region"], values= monthly_region["Sales Qty"], opacity= 0.5)])
        fig_month_region_pie.update_traces (hoverinfo='label+percent', textfont_size=15,textinfo= 'label+percent', pull= [0.05, 0, 0, 0, 0],marker_line=dict(color='#FFFFFF', width=2))
        st.plotly_chart(fig_month_region_pie)

    with b :
        regions = sorted(date_frame["Region"].unique())
        selected_region = st.selectbox("Choose one region for seeing monthly sales by market", options=["--Toutes--"] + regions) # Selectionner la region

        # Filtrer
        if selected_region == "--Toutes--":
            df_region = date_frame.copy()
        else:
            df_region = date_frame[date_frame["Region"] == selected_region].copy()

        if df_region.empty:
            st.warning("Aucune donnée pour la région sélectionnée.")
            st.stop()

        # --- AGRÉGATION : somme des ventes par Month et Market ---
        grouped = (
            df_region.groupby(["Month", "Market"], dropna=False)["Sales Qty"].sum().reset_index().sort_values("Month")
        )

        fig_region = px.bar(grouped, x="Market", y="Sales Qty", text="Sales Qty", title= "Monthly sales by market", color="Market")
        fig_region.update_traces(textposition = 'outside')
        st.plotly_chart(fig_region)

        # Pie Chart
        fig_region_pie = go.Figure(data=[go.Pie(labels= grouped["Market"], values= grouped["Sales Qty"], opacity= 0.5)])
        fig_region_pie.update_traces (hoverinfo='label+percent', textfont_size=15,textinfo= 'label+percent', pull= [0.05, 0, 0, 0, 0],marker_line=dict(color='#FFFFFF', width=2))
        st.plotly_chart(fig_region_pie)
            

    #######################################
    ### VENTE & COVERAGE PAR MODELES ######
    #######################################
            
    st.subheader("SALES AND COVERAGE BY MODELS", divider="gray")

    colc, cold = st.columns(2, gap="small")

    with colc :
        ######
        # Graph 4 : Situation de la vente par modeles (models, qty) [Graphic en Bar]
        models = date_frame.groupby("Model", as_index= False)["Sales Qty"].sum()

        fig_model_sales = px.bar(models, x="Model", y="Sales Qty", color="Model", text="Sales Qty", title="sales by Models")
        fig_model_sales.update_traces(textposition = 'outside')
        st.plotly_chart(fig_model_sales)

        st.markdown("___")
        ####
        # Graph 5 : Situation de la vente par modeles en fonction du mois (month, qty) [Graphic en Line]. Avoir la possibilite de choisir les models en multi choix
        # Creation d'une liste des models uniques
        models_data = date_frame["Model"].unique()

        # Creation d'un selecteur multiple
        selected_models = st.multiselect("Selecte your models", models_data)

        # Filtrage des donnees en fonction de la selection
        date_groupby = date_frame.groupby(["Month","Model"], as_index= False)["Sales Qty"].sum()
        df_filtered = date_groupby[date_groupby["Model"].isin(selected_models)]
        
        fig_area = px.bar(df_filtered, x="Month", y="Sales Qty", text="Sales Qty", title="Models sale by month", color="Model", barmode="group")
        fig_area.update_traces(textposition = 'outside')
        st.plotly_chart(fig_area)
        
        st.markdown("___")
        # Graph 6 : Meme chose mais en graphic Pie
        #liste = date_frame["Model"].unique()
        fig_pie = go.Figure(data=[go.Pie(labels= models["Model"], values= models["Sales Qty"], title="Proportion sales by Models", opacity= 0.5)])
        fig_pie.update_traces (hoverinfo='label+percent', textfont_size=15,textinfo= 'label+percent', pull= [0.05, 0, 0, 0, 0],marker_line=dict(color='#FFFFFF', width=2))
        st.plotly_chart(fig_pie)
        

    with cold :
        # Graph 7 : Situation de la couverture par modeles (models, qty)[Graphic en Bar]
        covert = couverture_dr.groupby("Model", as_index= False)["Available Quantity"].sum()

        fig_models_covert = px.bar(covert, x="Model", y="Available Quantity", color="Model", text="Available Quantity", title="Coverage by Models")
        fig_models_covert.update_traces(textposition = 'outside')
        st.plotly_chart(fig_models_covert) 
        #st.write(covert)
        st.markdown("___")

        # Graph 8 : Graphique en 'Bar', selectionant le modele pour connaitre le notre des shops ayant sa couverture par regions
        models_covert = couverture_dr["Model"].unique()
        select_model = st.selectbox("Choose one model for seeing his coverage", models_covert) # Selectionner le shop

        choix = couverture_dr[couverture_dr["Model"] == select_model]
        cover_region = (choix.groupby("Region")["Shop Name"].unique().reset_index()) 
        cover_region["count"] = cover_region["Shop Name"].apply(len) 

        fig_cover_region = px.line(cover_region, x="Region", y="count", text= "count", title= f"Quantity shop with coverage by regions for models {select_model }")
        fig_cover_region.update_traces(textposition = 'top center')
        st.plotly_chart(fig_cover_region)
        
        st.markdown("___")

        # Graph 9 : Meme chose mais en graphic Pie
        fig_pie_cov = go.Figure(data=[go.Pie(labels= covert["Model"], values= covert["Available Quantity"], title="Proportion coverage by Models", opacity= 0.5)])
        fig_pie_cov.update_traces (hoverinfo='label+percent', textfont_size=15,textinfo= 'label+percent', pull= [0.05, 0, 0, 0, 0],marker_line=dict(color='#FFFFFF', width=2))
        st.plotly_chart(fig_pie_cov)



        

    #######################################
    ### VENTE MODELES PAR REGIONS ######### 
    #######################################
            
    st.subheader("SALES MODELS BY REGIONS", divider="gray")
    # Afficher les modeles vendu par  region
    region_sales = date_frame.groupby(["Region", "Model"], as_index= False)["Sales Qty"].sum()
    graph_region_sales = px.bar(region_sales, x="Region", y="Sales Qty", barmode= "group", color="Model", text= "Sales Qty", title= "sales models by region")
    graph_region_sales.update_traces(textposition = 'outside')
    st.plotly_chart(graph_region_sales)
    
    # Proportion de la vente par region en 'Pie' [ Region, Qty]
    region_pie = date_frame.groupby(["Region"], as_index= False)["Sales Qty"].sum()
    graph_region_pie = go.Figure(data=[go.Pie(labels= region_pie["Region"], values= region_pie["Sales Qty"], title="Proportion sales by regions", opacity= 0.5)])
    graph_region_pie.update_traces (hoverinfo='label+percent', textfont_size=15,textinfo= 'label+percent', pull= [0.05, 0, 0, 0, 0],marker_line=dict(color='#FFFFFF', width=2))
    st.plotly_chart(graph_region_pie)


    # Activation/Inactivation general
    c1, c2 = st.columns(2, gap="small")

    with c1 :
        activation_gen = date_frame.groupby("Activation Status", as_index=False)["Sales Qty"].count()
        graph_activ_sales = px.bar(activation_gen, x="Activation Status", y="Sales Qty", color="Activation Status", text= "Sales Qty", title= "General activation and Inactivation")
        graph_activ_sales.update_traces(textposition = 'outside')
        st.plotly_chart(graph_activ_sales)
        
    # Activation/Inactivation par region
    with c2 :
        activation_region = date_frame.groupby(["Activation Status", "Region"], as_index=False)["Sales Qty"].count()
        graph_activ_region = px.bar(activation_region, x="Region", y="Sales Qty", color="Activation Status", text= "Sales Qty", title= "Regional activation and Inactivation")
        graph_activ_region.update_traces(textposition = 'outside')
        st.plotly_chart(graph_activ_region)
        


    #######################################
    ### SITUATION PAR SHOPS ###############
    #######################################
            
    st.subheader("SHOPS SITUATIONS", divider="gray")

    #########################
    ## Liste shops par vente
    ####

    st.subheader("1- Shops by Sell")
    vente_shops = date_frame.groupby(["Shop Name", "Month"])["Sales Qty"].sum().reset_index().sort_values("Sales Qty", ascending= False) # Tri du plus grand au plus petit
    st.dataframe(vente_shops)


    ##########
    ######
    st.subheader("2- Shops information Sell")
    shop_unique = date_frame["Shop Name"].unique() # On recupere le nom des shops


    # Avoir la possibilite de choisir un shop
    select_shops = st.selectbox("Choose your shop", shop_unique) # On selectionne les shops

    ####
    shop_select = date_frame[date_frame["Shop Name"] == select_shops] # On creer une variable qui donnera les donnee selon les shops selectionner
    total_salesx = shop_select.groupby("Shop Name", as_index = False)["Sales Qty"].sum()

    # Data metric

    v1, v2, v3 = st.columns(3)
    regions = shop_select["Region"].astype(str).unique()
    market = shop_select["Market"].astype(str).unique()

    with v1:
        st.metric(label="Shop selected :", value= select_shops, delta= "shop situation")
    with v2:
        st.metric(label="Total sales :", value= f"{int(total_salesx["Sales Qty"])} pcs", delta= "shop situation")
    with v3 :
        st.metric(label="Region :", value= str(regions[0]), delta= f" Market : {str(market[0])}")

    
    # Afficher ses ventes mensuel

    vente_mensuel = shop_select.groupby(["Shop Name", "Month"], as_index= False)["Sales Qty"].sum()
    fig_shop_select_bar = px.line(vente_mensuel, x="Month", y="Sales Qty", text="Sales Qty", title=f"Sales of shop : {select_shops} by months")
    fig_shop_select_bar.update_traces(textposition = 'top center')
    st.plotly_chart(fig_shop_select_bar)

    st.markdown("___")

    # Afficher sa couverture
    select_covert = couverture_dr[couverture_dr["Shop Name"] == select_shops]
    covert_shop = select_covert.groupby("Model", as_index= False)["Available Quantity"].sum()

    fig_models_covert_shop = px.bar(covert_shop, x="Model", y="Available Quantity", color="Model", text="Available Quantity", title= f"Coverage by Models for the shop : {select_shops}")
    fig_models_covert_shop.update_traces(textposition = 'outside')
    st.plotly_chart(fig_models_covert_shop) 
    st.markdown("___")

    # Afficher les models vendu
    shopModels = shop_select.groupby("Model", as_index= False)["Sales Qty"].sum()

    fig_shopModels = px.bar(shopModels, x="Model", y="Sales Qty", color="Model", text="Sales Qty", title= f"Sales by Models for shop : {select_shops} ")
    fig_shopModels.update_traces(textposition = 'outside')
    st.plotly_chart(fig_shopModels)

    graph_shop_pie = go.Figure(data=[go.Pie(labels= shopModels["Model"], values= shopModels["Sales Qty"], title= f"Proportion Sales for the shop : {select_shops}", opacity= 0.5)])
    graph_shop_pie.update_traces (hoverinfo='label+percent', textfont_size=15,textinfo= 'label+percent', pull= [0.05, 0, 0, 0, 0],marker_line=dict(color='#FFFFFF', width=2))
    st.plotly_chart(graph_shop_pie)

    st.markdown("___")

    # Afficher les activation et inactivations
    shop_activation = shop_select.groupby("Activation Status", as_index=False)["Sales Qty"].count()
    graph_shop_activ = px.bar(shop_activation, x="Activation Status", y="Sales Qty", color="Activation Status", text= "Sales Qty", title= f"Activation and Inactivation for the shop : {select_shops}")
    graph_shop_activ.update_traces(textposition = 'outside')
    st.plotly_chart(graph_shop_activ)

    # Pays de delivrance pour les produits vendus dans les shops

    if "Delivery Country" in shop_select.columns:
        shop_deliv = shop_select.groupby("Delivery Country", as_index= False)["Sales Qty"].sum()
        fig_shop_deliv = px.bar(shop_deliv, x="Delivery Country", y="Sales Qty", color="Delivery Country", text="Sales Qty", title=f"Delivery Country of the shop : {select_shops}")
        fig_shop_deliv.update_traces(textposition = 'outside')
        st.plotly_chart(fig_shop_deliv)

    else:
        st.warning("The 'Delivery Country' column does not exist in the data for this shop..")

    # Pays d'activations pour les produits vendus dans les shops

    if "Activation Country" in shop_select.columns:
        activation_produits = shop_select.groupby("Activation Country", as_index= False)["Sales Qty"].sum()
        graph_activ_p = px.bar(activation_produits, x="Activation Country", y="Sales Qty", color = "Activation Country", text="Sales Qty", title= f"Countries activation of product sold by the shop {select_shops}")
        graph_activ_p.update_traces(textposition = 'outside')
        st.plotly_chart(graph_activ_p)

        shops_date = shop_select.groupby(["Activation Country", "Activation Date"], as_index = False)["Sales Qty"].sum()
   
        st.dataframe(shops_date, use_container_width= True)
    else:
        st.warning("The 'Activation Country' column does not exist in the data for this shop.")    

            
    ##########################################
    ### DELIVRANCY AND ACTIVATION COUNTRIES ##
    ##########################################
            
    st.subheader("DELIVRANCY AND ACTIVATION COUNTRIES", divider="gray")
    # Graphique en Bar pour les pays de delivrance
    if "Delivery Country" not in date_frame.columns:
        st.warning("The 'Delivery Country' column does not exist in the data.") 
    else:
        pays_deliv = date_frame.groupby("Delivery Country", as_index= False)["Sales Qty"].sum()
        fig_pays = px.bar(pays_deliv, x="Delivery Country", y="Sales Qty", color="Delivery Country", text="Sales Qty", title="Delivery Country of Feature Phone Tecno in DRC")
        fig_pays.update_traces(textposition = 'outside')
        st.plotly_chart(fig_pays)
    

    # Graphique en carte pour les pays d'activation
    if "Activation Country" not in date_frame.columns:
        st.warning("The 'Delivery Country' column does not exist in the data.") 

    else:
        pays_activ = date_frame.groupby("Activation Country", as_index= False)["Sales Qty"].sum()
        pays_list = pays_activ["Activation Country"].unique()
        fig_monde = px.choropleth(data_frame= pays_activ, locations= pays_activ["Activation Country"], locationmode="country names", color="Sales Qty", color_continuous_scale = 'Viridis', title = 'Activation countries')
        st.plotly_chart(fig_monde)

        fig_world = px.bar(pays_activ, x= "Activation Country", y="Sales Qty", color="Activation Country", text = "Sales Qty", title = 'General Activation countries ')
        fig_world.update_traces(textposition = 'outside')
        st.plotly_chart(fig_world)

        pays_date = date_frame.groupby(["Activation Country", "Activation Date"], as_index = False)["Sales Qty"].sum()

        st.dataframe(pays_date, use_container_width= True)

    st.markdown("___")
    ## FIN
    st.title("THANKS FOR YOUR ATTENTION !")
    #"""
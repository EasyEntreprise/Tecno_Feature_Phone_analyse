# Librairies
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.metric_cards import style_metric_cards
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import os
import time


st.markdown("<h1 style='text-align: center; color: blue;'> TECNO FP SUB-DEALERS DASHBOARD </h1>", unsafe_allow_html= True)
st.markdown("<br/>", unsafe_allow_html= True)
st.markdown("<br/>", unsafe_allow_html= True)
st.markdown("<h6 style='text-align: center; color: red;'> Welcome in our SD purchases Dashboard for Tecno DRC feature phone. This dashboard is important for following the purchase of A sub-dealers."
" "
"</h6>", unsafe_allow_html= True)

st.markdown("___")

# Boutons fermeture et rederamarrage
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
    pass

st.markdown("___")

####################################
### Fonction de lecture de fichier
####################################

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

########################
# Load dataset
###
file = st.file_uploader("📂 Insert your Excel file by pressing the 'Browse files' button", type=["xlsx","xls", "csv"])

if file is not None:
    #dataset_full = pd.read_excel(file)
    dataset_full = read_file(file)

    # Traitement des valeurs null
    dataset = dataset_full.dropna(subset=['Purchases Qty (Pcs)']) # Mettre les valeurs null à '0'
    #dataset = dataset_full.dropna(how='all') # Supprimer les valeurs null

    # Creation des dates
    col1, col2 = st.columns(2)
    
    with col1:
        st.text("Select Date Range")
        start_date = st.date_input(label="Start Dates")
        

    with col2:
        st.text("Select Date Range")
        en_date = st.date_input(label="End Dates")

    # Provide a message for selected date range 
    st.success("you have choosen analytics from: "+str(start_date)+" to "+str(en_date))

    ##################
    # Filtre dates
    ###

    dataset["Date"] = pd.to_datetime(dataset["Date"], errors="coerce") # Convertir la colonne "Date" en datetime
    #date_frame = dataset[(dataset["Date"]>=str(start_date)) & (dataset["Date"]<=str(en_date))]
    date_frame = dataset[(dataset["Date"] >= pd.to_datetime(start_date)) & (dataset["Date"] <= pd.to_datetime(en_date))]


    with st.expander("Filter dates"):
        filter_date = dataframe_explorer(date_frame, case=False)
        st.dataframe(filter_date, use_container_width= True)

    ####
    # Creat columns and content
    col1, col2, col3 = st.columns([1, 1, 3])

    with col1 :
        st.subheader("List of SD", divider="rainbow")
        clients = date_frame.groupby(["Customers Name"], as_index= False).agg(
            purchases_sum = ("Purchases Qty (Pcs)", "sum"),
            invest_sum = ("Investments ($)", "sum")
        )
        st.dataframe(clients, use_container_width= True)

    with col2 :
        st.subheader("SD by regions", divider="rainbow")
        
        #-------------Recuperer Nbr client par region ----------
        kin_sd = date_frame[date_frame["Cities"]== "KINSHASA"] # Filtrer la dataset en Kinshasa comme Cities
        kat_sd = date_frame[date_frame["Cities"]== "KATANGA"]
        kc_sd  = date_frame[date_frame["Cities"]== "KONGO CENTRAL"]
        bk_sd  = date_frame[date_frame["Cities"]== "BIG KASAI"]
        be_sd  = date_frame[date_frame["Cities"]== "BIG EQUATOR"]


        kinshasa = kin_sd["Customers Name"].nunique() # Recuperer le nombre des clients
        katanga  = kat_sd["Customers Name"].nunique()
        kcongo   = kc_sd["Customers Name"].nunique()
        bkasai   = bk_sd["Customers Name"].nunique()
        bequator = be_sd["Customers Name"].nunique()

        # Recuperer le nom du meilleurs clients par region

        client_kin = kin_sd.loc[kin_sd["Purchases Qty (Pcs)"].idxmax()]
        client_kat = kat_sd.loc[kat_sd["Purchases Qty (Pcs)"].idxmax()]
        client_kc = kc_sd.loc[kc_sd["Purchases Qty (Pcs)"].idxmax()]
        client_bk = bk_sd.loc[bk_sd["Purchases Qty (Pcs)"].idxmax()]
        client_be = be_sd.loc[be_sd["Purchases Qty (Pcs)"].idxmax()]

        # Metric

        Kin = st.metric(label="SD to KINSHASA", value= kinshasa, delta=client_kin["Customers Name"])
        Kat = st.metric(label="SD to KATANGA", value= katanga, delta=client_kat["Customers Name"])
        KongC = st.metric(label="SD to KONGO-CENTRAL", value= kcongo, delta=client_kc["Customers Name"])
        BigK = st.metric(label="SD to Big-KASAÏ", value= bkasai, delta=client_bk["Customers Name"])
        BigE = st.metric(label="SD to Big-Equator", value= bequator, delta=client_be["Customers Name"])


    with col3 :
        st.subheader("Business Situation", divider="rainbow")
        a1, a2, a3 = st.columns(3) # Creating columns for (total customers, total purchase and total investiment)

        total_sd = date_frame["Customers Name"].nunique() # Recuperation du nombre des clients
        total_somme = date_frame.groupby("Country", as_index= False)["Purchases Qty (Pcs)"].sum()
        total_mean = date_frame.groupby("Country", as_index= False)["Investments ($)"].sum()


        a1.metric(label="Total Sub-dealers", value= total_sd, delta= "number total sd")
        a2.metric(label="Total Purchase", value= total_somme["Purchases Qty (Pcs)"], delta=date_frame["Purchases Qty (Pcs)"].sum()/total_sd)
        a3.metric(label="Total Investismen", value= total_mean["Investments ($)"].sum(), delta= date_frame["Investments ($)"].sum()/total_sd)

        st.subheader("Situation by regions", divider="blue")
        col1, col2, col3, col4, col5 = st.columns(5)

        sit_kin = kin_sd.groupby("Cities", as_index= False)["Purchases Qty (Pcs)"].sum()
        sit_kat = kat_sd.groupby("Cities", as_index= False)["Purchases Qty (Pcs)"].sum()
        sit_kc = kc_sd.groupby("Cities", as_index= False)["Purchases Qty (Pcs)"].sum()
        sit_bk = bk_sd.groupby("Cities", as_index= False)["Purchases Qty (Pcs)"].sum()
        sit_be = be_sd.groupby("Cities", as_index= False)["Purchases Qty (Pcs)"].sum() 

        col1.metric(label="KINSHASA Situation", value= sit_kin["Purchases Qty (Pcs)"], delta=kin_sd["Purchases Qty (Pcs)"].sum()/kinshasa)
        col2.metric(label="KATANGA Situation", value= sit_kat["Purchases Qty (Pcs)"], delta=kat_sd["Purchases Qty (Pcs)"].sum()/katanga)
        col3.metric(label="KONGO-CENTRAL Situation", value= sit_kc["Purchases Qty (Pcs)"], delta=kc_sd["Purchases Qty (Pcs)"].sum()/kcongo)
        col4.metric(label="BIG-KASAI Situation", value= sit_bk["Purchases Qty (Pcs)"], delta=bk_sd["Purchases Qty (Pcs)"].sum()/bkasai)
        col5.metric(label="BIG-EQUATOR Situation", value= sit_be["Purchases Qty (Pcs)"], delta=be_sd["Purchases Qty (Pcs)"].sum()/bequator)

        achat_year = date_frame.groupby("Cities", as_index= False)["Purchases Qty (Pcs)"].sum()
        fig_pie = go.Figure(data=[go.Pie(labels= achat_year["Cities"], values= achat_year["Purchases Qty (Pcs)"], title="Proportion des données par City", opacity= 0.5)])
        fig_pie.update_traces (hoverinfo='label+percent', textfont_size=15,textinfo= 'label+percent', pull= [0.05, 0, 0, 0, 0],marker_line=dict(color='#FFFFFF', width=2))
        st.plotly_chart(fig_pie)

    # Style the metric
    style_metric_cards(background_color="#3c4d66", border_left_color="#99f2c8", border_color="#0006a")
        
    ####################
    ## Sub-dealer evolution by years

    st.subheader("Sub-dealer Evolution by Years", divider="rainbow")
    # Create a DataFrame for sub-dealer evolution by years
    sub_dealer_evolution = dataset.groupby("Years", as_index= False)["Customers Name"].nunique()

    fig_sd_evolution = px.line(sub_dealer_evolution, x="Years", y="Customers Name", text="Customers Name", title="Evolution of Sub-dealers by Years")
    fig_sd_evolution.update_traces(textposition = 'top center')
    st.plotly_chart(fig_sd_evolution)

    #######################
    #### Market
    #############
    st.subheader("Markets Situation", divider="rainbow")

    region_id =  date_frame["Cities"].unique()

    all_city = ["All Regions"] + sorted(date_frame["Cities"].dropna().unique().tolist())
    selected_city = st.selectbox("Select your region here", all_city )
    #dataset_cities = date_frame[date_frame["Cities"] == selected_city]

    if selected_city == "All Regions":
        dataset_cities = date_frame

    else :
        dataset_cities = date_frame[date_frame["Cities"] == selected_city]
    
    market = dataset_cities.groupby("Market", as_index= False)["Purchases Qty (Pcs)"].sum()

    colx1, colx2 = st.columns(2)

    with colx1:
        fig_market = px.bar(market, x="Market", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title=f"Purchase by market in {selected_city}", color="Market")
        fig_market.update_traces(textposition = 'outside')
        st.plotly_chart(fig_market)

    with colx2:
        fig_market_pie = go.Figure(data=[go.Pie(labels= market["Market"], values= market["Purchases Qty (Pcs)"], title=f"Proportion of purchases by market in {selected_city}", opacity= 0.5)])
        fig_market_pie.update_traces (hoverinfo='label+percent', textfont_size=15,textinfo= 'label+percent', pull= [0.05, 0, 0, 0, 0],marker_line=dict(color='#FFFFFF', width=2))
        st.plotly_chart(fig_market_pie)

    ###########################
    #### Sub-dealer by Market
    #############
    st.subheader("Sub-dealers by Markets Situation", divider="rainbow")

    market_id =  date_frame["Market"].unique()

    all_markets = ["All Markets"] + sorted(date_frame["Market"].dropna().unique().tolist())
    selected_markets = st.selectbox("Select your Market here", all_markets)
    #dataset_market = date_frame[date_frame["Market"] == selected_markets]

    if selected_markets == "All Markets":
        dataset_market = date_frame

    else :
        dataset_market = date_frame[date_frame["Market"] == selected_markets]

    market_sd = dataset_market.groupby("Customers Name", as_index= False)["Purchases Qty (Pcs)"].sum()

    colz1, colz2 = st.columns(2)

    with colz1:
        fig_market_sd = px.bar(market_sd, x="Customers Name", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title=f"Purchase by market in {selected_city}", color="Customers Name")
        fig_market_sd.update_traces(textposition = 'outside')
        st.plotly_chart(fig_market_sd)

    with colz2:
        fig_market_sd_pie = go.Figure(data=[go.Pie(labels= market_sd["Customers Name"], values= market_sd["Purchases Qty (Pcs)"], title=f"Sub-dealers' Proportion purchases by market in {selected_markets}", opacity= 0.5)])
        fig_market_sd_pie.update_traces (hoverinfo='label+percent', textfont_size=15,textinfo= 'label+percent', pull= [0.05, 0, 0, 0, 0],marker_line=dict(color='#FFFFFF', width=2))
        st.plotly_chart(fig_market_sd_pie)


    ###############################
    # Situation annuel des achats
    ####
    st.subheader("Yearly purchase situation (SD)", divider="rainbow")
    b1, b2 = st.columns([2, 3])

    with b1:
        achat_year = dataset_full.groupby("Years", as_index= False)["Purchases Qty (Pcs)"].sum()
        fig_years = px.line(achat_year, x="Years", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title="Total Purchase by Years")
        fig_years.update_traces(textposition = 'top center')
        st.plotly_chart(fig_years)
        

    with b2:
        achat_month = date_frame.groupby("Date", as_index= False)["Purchases Qty (Pcs)"].sum()
        fig_mois = px.line(achat_month, x="Date", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title="Total Purchase by Months")
        fig_mois.update_traces(textposition = 'top center')
        st.plotly_chart(fig_mois)
        

    ###########################
    # Situation modeles
    #####
    st.subheader("Yearly purchase situation (Models)", divider="rainbow")
    c1, c2 = st.columns([2, 3])

    with c1:
        achat_models = dataset_full.groupby(["Products", "Years"], as_index= False)["Purchases Qty (Pcs)"].sum()
        fig_models = px.bar(achat_models, x="Years", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title="Purchase by models (Years)", color="Products")
        st.plotly_chart(fig_models)
        

    with c2:
        models_month = date_frame.groupby(["Products", "Date"], as_index= False)["Purchases Qty (Pcs)"].sum()
        fig_modelx = px.bar(models_month, x="Date", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title="Purchase by models(Months)", color="Products")
        st.plotly_chart(fig_modelx)

    
    # Creation d'une liste des models uniques
    models_data = date_frame["Products"].unique()

    # Creation d'une selecteur multiple
    selected_models = st.multiselect("Select your models", models_data)


    # Filtrage des donnees en fonction de la selection
    date_groupby = date_frame.groupby(["Products", "Date"], as_index= False)["Purchases Qty (Pcs)"].sum()
    df_filtered = date_groupby[date_groupby["Products"].isin(selected_models)]

    fig_select = px.line(df_filtered, x="Date", y="Purchases Qty (Pcs)", color="Products", text="Purchases Qty (Pcs)")
    fig_select.update_traces(textposition = 'top center')
    st.plotly_chart(fig_select)
 
   # Sélecteur de modèle (SEUL filtre demandé)
    modele_choisi = st.selectbox(
        "Choisir le modèle",
        sorted(date_frame["Products"].unique())
    )

    df_models = date_frame[date_frame["Products"] == modele_choisi]

    # Agrégation
    df_group = (
        df_models.groupby(["Customers Name", "Products", "Date"], as_index=False)
        ["Purchases Qty (Pcs)"]
        .sum()
    )

    # Pivot mois en colonnes
    tableau = df_group.pivot_table(
        index=["Customers Name", "Products"],
        columns="Date",
        values="Purchases Qty (Pcs)"
    )

    tableau = tableau.reset_index()

    # Affichage final
    st.subheader(f"Monthly quantity by Modèle : {modele_choisi}")
    st.dataframe(tableau, use_container_width=True)


    ########################
    # Target clients & Realisation 
    ########
    st.subheader("Target & Achievment", divider="grey")

    view_2025 = dataset_full[dataset_full["Years"] == 2025]
    target_2025 = view_2025.groupby("Date", as_index= False)["Purchases Qty (Pcs)"].sum()

    def creer_target_si_un_mois(target_2025):
        if target_2025["Date"].nunique() == 1:
            target_2025["Target"] = 9600
            return target_2025["Target"]
        
        elif target_2025["Date"].nunique() == 2:
            target_2025["Target"] = [9600, 9600]
            return target_2025["Target"]
        elif target_2025["Date"].nunique() == 3:  
            target_2025["Target"] = [9600, 9600, 9600] # Creation d'une colonne target
            return target_2025["Target"]
        elif target_2025["Date"].nunique() == 4:
            target_2025["Target"] = [9600, 9600, 9600, 8330]
            return target_2025["Target"]
        elif target_2025["Date"].nunique() == 5:
            target_2025["Target"] = [9600, 9600, 9600, 8330, 9335]
            return target_2025["Target"]
        elif target_2025["Date"].nunique() == 6:
            target_2025["Target"] = [9600, 9600, 9600, 8330, 9335, 9520]
            return target_2025["Target"]
        elif target_2025["Date"].nunique() == 7:
            target_2025["Target"] = [9600, 9600, 9600, 8330, 9335, 9520, 9110]
            return target_2025["Target"]
        elif target_2025["Date"].nunique() == 8:
            target_2025["Target"] = [9600, 9600, 9600, 8330, 9335, 9520, 9110, 9175]
            return target_2025["Target"]
        elif target_2025["Date"].nunique() == 9:
            target_2025["Target"] = [9600, 9600, 9600, 8330, 9335, 9520, 9110, 9175, 9200]
            return target_2025["Target"]
        elif target_2025["Date"].nunique() == 10:
            target_2025["Target"] = [9600, 9600, 9600, 8330, 9335, 9520, 9110, 9175, 9200, 9500]
            return target_2025["Target"]
        elif target_2025["Date"].nunique() == 11:
            target_2025["Target"] = [9600, 9600, 9600, 8330, 9335, 9520, 9110, 9175, 9200, 9500, 9970]
            return target_2025["Target"]
        elif target_2025["Date"].nunique() == 12:
            target_2025["Target"] = [9600, 9600, 9600, 8330, 9335, 9520, 9110, 9175, 9200, 9500, 9970, 9900]
            return target_2025["Target"]
        else:
            return None  # ou gérer autrement si plusieurs mois
        
    target = creer_target_si_un_mois(target_2025)

    # Creation graphic combiner (bar and line)
    #"""
    fig_cmb = go.Figure()

    #-- Barre pour l'achievment ---
    fig_cmb.add_trace(go.Bar(
        x = target_2025["Date"],
        y = target_2025["Purchases Qty (Pcs)"],
        name = "Achievment",
        text = target_2025["Purchases Qty (Pcs)"],
        textposition= "auto", # il y a 'auto' 'outside' 'inside'
        marker_color = "skyblue"
    ))

    #-- Ligne pour le target --
    fig_cmb.add_trace(go.Scatter(
        x = target_2025["Date"],
        y = target,
        name ="Target (Pcs)",
        mode = 'lines+text+markers',
        text = target_2025["Target"],
        textposition= "top center",
        line = dict(color = "orange", width = 3)
    ))
    #"""

    # Mettre a jour la mise en page
    #"""
    fig_cmb.update_layout(
        title = "Sub-dealers > Target and Achievment for 2025", 
        yaxis = dict(title= "Purchases Qty (Pcs)"),
        yaxis2 = dict(title= "Buy", overlaying = 'y', side = 'right'), 
        xaxis = dict(title = "Month"),
        legend = dict(x=0.1, y=1.1, orientation = 'h'), 
        bargap = 0.3
    )

    st.plotly_chart(fig_cmb)


    ##############################
    #### PREDICTION DES ACHATS ###
    #############################
    
    st.header("FUTURE PURCHASING FORECASTS", divider="rainbow")

    #############################
    ## 1- Predictions Global

    st.subheader("1. 📊Global Forecasts")

    dataset["Date"] = pd.to_datetime(dataset["Date"])
    st.success(f"{len(dataset)} lignes de données chargées avec succès ✅")

    # Regrouper les ventes par mois
    prediction_global = dataset.groupby("Date")["Purchases Qty (Pcs)"].sum().reset_index()
    prediction_global = prediction_global.rename(columns={"Date":"ds", "Purchases Qty (Pcs)":"y"})  # On renome la colonne "Months" en "ds" et celui de "Purchased Qty" en "y". Car Prophet ne reconnait que ces noms

    # Modèle Prophet
    purchases_global = Prophet()
    purchases_global.fit(prediction_global)

    # Prévision sur 3 mois
    predict_futur = purchases_global.make_future_dataframe(periods=3, freq='M') # On fait une prediction de 3 Mois en tenant compte de l'histoire des achats
    forecast_global = purchases_global.predict(predict_futur)
    

    # -------------------------------
    # 4️⃣ Affichage des données
    # -------------------------------
    with st.expander("📄 Voir les données de prévision brutes"):
        st.dataframe(forecast_global[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail())


    ##############################
    #### Affichage des résultats
    ##########

    # Graphique Plotly (interactif)

    bg_color = st.sidebar.color_picker("Background", "#f0f8ff")
    paper_color = st.sidebar.color_picker("Background general", "#ffffff")

    fig_global = plot_plotly(purchases_global, forecast_global)
    fig_global.update_layout(
        title = "Prévision Globale des ventes Tecno",
        xaxis_title = "Date",
        yaxis_title ="Quantité achetée",
        template ="plotly_white",
        
        plot_bgcolor = bg_color,     #'rgba(240,248,255,1)',  # 🔹 bleu très clair à l'intérieur du graphique
        paper_bgcolor = paper_color, #'rgba(255,255,255,1)', # 🔹 fond général blanc
    )

    st.plotly_chart(fig_global, use_container_width=True)

    ##############################
    ## 2- Predictions Par Modeles
    st.subheader("2. 📊Models Forecasts")

    # Creation d'une selecteur multiple
    select_models_all = st.multiselect("Please can you select your model here ? (One model please ! ) : ", models_data)

    # Filtrage des donnees en fonction de la selection
    sd_models_choose_all = dataset[dataset["Products"].isin(select_models_all)]
    sd_models_all = sd_models_choose_all.groupby("Date")["Purchases Qty (Pcs)"].sum().reset_index()
    sd_models_all = sd_models_all.rename(columns={"Date": "ds", "Purchases Qty (Pcs)": "y"})

    model_forecast_all = Prophet()
    model_forecast_all.fit(sd_models_all)

    model_future_all = model_forecast_all.make_future_dataframe(periods=3, freq='M')
    forecast_model_all = model_forecast_all.predict(model_future_all)

    st.write(f"📊 Forecast Evolution by {select_models_all}")
    fig_model_preview_all = plot_plotly(model_forecast_all, forecast_model_all)
    fig_model_preview_all.update_layout(
        title = "Clients purchase model forcast ",
        xaxis_title = "Months",
        yaxis_title ="Purchases Quantity by model",
        template ="plotly_white",
        
        plot_bgcolor = bg_color,     #'rgba(240,248,255,1)',  # 🔹 bleu très clair à l'intérieur du graphique
        paper_bgcolor = paper_color, #'rgba(255,255,255,1)', # 🔹 fond général blanc
    )
    st.plotly_chart(fig_model_preview_all, use_container_width=True)


    #############################
    ## 3- Predictions Par Ville
    st.subheader("3. 📊Cities Forecasts")

    # Vérifier les colonnes requises
    required_cols = {"Cities", "Date", "Purchases Qty (Pcs)"}
    if not required_cols.issubset(dataset.columns):
        st.error(f"The file must contain the columns : {', '.join(required_cols)}")
        st.stop()
    
    # Préparer les données
    
    date_ville = dataset.groupby(["Cities", "Date"], as_index= False)["Purchases Qty (Pcs)"].sum() 
    date_ville = date_ville.rename(columns={"Date":"ds", "Purchases Qty (Pcs)":"y"})
    date_ville["ds"] = pd.to_datetime(date_ville["ds"])

    cities = sorted(dataset["Cities"].unique())
    st.success(f"✅ {len(cities)} cities detected : {', '.join(cities)}")

    # -------------------------------
    # Paramètres utilisateur
    # -------------------------------
    nb_mois = st.slider("Number of months to predict", 1, 12, 3)  # 3 mois par défaut

    col1, col2 = st.columns(2)
    predictions_all = []

    # -------------------------------
    # Prévision par ville
    # -------------------------------
    st.header("📈 Forecasts by City")

    for i, city in enumerate(cities):
        city_data = date_ville[date_ville["Cities"] == city][["ds", "y"]]
        
        if len(city_data) < 5:
            st.warning(f"⚠️ Too little data for {city}, forecast ignored.")
            continue

        model_ville = Prophet()
        model_ville.fit(city_data)
        future_ville = model_ville.make_future_dataframe(periods=nb_mois, freq='M')
        forecast_ville = model_ville.predict(future_ville)
        forecast_ville["Cities"] = city
        predictions_all.append(forecast_ville)

        # Graphique interactif
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=city_data["ds"], y=city_data["y"], mode="markers+lines", name="Historique"))
        fig.add_trace(go.Scatter(x=forecast_ville["ds"], y=forecast_ville["yhat"], mode="lines", name="Prévision"))
        fig.update_layout(title=f"📍 {city}", xaxis_title="Date", yaxis_title="Quantité", template="plotly_white")

        # Affichage côte à côte
        if i % 2 == 0:
            with col1:
                st.plotly_chart(fig, use_container_width=True)
        else:
            with col2:
                st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # 4️⃣ Comparatif entre villes
    # -------------------------------
    if predictions_all:
        predictions_all = pd.concat(predictions_all)

        # Dernière date prévue = prévision la plus récente
        latest_date = predictions_all["ds"].max()
        summary = (
            predictions_all[predictions_all["ds"] == latest_date]
            .groupby("Cities")["yhat"]
            .sum()
            .reset_index()
            .sort_values(by="yhat", ascending=False)
        )

        st.text("🏆 Ranking of Cities by Purchasing Forecast")
        
        col3, col4 = st.columns([2, 1])
        with col3:
            fig_bar = px.bar(
                summary,
                x="Cities",
                y="yhat",
                title="Average purchasing forecasts by city",
                labels={"yhat": "Expected quantity", "City": "City"},
                text_auto=".0f",
                color="Cities"
            )
            fig_bar.update_layout(template="plotly_white")
            st.plotly_chart(fig_bar, use_container_width=True)

        with col4:
            st.dataframe(summary.rename(columns={"yhat": "Planned quantity"}), hide_index=True)

    else:
        st.info("⬆️ Import your Excel file to get started.")


    

    #######################################
    ######### Profil des clients ########## 
    #######################################
    st.subheader("CUSTOMERS PROFILE", divider="rainbow")
    
    sd_unique = dataset["Customers Name"].unique()
        
    select_sd = st.selectbox("Choose your sub-dealer name", sd_unique) # On selectionne les clients
    region_sd = date_frame[date_frame["Customers Name"]==select_sd] # Recuperer la region du client selectionner
    total_buy = region_sd.groupby("Customers Name", as_index= False)["Purchases Qty (Pcs)"].sum() # Total achat du client selectionner 
    total_inv = region_sd.groupby("Customers Name", as_index= False)["Investments ($)"].sum() # Total achat du client invest

    region_predict = dataset[dataset["Customers Name"]==select_sd] # Recuperer la region du client selectionner

    nbr_line = region_predict["Months"].unique() 

    col6, col7, col8 = st.columns(3)

    col6.metric(label="SD NAME", value=select_sd, delta=str(region_sd["Cities"].unique()))
    col7.metric(label="Total Purchase (Pcs)", value=int(total_buy["Purchases Qty (Pcs)"]), delta=int(total_buy["Purchases Qty (Pcs)"])/int(nbr_line.shape[0]))
    col8.metric(label="Total Invest ($)", value=int(total_inv["Investments ($)"]), delta=int(total_inv["Investments ($)"])/int(nbr_line.shape[0]))

    # Graphic radar
    achat_models_sd = region_sd.groupby(["Customers Name", "Products"], as_index = False)["Purchases Qty (Pcs)"].sum()

    fig_profil = go.Figure()

    fig_profil.add_trace(go.Scatterpolar(
        r= achat_models_sd["Purchases Qty (Pcs)"],
        theta= achat_models_sd["Products"],
        fill= 'toself',
        name=select_sd
    ))

    fig_profil.update_layout(
        polar = dict(
            radialaxis= dict(visible=True, range= [0, 100])
        ),
        showlegend = False
    )

    st.plotly_chart(fig_profil)
    st.markdown("___")

        
    # Graphic achat mensuel du client selectionner
    achat_mensuel_sd = region_sd.groupby(["Customers Name", "Date"], as_index = False)["Purchases Qty (Pcs)"].sum()
    fig_sd = px.line(achat_mensuel_sd, x="Date", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title=f"Purchases Sub-dealers {select_sd} by months")
    fig_sd.update_traces(textposition = 'top center')
    st.plotly_chart(fig_sd)
    st.markdown("___")

    # Graphic achat mensuel du client par models
        
    fig_sd_models = px.bar(achat_models_sd, x="Products", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title=f"Purchases of  Sub-dealers {select_sd} by models", color="Products")
    fig_sd_models.update_traces(textposition = 'outside')
    st.plotly_chart(fig_sd_models)

    # Graphic achat mensuel du client selectionner par models

    models = region_sd["Products"].unique()
    sd_select = st.multiselect("Select models", models)
    
    sd = region_sd.groupby(["Products", "Date"], as_index= False)["Purchases Qty (Pcs)"].sum()
    sd_filtered = sd[sd["Products"].isin(sd_select)]
    
    fig_sd_models_line = px.line(sd_filtered, x="Date", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title="Evolutions purchase models by months")
    fig_sd_models_line.update_traces(textposition = 'top center')
    st.plotly_chart(fig_sd_models_line)

    ######
    # Prediction client
    st.title(f"Purchase Forecasts for customer : {select_sd}")

    st.write("1- Monthly FORECAST")
    predict_sd_mensuel = region_predict.groupby(["Date"], as_index = False)["Purchases Qty (Pcs)"].sum()
    sd_predictionMensuel = predict_sd_mensuel.rename(columns={"Date":"ds", "Purchases Qty (Pcs)":"y"})
    
    # Modele Prophet
    sd_predict_month = Prophet()
    sd_predict_month.fit(sd_predictionMensuel)

    # Prévision sur 3 mois
    sd_futur = sd_predict_month.make_future_dataframe(periods=3, freq='M')
    sd_forcast = sd_predict_month.predict(sd_futur)

    # -------------------------------
    # Affichage de resultat
    # -------------------------------

    month_sd_forcast = plot_plotly(sd_predict_month, sd_forcast)
    month_sd_forcast.update_layout(
        title = "Clients purchase monthly forcast ",
        xaxis_title = "Months",
        yaxis_title ="Purchases Quantity for SD",
        template ="plotly_white",
        
        plot_bgcolor = bg_color,     #'rgba(240,248,255,1)',  # 🔹 bleu très clair à l'intérieur du graphique
        paper_bgcolor = paper_color, #'rgba(255,255,255,1)', # 🔹 fond général blanc
    )

    st.plotly_chart(month_sd_forcast, use_container_width=True)
    

    st.write("2- Models Forecast")

    # Creation d'une selecteur multiple
    select_models = st.multiselect("Select your model here (One model please ! ) :", models_data)

    # Filtrage des donnees en fonction de la selection
    sd_models_choose = region_predict[region_predict["Products"].isin(select_models)]
    sd_models = sd_models_choose.groupby("Date")["Purchases Qty (Pcs)"].sum().reset_index()
    sd_models = sd_models.rename(columns={"Date": "ds", "Purchases Qty (Pcs)": "y"})

    model_forecast = Prophet()
    model_forecast.fit(sd_models)

    model_future = model_forecast.make_future_dataframe(periods=3, freq='M')
    forecast_model = model_forecast.predict(model_future)

    st.subheader(f"📊 Forecast Evolution by {select_models}")
    fig_model_preview = plot_plotly(model_forecast, forecast_model)
    fig_model_preview.update_layout(
        title = "Clients purchase model forcast ",
        xaxis_title = "Months",
        yaxis_title ="Purchases Quantity bym odel",
        template ="plotly_white",
        
        plot_bgcolor = bg_color,     #'rgba(240,248,255,1)',  # 🔹 bleu très clair à l'intérieur du graphique
        paper_bgcolor = paper_color, #'rgba(255,255,255,1)', # 🔹 fond général blanc
    )
    st.plotly_chart(fig_model_preview, use_container_width=True)

    st.markdown("___")
    ## FIN
    st.title("THANKS FOR YOUR ATTENTION !")

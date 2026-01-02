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
import matplotlib.pyplot as plt
import os
import time


st.markdown("<h1 style='text-align: center; color: blue;'> TECNO SP DASHBOARD FOR ST</h1>", unsafe_allow_html= True)
st.markdown("<br/>", unsafe_allow_html= True)
st.markdown("<br/>", unsafe_allow_html= True)
st.markdown("<h6 style='text-align: center; color: red;'> Welcome in our Smart Phone dashboard for Tecno brand DRC. This dashboard is important for following the ST purchase of customers."
"In this "
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

# Load dataset
file = st.file_uploader("📂 Inserer votre fichier Excel en appuyant sur le bouton 'Browse files'", type=["xlsx","xls", "csv"])

if file is not None:
    
    #dataset_full = pd.read_excel(file)
    dataset_full = read_file(file)

    # Traitement des valeurs null
    dataset = dataset_full.dropna(subset='Purchased Qty') # Supprimer les valeurs null

    # Creation des dates
    col1, col2 = st.columns(2)
    
    with col1:
        st.text("Select Date Range")
        start_date = st.date_input(label="Start Dates")

    with col2:
        st.text("Select Date Range")
        en_date = st.date_input(label="End Dates")

    # Provide a message for selected date range 
    st.success(" you have choosen analytics from: "+str(start_date)+" to "+str(en_date))

    # Filtre dates
    date_frame = dataset[(dataset["Date"]>=str(start_date)) & (dataset["Date"]<=str(en_date))]

    with st.expander("Filter dates"):
        filter_date = dataframe_explorer(date_frame, case=False)
        st.dataframe(filter_date, use_container_width= True)
    
    
    #####################################
    # Creation columns of metric
    ####
    st.subheader("Data Metric", divider="rainbow")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    #----------------------------------------------------
    price_high = date_frame.loc[date_frame["Prices ($)"].idxmax()]
    converter_high_price = str(price_high["Products"])
    #-----
    price_low = date_frame.loc[date_frame["Prices ($)"].idxmin()]
    converter_low_price = str(price_low["Products"])
    #----------------------------------------------------

    db = date_frame.groupby("Weeks")["Purchased Qty"].sum().reset_index() # Faire un group by sans index
    mean = date_frame.groupby("Products", as_index= False)["Purchased Qty"].sum()
    som = mean.sum()
    nbr = date_frame["Products"].nunique()

    col1.metric(label="Sum Purchase(Pcs)", value= date_frame["Purchased Qty"].sum(), delta="General Purchase(Pcs)")
    col2.metric(label="General Average(Pcs)", value= som["Purchased Qty"]/nbr, delta="General Average(Pcs)")
    col3.metric(label="High Price($)", value= date_frame["Prices ($)"].max(), delta = converter_high_price)
    col4.metric(label="Low Price($)", value= date_frame["Prices ($)"].min(), delta = converter_low_price)

    dbmax = db.loc[db["Purchased Qty"].idxmax()] # Recuperation de la semaine avec le plus grand achat
    dbmin = db.loc[db["Purchased Qty"].idxmin()] # Recuperation de la semaine avec le plus faible achat

    col5.metric(label="Best week (Pcs)", value=db["Purchased Qty"].max(), delta= dbmax["Weeks"]) # Afficher le metric de la semaine avec plus d'achats
    col6.metric(label="Bad week (Pcs)", value=db["Purchased Qty"].min(), delta= dbmin["Weeks"]) # Afficher le metric de la semaine avec moins d'achats


    a1, a2 = st.columns(2)

    with a1 :
        st.subheader("Graphic Keys models", divider="blue")
        series = date_frame["SERIES"].unique()
        
        selecte_series = st.multiselect("Selecte your series here", series, default=["SPARK", "CAMON", "POP"])
        key_series = date_frame.groupby(["SERIES"], as_index= False)["Purchased Qty"].sum()
        series_filter = key_series[key_series["SERIES"].isin(selecte_series)]

        fig_key = px.bar(series_filter, x="SERIES", y="Purchased Qty", text="Purchased Qty", title="Graphic Series and Purchased Qty", color="SERIES")
        st.plotly_chart(fig_key)

        #st.markdown("___")
        area_data = date_frame.groupby("City")["Purchased Qty"].sum().reset_index()
        fig_pie = go.Figure(data=[go.Pie(labels= area_data["City"], values= area_data["Purchased Qty"], title="Proportion purchase by City", opacity= 0.5)])
        fig_pie.update_traces (hoverinfo='label+percent', textfont_size=15,textinfo= 'label+percent', pull= [0.05, 0, 0, 0, 0],marker_line=dict(color='#FFFFFF', width=2))
        st.plotly_chart(fig_pie)

    #####   
    # Metric keys models
    with a2 :
        st.subheader("Keys Series", divider="rainbow")
        key1,key2 = st.columns(2)

        Spark = date_frame[date_frame["SERIES"]=="SPARK"]
        key1.metric(label="Series Spark (Pcs)", value= Spark["Purchased Qty"].sum(), delta=Spark["Purchased Qty"].mean()) 

        Camon = date_frame[date_frame["SERIES"]=="CAMON"]
        key2.metric(label="Serie Camon (Pcs)", value= Camon["Purchased Qty"].sum(), delta=Camon["Purchased Qty"].mean()) 
        

        key3,key4 = st.columns(2)
        Pop = date_frame[date_frame["SERIES"]=="POP"]
        key3.metric(label="Series Pop (Pcs)", value= Pop["Purchased Qty"].sum(), delta=Pop["Purchased Qty"].mean()) 

        Phantom = date_frame[date_frame["SERIES"]=="PHANTOM"]
        key4.metric(label="Series Phantom (Pcs)", value= Phantom["Purchased Qty"].sum(), delta=Phantom["Purchased Qty"].mean())

        dataset_kin = date_frame[date_frame["City"]=="KIN"]
        dataset_Lushi = date_frame[date_frame["City"]=="LUSHI"]
        col11, col12 = st.columns(2)
        col11.metric(label="Kin Purchase(Pcs)", value= dataset_kin["Purchased Qty"].sum(), delta= dataset_kin["Purchased Qty"].mean())
        col12.metric(label="Lushi Purchase(Pcs)", value= dataset_Lushi["Purchased Qty"].sum(), delta= dataset_Lushi["Purchased Qty"].mean())

        # Style the metric
        style_metric_cards(background_color="#636363", border_left_color="#a8ff78", border_color="#9FC1FF")

        #
        st.markdown("___")
        fig_chanel = px.bar(area_data, x="City", y="Purchased Qty", text="Purchased Qty", title=f"Situation of Channel Kin and Lushi", color="City")
        fig_chanel.update_traces(textposition = 'outside')
        st.plotly_chart(fig_chanel)
    
    # Situation purchased
    st.subheader("Purchase Situation", divider="rainbow")
    
    # Creation d'une liste des models uniques
    serie_data = date_frame["SERIES"].unique()

    # Creation d'un selecteur multiple
    selected_series = st.multiselect("Selecte your series", serie_data, default=["SPARK", "CAMON", "POP"])

    # Filtrage des donnees en fonction de la selection
    date_groupby = date_frame.groupby(["City","SERIES"], as_index= False)["Purchased Qty"].sum()
    df_filtered = date_groupby[date_groupby["SERIES"].isin(selected_series)]
        
    fig_area = px.bar(df_filtered, x="City", y="Purchased Qty", text="Purchased Qty", title="Series purchase by region", color="SERIES", barmode="group")
    fig_area.update_traces(textposition = 'outside')
    st.plotly_chart(fig_area)

    st.markdown("___")

    # Creation d'une liste des models uniques
    category_data = date_frame["Categories"].unique()

    # Creation d'une selecteur multiple
    selected_category = st.multiselect("Selecte your categories", category_data) # "SPARK 40", "CAMON 40", "POP 10"

    # Filtrage des donnees en fonction de la selection
    date_groupby = date_frame.groupby(["City","Categories"], as_index= False)["Purchased Qty"].sum()
    df_filtered = date_groupby[date_groupby["Categories"].isin(selected_category)]
        
    fig_area = px.bar(df_filtered, x="City", y="Purchased Qty", text="Purchased Qty", title="Category purchased by region", color="Categories", barmode="group")
    fig_area.update_traces(textposition = 'outside')
    st.plotly_chart(fig_area)


    #####################
    # Situation Models
    ####
    
    st.subheader("Situation by Models", divider="rainbow")
    date_groupbyx = date_frame.groupby(["Products"], as_index= False)["Purchased Qty"].sum()
        
    fig_product = px.bar(date_groupbyx, x="Products", y="Purchased Qty", color="Products", text="Purchased Qty")
    fig_product.update_traces(textposition = 'outside')
    st.plotly_chart(fig_product)

    fig_product_pie = go.Figure(data = [go.Pie(labels = date_groupbyx["Products"], values= date_groupbyx["Purchased Qty"], title = "Proportions models", opacity=0.5)])
    fig_product_pie.update_traces (hoverinfo='label+percent', textfont_size=15,textinfo= 'label+percent', pull= [0.05, 0, 0, 0, 0],marker_line=dict(color='#FFFFFF', width=2))
    st.plotly_chart(fig_product_pie)

    ##########################
    # Situation Models by months
    #####
    # Creation d'une liste des models uniques
    models_data_months = date_frame["Products"].unique().tolist()

    # Creation d'une selecteur multiple
    selected_models_months = st.multiselect("Selecte your differents models", models_data_months)


    # Filtrage des donnees en fonction de la selection
    purchase_groupby_months = date_frame.groupby(["Products", "Months"], as_index= False)["Purchased Qty"].sum()
    #st.write(purchase_groupby_months)
    df_purchase_months = purchase_groupby_months[purchase_groupby_months["Products"].isin(selected_models_months)]

    fig_select_months = px.line(df_purchase_months, x="Months", y="Purchased Qty", color="Products", text="Purchased Qty")
    fig_select_months.update_traces(textposition = 'top center')
    st.plotly_chart(fig_select_months)
 

    ##################################
    # Situation Models by years
    #####

    st.subheader("Situation Models by years", divider="rainbow")
    with st.expander("Filter years"):
        date_groupby = dataset.groupby(["Products", "Years"], as_index= False)["Purchased Qty"].sum()
        filter_years = dataframe_explorer(date_groupby, case=False)
        st.dataframe(filter_years, use_container_width= True)

    fig_y =  px.bar(filter_years, x="Years", y="Purchased Qty", color="Products", barmode="group", text="Purchased Qty")
    fig_y.update_traces(textposition = 'outside')
    st.plotly_chart(fig_y)

    #########################
    # Situation by Months
    #####

    st.subheader("Situation by Months", divider="rainbow")
    with st.expander("Filter years"):
        date_groupby = dataset.groupby(["Years", "Months"], as_index= False)["Purchased Qty"].sum()
        filter_years = dataframe_explorer(date_groupby, case=False)
        st.dataframe(filter_years, use_container_width= True)

    fig_month =  px.line(filter_years, x="Months", y="Purchased Qty", text="Purchased Qty")
    fig_month.update_traces(textposition = 'top center')
    st.plotly_chart(fig_month)
    
    
    ###########################
    # Situation by weeks
    ####

    st.subheader("Situation purchase by weeks", divider="rainbow")

    col7, col8 = st.columns(2)
    recupMois = date_frame.groupby(["Weeks", "Date"])["Purchased Qty"].sum().reset_index()

    with col7:
        maximal = recupMois.loc[recupMois["Purchased Qty"].idxmax()]
        string_convert_max = str(maximal["Date"]) # J'ai convertir mon pandas serie en chaine des caracteres
        string_convert_max = string_convert_max.split() # avec split, je divise ma chaine de caracteres en deux partie en choisisant l'espace vide comme indice de separation
        st.metric(label="Best weekly purchase (Pcs)", value=db["Purchased Qty"].max(), delta= string_convert_max[0])
    
    with col8:
        minimal = recupMois.loc[recupMois["Purchased Qty"].idxmin()]
        string_convert_min = str(minimal["Date"]) # J'ai convertir mon pandas serie en chaine des caracteres
        string_convert_min = string_convert_min.split() # avec split, je divise ma chaine de caracteres en deux partie en choisisant l'espace vide comme indice de separation
        st.metric(label="Bad weekly purchase (Pcs)", value=db["Purchased Qty"].min(), delta= string_convert_min[0]) # Afficher le metric de la semaine avec moins d'achats
    
    # Graphic 
    data_weeks = px.line(db, x="Weeks", y="Purchased Qty", title="Purchase situation by weeks", text="Purchased Qty")
    data_weeks.update_traces(textposition = 'top center')
    st.plotly_chart(data_weeks)

    
    ##########################
    # Situation by years
    ####
    st.subheader("Purchase situation by Years", divider="rainbow")
    dataset_years = dataset.groupby("Years")["Purchased Qty"].sum().reset_index()
    data_years = px.line(dataset_years, x="Years", y="Purchased Qty", title="Situation purchase by years", text="Purchased Qty")
    data_years.update_traces(textposition = 'top center')
    st.plotly_chart(data_years)


    ##############################
    #### PREDICTION DES ACHATS ###
    ##############################
    
    st.header("Future Purchasing Forecasts", divider="rainbow")

    #############################
    ## 1- Predictions Global

    st.subheader("1. 📊Global Forecasts")

    dataset["Months"] = pd.to_datetime(dataset["Months"])
    st.success(f"{len(dataset)} lignes de données chargées avec succès ✅")

    # Regrouper les ventes par mois
    prediction_global = dataset.groupby("Months")["Purchased Qty"].sum().reset_index()
    prediction_global = prediction_global.rename(columns={"Months":"ds", "Purchased Qty":"y"})  # On renome la colonne "Months" en "ds" et celui de "Purchased Qty" en "y". Car Prophet ne reconnait que ces noms

    # Modèle Prophet
    purchases_global = Prophet()
    purchases_global.fit(prediction_global)

    # Prévision sur 3 mois
    predict_futur = purchases_global.make_future_dataframe(periods=3, freq='M') # On fait une prediction de 3 Mois en tenant compte de l'histoire des achats
    forecast_global = purchases_global.predict(predict_futur)


    # -------------------------------
    # 4️⃣ Affichage des données
    # -------------------------------
    
    with st.expander("📄 View raw forecast data "):
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
        yaxis_title ="Purchases Quantity",
        template ="plotly_white",
        
        plot_bgcolor = bg_color,     #'rgba(240,248,255,1)',  # 🔹 bleu très clair à l'intérieur du graphique
        paper_bgcolor = paper_color, #'rgba(255,255,255,1)', # 🔹 fond général blanc
    )

    st.plotly_chart(fig_global, use_container_width=True)


    #############################
    ## 2- Predictions Par Ville
    st.subheader("2. 📊City Forecasts")

    # Vérifier les colonnes requises
    required_cols = {"City", "Months", "Purchased Qty"}
    if not required_cols.issubset(dataset.columns):
        st.error(f"The file must contain the columns : {', '.join(required_cols)}")
        st.stop()
    
    # Préparer les données
    
    date_ville = dataset.groupby(["City", "Months"], as_index= False)["Purchased Qty"].sum() 
    date_ville = date_ville.rename(columns={"Months":"ds", "Purchased Qty":"y"})
    date_ville["ds"] = pd.to_datetime(date_ville["ds"])

    cities = sorted(dataset["City"].unique())
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
        city_data = date_ville[date_ville["City"] == city][["ds", "y"]]
        
        if len(city_data) < 5:
            st.warning(f"⚠️ Too little data for {city}, forecast ignored.")
            continue

        model_ville = Prophet()
        model_ville.fit(city_data)
        future_ville = model_ville.make_future_dataframe(periods=nb_mois, freq='M')
        forecast_ville = model_ville.predict(future_ville)
        forecast_ville["City"] = city
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
            .groupby("City")["yhat"]
            .sum()
            .reset_index()
            .sort_values(by="yhat", ascending=False)
        )

        st.text("🏆 Ranking of Cities by Purchasing Forecast")
        
        col3, col4 = st.columns([2, 1])
        with col3:
            fig_bar = px.bar(
                summary,
                x="City",
                y="yhat",
                title="Average purchasing forecasts by city",
                labels={"yhat": "Expected quantity", "City": "City"},
                text_auto=".0f",
                color="City"
            )
            fig_bar.update_layout(template="plotly_white")
            st.plotly_chart(fig_bar, use_container_width=True)

        with col4:
            st.dataframe(summary.rename(columns={"yhat": "Planned quantity"}), hide_index=True)

    else:
        st.info("⬆️ Import your Excel file to get started.")



    ##############################
    ## 3- Predictions Par Series
    st.subheader("3. 📊Series Forecasts")

    # use dataset
    # Creation d'une selecteur multiple
    #serie_data = date_frame["SERIES"].unique()
    select_serie_all = st.multiselect("Please can you select your serie here ? (One serie please ! ) : ", serie_data, default="SPARK")

    # Filtrage des donnees en fonction de la selection
    st_serie_choose_all = dataset[dataset["SERIES"].isin(select_serie_all)]
    st_serie_all = st_serie_choose_all.groupby("Months")["Purchased Qty"].sum().reset_index()
    st_serie_all = st_serie_all.rename(columns={"Months": "ds", "Purchased Qty": "y"})

    serie_forecast_all = Prophet()
    serie_forecast_all.fit(st_serie_all)

    serie_future_all = serie_forecast_all.make_future_dataframe(periods=3, freq='M')
    forecast_serie_all = serie_forecast_all.predict(serie_future_all)

    st.write(f"📊 Forecast Evolution by {select_serie_all}")
    fig_serie_preview_all = plot_plotly(serie_forecast_all, forecast_serie_all)
    fig_serie_preview_all.update_layout(
        title = "ST purchase series forcast ",
        xaxis_title = "Months",
        yaxis_title ="Purchases Quantity by series",
        template ="plotly_white",
        
        plot_bgcolor = bg_color,     #'rgba(240,248,255,1)',  # 🔹 bleu très clair à l'intérieur du graphique
        paper_bgcolor = paper_color, #'rgba(255,255,255,1)', # 🔹 fond général blanc
    )
    st.plotly_chart(fig_serie_preview_all, use_container_width=True)


    ##############################
    ## 4- Predictions Par Model
    st.subheader("4. 📊Models Forecasts")

    # use dataset
    # Creation d'une selecteur multiple
    models_data = date_frame["Products"].unique()
    select_models_all = st.multiselect("Please can you select your Model here ? (One Model please ! ) : ", models_data)

    # Filtrage des donnees en fonction de la selection
    st_models_choose_all = dataset[dataset["Products"].isin(select_models_all)]
    st_models_all = st_models_choose_all.groupby("Months")["Purchased Qty"].sum().reset_index()
    st_models_all = st_models_all.rename(columns={"Months": "ds", "Purchased Qty": "y"})

    model_forecast_all = Prophet()
    model_forecast_all.fit(st_models_all)

    model_future_all = model_forecast_all.make_future_dataframe(periods=3, freq='M')
    forecast_model_all = model_forecast_all.predict(model_future_all)

    st.write(f"📊 Forecast Evolution by {select_models_all}")
    fig_model_preview_all = plot_plotly(model_forecast_all, forecast_model_all)
    fig_model_preview_all.update_layout(
        title = "ST purchase model forcast ",
        xaxis_title = "Months",
        yaxis_title ="Purchases Quantity by model",
        template ="plotly_white",
        
        plot_bgcolor = bg_color,     #'rgba(240,248,255,1)',  # 🔹 bleu très clair à l'intérieur du graphique
        paper_bgcolor = paper_color, #'rgba(255,255,255,1)', # 🔹 fond général blanc
    )
    st.plotly_chart(fig_model_preview_all, use_container_width=True)


    st.markdown("___")
    ## FIN
    st.title("THANKS FOR YOUR ATTENTION !")
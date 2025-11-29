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

st.markdown("<h1 style='text-align: center; color: blue;'> TECNO FEATURE PHONE YEARLY REPORT"
"</h1>", unsafe_allow_html= True)
st.markdown("<br/>", unsafe_allow_html= True)
st.markdown("<br/>", unsafe_allow_html= True)
st.markdown("<h6 style='text-align: center; color: red;'> Welcome in our feature phone report. In this report we can found the datas of ST and A sub-dealers"
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

########################
# Load dataset
###

######################################################################################################################################
################################################### Partie 1 : ST REPORT #############################################################
######################################################################################################################################
file_st = st.file_uploader("📂 Insert your Excel file du 'ST FP Tecno' by pressing the 'Browse files' button", type=["xlsx","xls"])

if file_st is not None:

    dataset_full_st = pd.read_excel(file_st)

    # Traitement des valeurs null
   
    #dataset_st = dataset_full_st.dropna() # Supprimer les valeurs null
    dataset_st = dataset_full_st.dropna(subset="Purchased Qty") # Mettre les valeurs null à '0'

    # Creation des dates
    col1, col2 = st.columns(2)
    
    with col1:
        st.text("Select Date Range")
        start_date_st = st.date_input(label="Start Dates")

    with col2:
        st.text("Select Date Range")
        en_date_st = st.date_input(label="End Dates")

    # Provide a message for selected date range 
    st.success("you have choosen analytics from: "+str(start_date_st)+" to "+str(en_date_st))

    ##################
    # Filtre dates
    ###
    date_frame_st = dataset_st[(dataset_st["Date"]>=str(start_date_st)) & (dataset_st["Date"]<=str(en_date_st))]

    ## Situation general des achats
    st.subheader("ST General situation", divider="rainbow")
    
    #####################
    # 1- Yearly buy
    ######
    
    buy_st = dataset_full_st.groupby(["Years"], as_index= False)["Purchased Qty"].sum()
    fig_buy = px.line(buy_st, x="Years", y="Purchased Qty", text="Purchased Qty", title="Yearly purchase")
    fig_buy.update_traces(textposition = 'top center')
    st.plotly_chart(fig_buy)
    st.markdown("___")

    ###############
    # 2-Monthly
    ######
    
    # Create a list for each years
    years_selected = date_frame_st["Years"].unique()
    
    # Create the selector
    select_years = st.multiselect("Select your years", years_selected, default=[2024, 2025])

    # Data Filtrage 
    month_st = date_frame_st.groupby(["Years", "Months"], as_index= False)["Purchased Qty"].sum()
    filter = month_st[month_st["Years"].isin(select_years)]
    fig_month = px.line(filter, x="Months", y="Purchased Qty", text="Purchased Qty", title="Monthly purchase")
    fig_month.update_traces(textposition = 'top center')
    st.plotly_chart(fig_month)

    ######################################
    ## Situation semestriel des achats
    ######

    st.subheader("ST Weekly situation", divider="grey")
    
    col3, col4 = st.columns(2)

    with col3:
        annee = st.number_input("Write the old year")
        weeks = date_frame_st.groupby(["Years", "Weeks"], as_index= False)["Purchased Qty"].sum()
        filter_weeks = weeks[weeks["Years"]== annee]

        #----------------------------
        recupMois_old_years = date_frame_st.groupby(["Weeks", "Date", "Years"])["Purchased Qty"].sum().reset_index()
        filter_old_years = recupMois_old_years[recupMois_old_years["Years"]== annee]
        db = filter_old_years.groupby("Weeks")["Purchased Qty"].sum().reset_index() # Faire un group by sans index
        
        colv, colw = st.columns(2)
        with colv:
            maximal = filter_old_years.loc[filter_old_years["Purchased Qty"].idxmax()]
            string_convert_max = str(maximal["Date"]) # J'ai convertir mon pandas serie en chaine des caracteres
            string_convert_max = string_convert_max.split() # avec split, je divise ma chaine de caracteres en deux partie en choisisant l'espace vide comme indice de separation
            st.metric(label="Best weekly purchase (Pcs)", value=db["Purchased Qty"].max(), delta= string_convert_max[0])
            

        with colw:
            minimal = filter_old_years.loc[filter_old_years["Purchased Qty"].idxmin()]
            string_convert_min = str(minimal["Date"]) # J'ai convertir mon pandas serie en chaine des caracteres
            string_convert_min = string_convert_min.split() # avec split, je divise ma chaine de caracteres en deux partie en choisisant l'espace vide comme indice de separation
            st.metric(label="Bad weekly purchase (Pcs)", value=db["Purchased Qty"].min(), delta= string_convert_min[0]) # Afficher le metric de la semaine avec moins d'achats
            
        #----------------------------

        fig_week = px.line(filter_weeks, x="Weeks", y="Purchased Qty", title=f"Weekly {annee} purchase", text="Purchased Qty")
        fig_week.update_traces(textposition = 'top center')
        st.plotly_chart(fig_week)

    with col4 :
        weeks_enter = st.number_input("Write the year")
        weeks_y = date_frame_st.groupby(["Years", "Weeks"], as_index= False)["Purchased Qty"].sum()
        filter_weeks_y = weeks_y[weeks_y["Years"]== weeks_enter]

        #----------------------------
        recupMois_new_years = date_frame_st.groupby(["Weeks", "Date", "Years"])["Purchased Qty"].sum().reset_index()
        filter_new_years = recupMois_new_years[recupMois_new_years["Years"]== weeks_enter ]
        db_new = filter_new_years.groupby("Weeks")["Purchased Qty"].sum().reset_index() # Faire un group by sans index
        
        colx, coly = st.columns(2)
        with colx:
            maximal_new = filter_new_years.loc[filter_new_years["Purchased Qty"].idxmax()]
            string_convert_max_new = str(maximal_new["Date"]) # J'ai convertir mon pandas serie en chaine des caracteres
            string_convert_max_new = string_convert_max_new.split() # avec split, je divise ma chaine de caracteres en deux partie en choisisant l'espace vide comme indice de separation
            st.metric(label="Best weekly purchase (Pcs)", value=db_new["Purchased Qty"].max(), delta= string_convert_max_new[0])
            

        with coly:
            minimal_new = filter_new_years.loc[filter_new_years["Purchased Qty"].idxmin()]
            string_convert_min_new = str(minimal_new["Date"]) # J'ai convertir mon pandas serie en chaine des caracteres
            string_convert_min_new = string_convert_min_new.split() # avec split, je divise ma chaine de caracteres en deux partie en choisisant l'espace vide comme indice de separation
            st.metric(label="Bad weekly purchase (Pcs)", value=db_new["Purchased Qty"].min(), delta= string_convert_min_new[0]) # Afficher le metric de la semaine avec moins d'achats
            
        #----------------------------

        fig_week_y = px.line(filter_weeks_y, x="Weeks", y="Purchased Qty", title=f"Weekly {weeks_enter} purchase", text="Purchased Qty")
        fig_week_y.update_traces(textposition = 'top center')
        st.plotly_chart(fig_week_y)


    # Style the metric
    style_metric_cards(background_color="#636363", border_left_color="#a8ff78", border_color="#9FC1FF")

    ##################################
    ## Situation par modeles
    ####
    st.subheader("ST Models situation", divider="grey")
    
    # SERIES MODELS
    st.markdown("___")
    st.write(" Series by models ")

    col5, col6 = st.columns(2)

    with col5:
        #models_year = st.number_input("Put the old year")
        modeles = date_frame_st.groupby(["Years", "SERIES"], as_index= False)["Purchased Qty"].sum()
        filter_mdl = modeles[modeles["Years"] == annee]

        fig_mdl = px.bar(filter_mdl, x="SERIES", y="Purchased Qty", color="SERIES", text="Purchased Qty", title=f"Series models purchased for {annee}")
        fig_mdl.update_traces(textposition = 'outside')
        st.plotly_chart(fig_mdl)

        # Pie Chart
        fig_mdl_pie = go.Figure(data=[go.Pie(labels= filter_mdl["SERIES"], values= filter_mdl["Purchased Qty"], title=f"Series models proportion for {annee}", opacity= 0.5)])
        fig_mdl_pie.update_traces (hoverinfo='label+percent', textfont_size=15,textinfo= 'label+percent', pull= [0.05, 0, 0, 0, 0],marker_line=dict(color='#FFFFFF', width=2))
        st.plotly_chart(fig_mdl_pie)


    with col6 :
        
        mdl = date_frame_st.groupby(["Years", "SERIES"], as_index= False)["Purchased Qty"].sum()
        filter_model = mdl[mdl["Years"]== weeks_enter]

        fig_model = px.bar(filter_model, x="SERIES", y="Purchased Qty", color="SERIES", text="Purchased Qty", title=f"Series purchased for {weeks_enter}")
        fig_model.update_traces(textposition = 'outside')
        st.plotly_chart(fig_model)

        # Pie Chart
        fig_model_pie = go.Figure(data=[go.Pie(labels= filter_model["SERIES"], values= filter_model["Purchased Qty"], title=f"Series models proportion for {weeks_enter}", opacity= 0.5)])
        fig_model_pie.update_traces (hoverinfo='label+percent', textfont_size=15,textinfo= 'label+percent', pull= [0.05, 0, 0, 0, 0],marker_line=dict(color='#FFFFFF', width=2))
        st.plotly_chart(fig_model_pie)

    ### Models
    st.markdown("___")
    st.write(" Models ")


    col7, col8 = st.columns(2)

    with col7:
        #models_year = st.number_input("Put the old year")
        modeles = date_frame_st.groupby(["Years", "Products"], as_index= False)["Purchased Qty"].sum()
        filter_mdl = modeles[modeles["Years"] == annee]

        fig_mdl = px.bar(filter_mdl, x="Products", y="Purchased Qty", color="Products", text="Purchased Qty", title=f"Models purchased for {annee}")
        fig_mdl.update_traces(textposition = 'outside')
        st.plotly_chart(fig_mdl)

        # Pie Chart
        fig_mdl_pie = go.Figure(data=[go.Pie(labels= filter_mdl["Products"], values= filter_mdl["Purchased Qty"], title=f"Models proportion for {annee}", opacity= 0.5)])
        fig_mdl_pie.update_traces (hoverinfo='label+percent', textfont_size=15,textinfo= 'label+percent', pull= [0.05, 0, 0, 0, 0],marker_line=dict(color='#FFFFFF', width=2))
        st.plotly_chart(fig_mdl_pie)


    with col8 :
        
        mdl = date_frame_st.groupby(["Years", "Products"], as_index= False)["Purchased Qty"].sum()
        filter_model = mdl[mdl["Years"]== weeks_enter]

        fig_model = px.bar(filter_model, x="Products", y="Purchased Qty", color="Products", text="Purchased Qty", title=f"Models purchased for {weeks_enter}")
        fig_model.update_traces(textposition = 'outside')
        st.plotly_chart(fig_model)

        # Pie Chart
        fig_model_pie = go.Figure(data=[go.Pie(labels= filter_model["Products"], values= filter_model["Purchased Qty"], title=f"Models proportion for {weeks_enter}", opacity= 0.5)])
        fig_model_pie.update_traces (hoverinfo='label+percent', textfont_size=15,textinfo= 'label+percent', pull= [0.05, 0, 0, 0, 0],marker_line=dict(color='#FFFFFF', width=2))
        st.plotly_chart(fig_model_pie)



    ##################################
    ## ST Channel situation
    ####
    st.subheader("ST Channel situation", divider="grey")

    col9, col0 = st.columns(2)

    with col9 :
        city = date_frame_st.groupby(["Years", "City"], as_index= False)["Purchased Qty"].sum()
        city_years = city[city["Years"] == annee]
        fig_city = px.bar(city_years, x="City", y="Purchased Qty", text="Purchased Qty", title=f"Situation of Channel Kin and Lushi for {annee}", color="City")
        fig_city.update_traces(textposition = 'outside')
        st.plotly_chart(fig_city)

        st.markdown("___")
        # Pie Chart
        fig_city_pie = go.Figure(data=[go.Pie(labels= city_years["City"], values= city_years["Purchased Qty"], title=f"Channel proportion for {annee}", opacity= 0.5)])
        fig_city_pie.update_traces (hoverinfo='label+percent', textfont_size=15,textinfo= 'label+percent', pull= [0.05, 0, 0, 0, 0],marker_line=dict(color='#FFFFFF', width=2))
        st.plotly_chart(fig_city_pie)
        

    with col0 :
        #channel = date_frame_st.groupby(["Years", "City"], as_index= False)["Purchased Qty"].sum()
        channel = city[city["Years"] == weeks_enter]
        fig_channel = px.bar(channel, x="City", y="Purchased Qty", text="Purchased Qty", title=f"Situation of Channel Kin and Lushi for {weeks_enter}", color="City")
        fig_channel.update_traces(textposition = 'outside')
        st.plotly_chart(fig_channel)

        st.markdown("___")
        # Pie Chart
        fig_channel_pie = go.Figure(data=[go.Pie(labels= channel["City"], values= channel["Purchased Qty"], title=f"Channel proportion for {weeks_enter}", opacity= 0.5)])
        fig_channel_pie.update_traces (hoverinfo='label+percent', textfont_size=15,textinfo= 'label+percent', pull= [0.05, 0, 0, 0, 0],marker_line=dict(color='#FFFFFF', width=2))
        st.plotly_chart(fig_channel_pie)



    ##############################
    #### PREDICTION DES ACHATS ###
    ##############################

    st.header("Future Purchasing Forecasts", divider="rainbow")

    #############################
    ## 1- Predictions Global

    st.subheader("1. 📊Global Forecasts")

    dataset_st["Months"] = pd.to_datetime(dataset_st["Months"])
    st.success(f"{len(dataset_st)} lignes de données chargées avec succès ✅")

    # Regrouper les ventes par mois
    prediction_global = dataset_st.groupby("Months")["Purchased Qty"].sum().reset_index()
    prediction_global = prediction_global.rename(columns={"Months":"ds", "Purchased Qty":"y"})  # On renome la colonne "Months" en "ds" et celui de "Purchased Qty" en "y". Car Prophet ne reconnait que ces noms

    # Modèle Prophet
    purchases_global = Prophet()
    purchases_global.fit(prediction_global)

    # Prévision sur 3 mois
    predict_futur = purchases_global.make_future_dataframe(periods=12, freq='M') # On fait une prediction de 3 Mois en tenant compte de l'histoire des achats
    forecast_global = purchases_global.predict(predict_futur)

    # -------------------------------
    # 4️⃣ Affichage des données
    # -------------------------------
    
    with st.expander("📄 View raw forecast data"):
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
    if not required_cols.issubset(dataset_st.columns):
        st.error(f"The file must contain the columns : {', '.join(required_cols)}")
        st.stop()
    
    # Préparer les données
    
    date_ville = dataset_st.groupby(["City", "Months"], as_index= False)["Purchased Qty"].sum() 
    date_ville = date_ville.rename(columns={"Months":"ds", "Purchased Qty":"y"})
    date_ville["ds"] = pd.to_datetime(date_ville["ds"])

    cities = sorted(dataset_st["City"].unique())
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
    ### 3- Predictions par Series
    ####
    
    st.subheader("3. 📊Series Forecasts")

    # Vérifier les colonnes requises
    required_cols_series = {"SERIES", "Months", "Purchased Qty"}
    if not required_cols_series.issubset(dataset_st.columns):
        st.error(f"This file must contain the columns : {', '.join(required_cols_series)}")
        st.stop()
    
    # Préparer les données
    
    date_series = dataset_st.groupby(["SERIES", "Months"], as_index= False)["Purchased Qty"].sum() 
    date_series = date_series.rename(columns={"Months":"ds", "Purchased Qty":"y"})
    date_series["ds"] = pd.to_datetime(date_series["ds"])

    series = sorted(dataset_st["SERIES"].unique())
    st.success(f"✅ {len(series)} series detected : {', '.join(series)}")

    # -------------------------------
    # Paramètres utilisateur
    # -------------------------------
    #nb_mois = st.slider("Number of months to predict", 1, 12, 3)  # 3 mois par défaut

    col11, col22 = st.columns(2)
    predictions_series = []

    # -------------------------------
    # Prévision par series
    # -------------------------------
    st.header("📈 Forecasts by Series")

    for i, series in enumerate(series):
        series_data = date_series[date_series["City"] == series][["ds", "y"]]
        
        if len(series_data) < 5:
            st.warning(f"⚠️ Too little data for {series}, forecast ignored !")
            continue

        model_series = Prophet()
        model_series.fit(city_data)
        future_series = model_series.make_future_dataframe(periods=nb_mois, freq='M')
        forecast_series = model_series.predict(future_series)
        forecast_series["City"] = city
        predictions_series.append(forecast_series)

        # Graphique interactif
        fig_series = go.Figure()
        fig_series.add_trace(go.Scatter(x=series_data["ds"], y=series_data["y"], mode="markers+lines", name="Historique"))
        fig_series.add_trace(go.Scatter(x=forecast_series["ds"], y=forecast_series["yhat"], mode="lines", name="Prévision"))
        fig.update_layout(title=f"📍 {series}", xaxis_title="Date", yaxis_title="Quantité", template="plotly_white")

        # Affichage côte à côte
        if i % 2 == 0:
            with col1:
                st.plotly_chart(fig_series, use_container_width=True)
        else:
            with col2:
                st.plotly_chart(fig_series, use_container_width=True)

    # -------------------------------
    # 4️⃣ Comparatif entre series
    # -------------------------------
    if predictions_series:
        predictions_series = pd.concat(predictions_series)

        # Dernière date prévue = prévision la plus récente
        latest_date_series = predictions_series["ds"].max()
        summary = (
            predictions_series[predictions_series["ds"] == latest_date_series]
            .groupby("Series")["yhat"]
            .sum()
            .reset_index()
            .sort_values(by="yhat", ascending=False)
        )

        st.text("🏆 Ranking of Series by Purchasing Forecast")
        
        col3, col4 = st.columns([2, 1])
        with col3:
            fig_bar_series = px.bar(
                summary,
                x="Series",
                y="yhat",
                title="Average purchasing forecasts by Series",
                labels={"yhat": "Expected quantity", "Series": "Series"},
                text_auto=".0f",
                color="Series"
            )
            fig_bar_series.update_layout(template="plotly_white")
            st.plotly_chart(fig_bar_series, use_container_width=True)

        with col4:
            st.dataframe(summary.rename(columns={"yhat": "Planned quantity"}), hide_index=True)

    else:
        st.info("⬆️ Import your Excel file to get started.")


    ##############################
    ## 4- Predictions Par Modeles
    st.subheader("4. 📊Models Forecasts")

    # use dataset
    # Creation d'une selecteur multiple
    models_data = dataset_st["Products"].unique()
    select_models_all = st.multiselect("Please can you select your model here ? (One model please ! ) : ", models_data, default="T101")

    # Filtrage des donnees en fonction de la selection
    st_models_choose_all = dataset_st[dataset_st["Products"].isin(select_models_all)]
    st_models_all = st_models_choose_all.groupby("Months")["Purchased Qty"].sum().reset_index()
    st_models_all = st_models_all.rename(columns={"Months": "ds", "Purchased Qty": "y"})

    model_forecast_all = Prophet()
    model_forecast_all.fit(st_models_all)

    model_future_all = model_forecast_all.make_future_dataframe(periods=12, freq='M')
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



##########################################################################################################################################################
########################################################### Partie 2 : SD REPORT  ########################################################################
##########################################################################################################################################################
file_sd = st.file_uploader("📂 Insert your Excel file of 'SD FP Tecno' by pressing the 'Browse files' button", type=["xlsx","xls"])

if file_sd is not None:

    dataset_full_sd = pd.read_excel(file_sd)

    # Traitement des valeurs null
   
    dataset_sd = dataset_full_sd.dropna(subset="Purchases Qty (Pcs)") # Supprimer les valeurs null

    # Creation des dates
    col11, col12 = st.columns(2)
    
    with col11:
        st.text("Choose the Date Range")
        start_date_sd = st.date_input(label="First Dates")

    with col12:
        st.text("Choose the Date Range")
        en_date_sd = st.date_input(label="Last Dates")

    # Provide a message for selected date range 
    st.success("Here is your choose analytics from: "+str(start_date_sd)+" to "+str(en_date_sd))

    ##################
    # Filtre dates
    ###
    date_frame_sd = dataset_sd[(dataset_sd["Date"]>=str(start_date_sd)) & (dataset_sd["Date"]<=str(en_date_sd))]

    #################################
    ## Situation general des achats
    ######
    st.subheader("SD General situation", divider="rainbow")
    
    sd_years = dataset_full_sd.groupby("Years", as_index= False)["Purchases Qty (Pcs)"].sum()
    fig_years = px.line(sd_years, x="Years", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title="Sub-dealers Situation purchase by years")
    fig_years.update_traces(textposition = 'top center')
    st.plotly_chart(fig_years)

    st.subheader("SD Monthly situation", divider="blue")

    cola, colb = st.columns(2)

    with cola :
        sd_month = date_frame_sd.groupby(["Years", "Date"], as_index= False)["Purchases Qty (Pcs)"].sum()
        filtre_mois = sd_month[sd_month["Years"] == annee]
        fig_month = px.line(filtre_mois, x="Date", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Sub-dealers purchase Situation by Month for year {annee}")
        fig_month.update_traces(textposition = 'top center')
        st.plotly_chart(fig_month)

    with colb :
        sd_month_2 = date_frame_sd.groupby(["Years", "Date"], as_index= False)["Purchases Qty (Pcs)"].sum()
        filtre_mois_2 = sd_month[sd_month["Years"] == weeks_enter]
        fig_month_2 = px.line(filtre_mois_2, x="Date", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Sub-dealers purchase Situation by Month for year {weeks_enter}")
        fig_month_2.update_traces(textposition = 'top center')
        st.plotly_chart(fig_month_2)
    
    ################################
    ## SD situation by region
    ########

    st.subheader("SD situation by region", divider="blue")

    colc, cold = st.columns(2)

    with colc:
        region = date_frame_sd.groupby(["Years", "Cities"], as_index= False)["Purchases Qty (Pcs)"].sum()
        filtre_region = region[region["Years"] == annee]
        fig_region = px.bar(filtre_region, x="Cities", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Sub-dealers purchase Situation by region for year {annee}", color="Cities")
        fig_region.update_traces(textposition = 'outside')
        st.plotly_chart(fig_region)

    with cold:
        city = date_frame_sd.groupby(["Years", "Cities"], as_index= False)["Purchases Qty (Pcs)"].sum()
        filtre_city = city[city["Years"] == weeks_enter]
        fig_city = px.bar(filtre_city, x="Cities", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Sub-dealers purchase Situation by region for year {weeks_enter}", color="Cities")
        fig_city.update_traces(textposition = 'outside')
        st.plotly_chart(fig_city)
        
    ##########################
    ## SD model situation
    #####

    st.subheader("SD models situation", divider="blue")

    cole, colf = st.columns(2)

    with cole:
        region_md = date_frame_sd.groupby(["Years", "Products"], as_index= False)["Purchases Qty (Pcs)"].sum()
        filtre_region_md = region_md[region_md["Years"] == annee]
        fig_region_md = px.bar(filtre_region_md, x="Products", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Sub-dealers purchase Situation by models for year {annee}", color="Products")
        fig_region_md.update_traces(textposition = 'outside')
        st.plotly_chart(fig_region_md)

    with colf:
        city_md = date_frame_sd.groupby(["Years", "Products"], as_index= False)["Purchases Qty (Pcs)"].sum()
        filtre_city_md = city_md[city_md["Years"] == weeks_enter]
        fig_city_md = px.bar(filtre_city_md, x="Products", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Sub-dealers purchase Situation by models for year {weeks_enter}", color="Products")
        fig_city_md.update_traces(textposition = 'outside')
        st.plotly_chart(fig_city_md)

    #########################
    ## SD model situation
    #######

    st.subheader("SD Target and Achievement", divider="blue")

    SD_view_2025 = dataset_full_sd[dataset_full_sd["Years"] == 2025]
    SD_target_2025 = SD_view_2025.groupby("Date", as_index= False)["Purchases Qty (Pcs)"].sum()

    def creer_target_sd_mois(SD_target_2025):
        if SD_target_2025["Date"].nunique() == 1:
            SD_target_2025["Target"] = 9600
            return SD_target_2025["Target"]
        
        elif SD_target_2025["Date"].nunique() == 2:
            SD_target_2025["Target"] = [9600, 9600]
            return SD_target_2025["Target"]
        
        elif SD_target_2025["Date"].nunique() == 3:  
            SD_target_2025["Target"] = [9600, 9600, 9600] # Creation d'une colonne target
            return SD_target_2025["Target"]
        
        elif SD_target_2025["Date"].nunique() == 4:
            SD_target_2025["Target"] = [9600, 9600, 9600, 8330]
            return SD_target_2025["Target"]
        
        elif SD_target_2025["Date"].nunique() == 5:
            SD_target_2025["Target"] = [9600, 9600, 9600, 8330, 9335]
            return SD_target_2025["Target"]
        
        elif SD_target_2025["Date"].nunique() == 6:
            SD_target_2025["Target"] = [9600, 9600, 9600, 8330, 9335, 9520]
            return SD_target_2025["Target"]
        
        elif SD_target_2025["Date"].nunique() == 7:
            SD_target_2025["Target"] = [9600, 9600, 9600, 8330, 9335, 9520, 9110]
            return SD_target_2025["Target"]
        
        elif SD_target_2025["Date"].nunique() == 8:
            SD_target_2025["Target"] = [9600, 9600, 9600, 8330, 9335, 9520, 9110, 9175]
            return SD_target_2025["Target"]
        
        elif SD_target_2025["Date"].nunique() == 9:
            SD_target_2025["Target"] = [9600, 9600, 9600, 8330, 9335, 9520, 9110, 9175, 9200]
            return SD_target_2025["Target"]
        
        elif SD_target_2025["Date"].nunique() == 10:
            SD_target_2025["Target"] = [9600, 9600, 9600, 8330, 9335, 9520, 9110, 9175, 9200, 9500]
            return SD_target_2025["Target"]
        
        elif SD_target_2025["Date"].nunique() == 11:
            SD_target_2025["Target"] = [9600, 9600, 9600, 8330, 9335, 9520, 9110, 9175, 9200, 9500, 10465]
            return SD_target_2025["Target"]
        
        elif SD_target_2025["Date"].nunique() == 12:
            SD_target_2025["Target"] = [9600, 9600, 9600, 8330, 9335, 9520, 9110, 9175, 9200, 9500, 10465, 11375]
            return SD_target_2025["Target"]
        
        else:
            return None  # ou gérer autrement si plusieurs mois
        
    sd_target = creer_target_sd_mois(SD_target_2025)


    # Creation graphic combiner (bar and line)
    #"""
    SD_fig_cmb = go.Figure()

    #-- Barre pour l'achievment ---
    SD_fig_cmb.add_trace(go.Bar(
        x = SD_target_2025["Date"],
        y = SD_target_2025["Purchases Qty (Pcs)"],
        name = "Achievment",
        text = SD_target_2025["Purchases Qty (Pcs)"],
        textposition= "auto", # il y a 'auto' 'outside' 'inside'
        marker_color = "skyblue"
    ))

    #-- Ligne pour le target --
    SD_fig_cmb.add_trace(go.Scatter(
        x = SD_target_2025["Date"],
        y = sd_target,
        name ="Target (Pcs)",
        mode = 'lines+text+markers',
        text = SD_target_2025["Target"],
        textposition= "top center",
        line = dict(color = "orange", width = 3)
    ))
    #"""

    # Mettre a jour la mise en page
    #"""
    SD_fig_cmb.update_layout(
        title = "Sub-dealers > Target and Achievment for 2025", 
        yaxis = dict(title= "Purchases Qty (Pcs)"),
        yaxis2 = dict(title= "Buy", overlaying = 'y', side = 'right'), 
        xaxis = dict(title = "Month"),
        legend = dict(x=0.1, y=1.1, orientation = 'h'), 
        bargap = 0.3
    )

    st.plotly_chart(SD_fig_cmb)

    #####################
    ## SD Performance
    ######
    
    st.subheader("SD Performance", divider="blue")

    colg, colh = st.columns(2)

    with colg:
        subDealer = date_frame_sd.groupby(["Years", "Customers Name"], as_index= False)["Purchases Qty (Pcs)"].sum()
        filtre_subDealer = subDealer[subDealer["Years"] == annee]
        fig_subDealer = px.bar(filtre_subDealer, x="Customers Name", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Sub-dealers purchase Situation for year {annee}", color="Customers Name")
        fig_subDealer.update_traces(textposition = 'outside')
        st.plotly_chart(fig_subDealer)

    with colh:
        sd = date_frame_sd.groupby(["Years", "Customers Name"], as_index= False)["Purchases Qty (Pcs)"].sum()
        filtre_sd = sd[sd["Years"] == weeks_enter]
        fig_sd = px.bar(filtre_sd, x="Customers Name", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Sub-dealers purchase Situation for year {weeks_enter}", color="Customers Name")
        fig_sd.update_traces(textposition = 'outside')
        st.plotly_chart(fig_sd)
    
    ###
    # Comparer les achats par client

    clients = date_frame_sd["Customers Name"].unique()
    
    ###
    # Select customer
    select_sdx =  st.selectbox("Choose your sub-dealer", clients)

    coli, colj = st.columns(2)

    with coli :
        sub_dealerx = date_frame_sd.groupby(["Years", "Customers Name", "Products"], as_index= False)["Purchases Qty (Pcs)"].sum()
        filtre_sub_dealer = sub_dealerx[sub_dealerx["Years"] == annee] # Definir l'annee
        
        filter_client =  filtre_sub_dealer[filtre_sub_dealer["Customers Name"] == select_sdx]
        
        fig_sub_dealer = px.bar(filter_client, x="Products", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Purchase situation of {select_sdx} for year {annee}", color="Products")
        fig_sub_dealer.update_traces(textposition = 'outside')
        st.plotly_chart(fig_sub_dealer)

    with colj :
        sub_dealer = date_frame_sd.groupby(["Years", "Customers Name", "Products"], as_index= False)["Purchases Qty (Pcs)"].sum()
        filtre_sub_client = sub_dealer[sub_dealer["Years"] == weeks_enter] # Definir l'annee
        
        filter_custo =  filtre_sub_client[filtre_sub_client["Customers Name"] == select_sdx]
        
        fig_sub_custo = px.bar(filter_custo, x="Products", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Purchase situation of {select_sdx} for year {weeks_enter}", color="Products")
        fig_sub_custo.update_traces(textposition = 'outside')
        st.plotly_chart(fig_sub_custo)


    ##############################
    #### PREDICTION DES ACHATS ###
    #############################
    
    st.header("FUTURE PURCHASING FORECASTS", divider="rainbow")

    #############################
    ## 1- Predictions Global

    st.subheader("1. 📊Global Forecasts")

    dataset_sd["Date"] = pd.to_datetime(dataset_sd["Date"])
    st.success(f"{len(dataset_sd)} lignes de données chargées avec succès ✅")

    # Regrouper les ventes par mois
    prediction_global = dataset_sd.groupby("Date")["Purchases Qty (Pcs)"].sum().reset_index()
    prediction_global = prediction_global.rename(columns={"Date":"ds", "Purchases Qty (Pcs)":"y"})  # On renome la colonne "Months" en "ds" et celui de "Purchased Qty" en "y". Car Prophet ne reconnait que ces noms

    # Modèle Prophet
    purchases_global = Prophet()
    purchases_global.fit(prediction_global)

    # Prévision sur 3 mois
    predict_futur = purchases_global.make_future_dataframe(periods=12, freq='M') # On fait une prediction de 3 Mois en tenant compte de l'histoire des achats
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
    select_models_all = st.multiselect("Please can you select your model here : ?", models_data, default="T101")

    # Filtrage des donnees en fonction de la selection
    sd_models_choose_all = dataset_sd[dataset_sd["Products"].isin(select_models_all)]
    sd_models_all = sd_models_choose_all.groupby("Date")["Purchases Qty (Pcs)"].sum().reset_index()
    sd_models_all = sd_models_all.rename(columns={"Date": "ds", "Purchases Qty (Pcs)": "y"})

    model_forecast_all = Prophet()
    model_forecast_all.fit(sd_models_all)

    model_future_all = model_forecast_all.make_future_dataframe(periods=12, freq='M')
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
    if not required_cols.issubset(dataset_sd.columns):
        st.error(f"The file must contain the columns : {', '.join(required_cols)}")
        st.stop()
    
    # Préparer les données
    
    date_ville = dataset_sd.groupby(["Cities", "Date"], as_index= False)["Purchases Qty (Pcs)"].sum() 
    date_ville = date_ville.rename(columns={"Date":"ds", "Purchases Qty (Pcs)":"y"})
    date_ville["ds"] = pd.to_datetime(date_ville["ds"])

    cities = sorted(dataset_sd["Cities"].unique())
    st.success(f"✅ {len(cities)} cities detected : {', '.join(cities)}")

    # -------------------------------
    # Paramètres utilisateur
    # -------------------------------
    nb_mois = st.slider("Number of months to predict", 1, 3, 12)  # 3 mois par défaut

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





st.markdown("___")

        


    
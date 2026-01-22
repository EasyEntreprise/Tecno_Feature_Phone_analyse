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

st.markdown("<h1 style='text-align: center; color: blue;'> TECNO BUSINESS YEARLY REPORT"
"</h1>", unsafe_allow_html= True)
st.markdown("<br/>", unsafe_allow_html= True)
st.markdown("<br/>", unsafe_allow_html= True)
st.markdown("<h6 style='text-align: center; color: red;'> Welcome in our yearly report. In this report we can found the datas of ST and A sub-dealers"
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

bg_color = st.sidebar.color_picker("Background", "#f0f8ff")
paper_color = st.sidebar.color_picker("Background general", "#ffffff")

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


st.markdown("")
st.markdown("")
######################################################################################################################################
################################################### Partie 1 : FP-ST REPORT #############################################################
######################################################################################################################################
st.header("Party One : FEATURE PHONE ST REPORT")
file_st_fp = st.file_uploader("📂 Insert your Excel file du 'ST FP Tecno' by pressing the 'Browse files' button", type=["xlsx","xls", "csv"])

if file_st_fp is not None:

    #dataset_full_st = pd.read_excel(file_st)
    dataset_full_st = read_file(file_st_fp)

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
    
    buy_st = dataset_st.groupby(["Years"], as_index= False)["Purchased Qty"].sum()
    fig_buy = px.line(buy_st, x="Years", y="Purchased Qty", text="Purchased Qty", title="Yearly purchase")
    fig_buy.update_traces(textposition = 'top center')
    st.plotly_chart(fig_buy)
    st.markdown("___")

    ###############
    # 2-Monthly
    ######
    
    # Create a list for each years
    years_selected = dataset_st["Years"].unique()
    
    # Create the selector
    select_years = st.multiselect("Select your years", years_selected) # default=[2024, 2025]

    # Data Filtrage 
    month_st = dataset_st.groupby(["Years", "Months"], as_index= False)["Purchased Qty"].sum()
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
    
    col5, col6 = st.columns(2)

    with col5:
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


    with col6 :
        
        mdl = date_frame_st.groupby(["Years", "Products"], as_index= False)["Purchased Qty"].sum()
        filter_model = mdl[mdl["Years"]== weeks_enter]

        fig_model = px.bar(filter_model, x="Products", y="Purchased Qty", color="Products", text="Purchased Qty", title=f"Models purchased for {weeks_enter}")
        fig_model.update_traces(textposition = 'outside')
        st.plotly_chart(fig_model)

        # Pie Chart
        fig_model_pie = go.Figure(data=[go.Pie(labels= filter_model["Products"], values= filter_model["Purchased Qty"], title=f"Models proportion for {weeks_enter}", opacity= 0.5)])
        fig_model_pie.update_traces (hoverinfo='label+percent', textfont_size=15,textinfo= 'label+percent', pull= [0.05, 0, 0, 0, 0],marker_line=dict(color='#FFFFFF', width=2))
        st.plotly_chart(fig_model_pie)

    ############################
    ## Histogram prices 
    ####

    col7, col8 = st.columns(2)

    with col7:
        # Create Histogram for prices

        date_groupby = date_frame_st.groupby(["Years", "Products", "Prices ($)"], as_index= False)["Purchased Qty"].sum()
        prices_filter = date_groupby[date_groupby["Years"] == weeks_enter]

        # Create a histogram
        fig_hist = px.histogram(prices_filter, x="Prices ($)", title="Distribution models on prices", hover_data=["Purchased Qty"])
        st.plotly_chart(fig_hist)


    with col8 :
        key_model = date_frame_st.groupby(["Years", "Products","Prices ($)"], as_index= False)["Purchased Qty"].sum()
        key_filter = key_model[key_model["Years"] == weeks_enter]

        fig_key = px.bar(key_filter, x="Products", y="Prices ($)", text="Prices ($)", title="Graphic Models and Prices", color="Products")
        fig_key.update_traces(textposition = 'outside')
        st.plotly_chart(fig_key)

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


    ##################################
    ## Target & Achievment
    ####   
    st.subheader("Target & Achievment", divider="grey")

    view_2025 = dataset_full_st[dataset_full_st["Years"] == 2025]
    target_2025 = view_2025.groupby("Months", as_index= False)["Purchased Qty"].sum()

    def creer_target_si_un_mois(target_2025):
        if target_2025["Months"].nunique() == 1:
            target_2025["Target"] = 16000
            return target_2025["Target"]
        
        elif target_2025["Months"].nunique() == 2:
            target_2025["Target"] = [16000, 16000]
            return target_2025["Target"]
        elif target_2025["Months"].nunique() == 3:  
            target_2025["Target"] = [16000, 16000, 16000] # Creation d'une colonne target
            return target_2025["Target"]
        elif target_2025["Months"].nunique() == 4:
            target_2025["Target"] = [16000, 16000, 16000, 17000]
            return target_2025["Target"]
        elif target_2025["Months"].nunique() == 5:
            target_2025["Target"] = [16000, 16000, 16000, 17000, 17000]
            return target_2025["Target"]
        elif target_2025["Months"].nunique() == 6:
            target_2025["Target"] = [16000, 16000, 16000, 17000, 17000, 11900] # [16000, 16000, 16000, 17000, 17000, 17000]
            return target_2025["Target"]
        elif target_2025["Months"].nunique() == 7:
            target_2025["Target"] = [16000, 16000, 16000, 17000, 17000, 11900, 13300] # [16000, 16000, 16000, 17000, 17000, 17000, 18500]
            return target_2025["Target"]
        elif target_2025["Months"].nunique() == 8:
            target_2025["Target"] = [16000, 16000, 16000, 17000, 17000, 11900, 13300, 13300] # [16000, 16000, 16000, 17000, 17000, 17000, 18500, 18500]
            return target_2025["Target"]
        elif target_2025["Months"].nunique() == 9:
            target_2025["Target"] = [16000, 16000, 16000, 17000, 17000, 11900, 13300, 13300, 14700] # [16000, 16000, 16000, 17000, 17000, 17000, 18500, 18500, 19000]
            return target_2025["Target"]
        elif target_2025["Months"].nunique() == 10:
            target_2025["Target"] = [16000, 16000, 16000, 17000, 17000, 11900, 13300, 13300, 14700, 14700] # [16000, 16000, 16000, 17000, 17000, 17000, 18500, 18500, 19000, 20000]
            return target_2025["Target"]
        elif target_2025["Months"].nunique() == 11:
            target_2025["Target"] = [16000, 16000, 16000, 17000, 17000, 11900, 13300, 13300, 14700, 14700, 16100] # [16000, 16000, 16000, 17000, 17000, 17000, 18500, 18500, 19000, 20000, 20000]
            return target_2025["Target"]
        elif target_2025["Months"].nunique() == 12:
            target_2025["Target"] = [16000, 16000, 16000, 17000, 17000, 11900, 13300, 13300, 14700, 14700, 16100, 17500] # [16000, 16000, 16000, 17000, 17000, 17000, 18500, 18500, 19000, 20000, 20000, 20000]
            return target_2025["Target"]
        else:
            return None  # ou gérer autrement si plusieurs mois
        
    target = creer_target_si_un_mois(target_2025)

    # Creation graphic combiner (bar and line)
    #"""
    fig_cmb = go.Figure()

    #-- Barre pour l'achievment ---
    fig_cmb.add_trace(go.Bar(
        x = target_2025["Months"],
        y = target_2025["Purchased Qty"],
        name = "Achievment",
        text = target_2025["Purchased Qty"],
        textposition= "auto", # il y a 'auto' 'outside' 'inside'
        marker_color = "skyblue"
    ))

    #-- Ligne pour le target --
    fig_cmb.add_trace(go.Scatter(
        x = target_2025["Months"],
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
        title = "Target and Achievment for 2025", 
        yaxis = dict(title= "Purchase (Pcs)"),
        yaxis2 = dict(title= "Buy", overlaying = 'y', side = 'right'), 
        xaxis = dict(title = "Month"),
        legend = dict(x=0.1, y=1.1, orientation = 'h'), 
        bargap = 0.3
    )

    st.plotly_chart(fig_cmb)
    #"""

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

    #bg_color = st.sidebar.color_picker("Background", "#f0f8ff", key="first")
    #paper_color = st.sidebar.color_picker("Background general", "#ffffff", key="second")

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
    ## 3- Predictions Par Modeles
    st.subheader("3. 📊Models Forecasts")

    # use dataset
    # Creation d'une selecteur multiple
    models_data = dataset_st["Products"].unique()
    select_models_all = st.multiselect("Please can you select your model here ? (One model please ! ) : ", models_data)

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


st.markdown("___")
st.markdown("")
st.markdown("")
##########################################################################################################################################################
########################################################### Partie 2 : FP-SD REPORT  ########################################################################
##########################################################################################################################################################
st.header("Party Two : FEATURE PHONE SUB-DEALERS REPORT")

file_sd_fp = st.file_uploader("📂 Insert your Excel file of 'SD FP Tecno' by pressing the 'Browse files' button", type=["xlsx","xls", "csv"])

if file_sd_fp is not None:

    #dataset_full_sd = pd.read_excel(file_sd)
    dataset_full_sd = read_file(file_sd_fp)

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
    
    sd_years = dataset_sd.groupby("Years", as_index= False)["Purchases Qty (Pcs)"].sum()
    fig_years = px.line(sd_years, x="Years", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title="Sub-dealers Situation purchase by years")
    fig_years.update_traces(textposition = 'top center')
    st.plotly_chart(fig_years)

    st.subheader("SD Monthly situation", divider="blue")

    cola, colb = st.columns(2)

    with cola :

        annee_x = st.number_input("Write the year you want to analyze")
        sd_month = date_frame_sd.groupby(["Years", "Date"], as_index= False)["Purchases Qty (Pcs)"].sum()
        filtre_mois = sd_month[sd_month["Years"] == annee_x]
        fig_month = px.line(filtre_mois, x="Date", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Sub-dealers purchase Situation by Month for year {annee_x}")
        fig_month.update_traces(textposition = 'top center')
        st.plotly_chart(fig_month)

    with colb :

        weeks_enter_x = st.number_input("Write the year you wanna analyze")
        sd_month_2 = date_frame_sd.groupby(["Years", "Date"], as_index= False)["Purchases Qty (Pcs)"].sum()
        filtre_mois_2 = sd_month[sd_month["Years"] == weeks_enter_x]
        fig_month_2 = px.line(filtre_mois_2, x="Date", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Sub-dealers purchase Situation by Month for year {weeks_enter_x}")
        fig_month_2.update_traces(textposition = 'top center')
        st.plotly_chart(fig_month_2)
    
    ################################
    ## SD situation by region
    ########

    st.subheader("SD situation by region", divider="blue")


    colc, cold = st.columns(2)

    with colc:
        region = date_frame_sd.groupby(["Years", "Cities"], as_index= False)["Purchases Qty (Pcs)"].sum()
        filtre_region = region[region["Years"] == annee_x]
        fig_region = px.bar(filtre_region, x="Cities", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Sub-dealers purchase Situation by region for year {annee_x}", color="Cities")
        fig_region.update_traces(textposition = 'outside')
        st.plotly_chart(fig_region)

        st.markdown("___")


    with cold:
        city = date_frame_sd.groupby(["Years", "Cities"], as_index= False)["Purchases Qty (Pcs)"].sum()
        filtre_city = city[city["Years"] == weeks_enter_x]
        fig_city = px.bar(filtre_city, x="Cities", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Sub-dealers purchase Situation by region for year {weeks_enter_x}", color="Cities")
        fig_city.update_traces(textposition = 'outside')
        st.plotly_chart(fig_city)

        st.markdown("___")

    sd_2 = dataset_sd["Cities"].unique()

    city_x = ["All cities"] + sorted(dataset_sd["Cities"].dropna().unique().tolist())
    selector = st.selectbox("Choose your City :", city_x)
    #sd_selector  = dataset_sd[dataset_sd["Cities"] == selector]

    if selector == "All cities":
        sd_selector = dataset_sd

    else:
        sd_selector = dataset_sd[dataset_sd["Cities"] == selector]

    colce, colde = st.columns(2)

    with colce:

        sd_3 = sd_selector[sd_selector["Years"] == annee_x]
        sd_groupby = sd_3.groupby(["Customers Name","Years"], as_index= False)["Purchases Qty (Pcs)"].sum()
        
        fig_groupby = px.bar(sd_groupby, x="Customers Name", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Sub-dealers purchase Situation by region for year {annee_x}", color="Customers Name")
        fig_groupby.update_traces(textposition = 'outside')
        st.plotly_chart(fig_groupby)

        st.markdown("___")
                             
        fig_groupby_pie = go.Figure(data=[go.Pie(labels= sd_groupby["Customers Name"], values= sd_groupby["Purchases Qty (Pcs)"], title=f"Sub-dealers purchase Situation by region for year {annee_x}", opacity= 0.5)])
        fig_groupby_pie.update_traces (hoverinfo='label+percent', textfont_size=15,textinfo= 'label+percent', pull= [0.05, 0, 0, 0, 0],marker_line=dict(color='#FFFFFF', width=2))
        st.plotly_chart(fig_groupby_pie)

        st.markdown("___")

    with colde:

        sd_4 = sd_selector[sd_selector["Years"] == weeks_enter_x]
        sd_groupby_2 = sd_4.groupby(["Customers Name","Years"], as_index= False)["Purchases Qty (Pcs)"].sum()
        
        fig_groupby_2 = px.bar(sd_groupby_2, x="Customers Name", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Sub-dealers purchase Situation by region for year {weeks_enter_x}", color="Customers Name")
        fig_groupby_2.update_traces(textposition = 'outside')
        st.plotly_chart(fig_groupby_2)

        st.markdown("___")

        fig_groupby_pie_2 = go.Figure(data=[go.Pie(labels= sd_groupby_2["Customers Name"], values= sd_groupby_2["Purchases Qty (Pcs)"], title=f"Sub-dealers purchase Situation by region for year {weeks_enter_x}", opacity= 0.5)])
        fig_groupby_pie_2.update_traces (hoverinfo='label+percent', textfont_size=15,textinfo= 'label+percent', pull= [0.05, 0, 0, 0, 0],marker_line=dict(color='#FFFFFF', width=2))
        st.plotly_chart(fig_groupby_pie_2)

        st.markdown("___")
        
    ##########################
    ## SD model situation
    #####

    st.subheader("SD models situation", divider="blue")

    cole, colf = st.columns(2)

    with cole:
        region_md = date_frame_sd.groupby(["Years", "Products"], as_index= False)["Purchases Qty (Pcs)"].sum()
        filtre_region_md = region_md[region_md["Years"] == annee_x]
        fig_region_md = px.bar(filtre_region_md, x="Products", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Sub-dealers purchase Situation by models for year {annee_x}", color="Products")
        fig_region_md.update_traces(textposition = 'outside')
        st.plotly_chart(fig_region_md)

    with colf:
        city_md = date_frame_sd.groupby(["Years", "Products"], as_index= False)["Purchases Qty (Pcs)"].sum()
        filtre_city_md = city_md[city_md["Years"] == weeks_enter_x]
        fig_city_md = px.bar(filtre_city_md, x="Products", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Sub-dealers purchase Situation by models for year {weeks_enter_x}", color="Products")
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
        filtre_subDealer = subDealer[subDealer["Years"] == annee_x]
        fig_subDealer = px.bar(filtre_subDealer, x="Customers Name", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Sub-dealers purchase Situation for year {annee_x}", color="Customers Name")
        fig_subDealer.update_traces(textposition = 'outside')
        st.plotly_chart(fig_subDealer)

    with colh:
        sd = date_frame_sd.groupby(["Years", "Customers Name"], as_index= False)["Purchases Qty (Pcs)"].sum()
        filtre_sd = sd[sd["Years"] == weeks_enter_x]
        fig_sd = px.bar(filtre_sd, x="Customers Name", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Sub-dealers purchase Situation for year {weeks_enter_x}", color="Customers Name")
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
        filtre_sub_dealer = sub_dealerx[sub_dealerx["Years"] == annee_x] # Definir l'annee
        
        filter_client =  filtre_sub_dealer[filtre_sub_dealer["Customers Name"] == select_sdx]
        
        fig_sub_dealer = px.bar(filter_client, x="Products", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Purchase situation of {select_sdx} for year {annee_x}", color="Products")
        fig_sub_dealer.update_traces(textposition = 'outside')
        st.plotly_chart(fig_sub_dealer)

    with colj :
        sub_dealer = date_frame_sd.groupby(["Years", "Customers Name", "Products"], as_index= False)["Purchases Qty (Pcs)"].sum()
        filtre_sub_client = sub_dealer[sub_dealer["Years"] == weeks_enter_x] # Definir l'annee
        
        filter_custo =  filtre_sub_client[filtre_sub_client["Customers Name"] == select_sdx]
        
        fig_sub_custo = px.bar(filter_custo, x="Products", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Purchase situation of {select_sdx} for year {weeks_enter_x}", color="Products")
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
    models_data_x = dataset_sd["Products"].unique()
    select_models_all = st.multiselect("Please can you select your model here : ?", models_data_x)

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
st.markdown("")
st.markdown("")
######################################################################################################################################
################################################### Partie 3 : SP-ST REPORT #############################################################
######################################################################################################################################
st.header("Party Three : SMART PHONE ST REPORT")
file_st_sp = st.file_uploader("📂 Insert your Excel file du 'ST SP Tecno' by pressing the 'Browse files' button", type=["xlsx","xls", "csv"])

if file_st_sp is not None:

    #dataset_full_SP_st = pd.read_excel(file_st)
    dataset_full_SP_st = read_file(file_st_sp )

    # Traitement des valeurs null
   
    #dataset_st = dataset_full_st.dropna() # Supprimer les valeurs null
    dataset_SP_st = dataset_full_SP_st.dropna(subset="Purchased Qty") # Mettre les valeurs null à '0'

    # Creation des dates
    col1a, col2a = st.columns(2)
    
    with col1a:
        st.text("Select Date Range")
        start_date_st_sp = st.date_input(label="From Dates")

    with col2a:
        st.text("Select Date Range")
        en_date_st_sp = st.date_input(label="To Dates")

    # Provide a message for selected date range 
    st.success("you have choosen analytics from: "+str(start_date_st_sp)+" to "+str(en_date_st_sp))

    ##################
    # Filtre dates
    ###
    date_frame_st_sp = dataset_SP_st[(dataset_SP_st["Date"]>=str(start_date_st_sp)) & (dataset_SP_st["Date"]<=str(en_date_st_sp))]

    ## Situation general des achats
    st.subheader("ST General situation", divider="rainbow")
    
    #####################
    # 1- Yearly buy
    ######
    
    buy_st = dataset_full_SP_st.groupby(["Years"], as_index= False)["Purchased Qty"].sum()
    fig_buy = px.line(buy_st, x="Years", y="Purchased Qty", text="Purchased Qty", title="Yearly purchase")
    fig_buy.update_traces(textposition = 'top center')
    st.plotly_chart(fig_buy)
    st.markdown("___")

    ###############
    # 2-Monthly
    ######
    
    # Create a list for each years
    years_selected_sp = dataset_SP_st["Years"].unique()
    
    # Create the selector
    select_years_sp = st.multiselect("Select your years for SP data", years_selected_sp) # default=[2024, 2025]

    # Data Filtrage 
    month_st_sp = dataset_SP_st.groupby(["Years", "Months"], as_index= False)["Purchased Qty"].sum()
    filter_sp = month_st_sp[month_st_sp["Years"].isin(select_years_sp)]
    fig_month_sp = px.line(filter_sp, x="Months", y="Purchased Qty", text="Purchased Qty", title="Monthly purchase")
    fig_month_sp.update_traces(textposition = 'top center')
    st.plotly_chart(fig_month_sp)

    ######################################
    ## Situation semestriel des achats
    ######

    st.subheader("ST Weekly situation", divider="grey")
    
    col3a, col4a = st.columns(2)

    with col3a:
        annee_sp = st.number_input("Write the last year")
        weeks_sp = dataset_SP_st.groupby(["Years", "Weeks"], as_index= False)["Purchased Qty"].sum()
        filter_weeks_sp = weeks_sp[weeks_sp["Years"]== annee_sp]

        #----------------------------
        recupMois_old_years_sp = dataset_SP_st.groupby(["Weeks", "Date", "Years"])["Purchased Qty"].sum().reset_index()
        filter_old_years_sp = recupMois_old_years_sp[recupMois_old_years_sp["Years"]== annee_sp]
        db = filter_old_years_sp.groupby("Weeks")["Purchased Qty"].sum().reset_index() # Faire un group by sans index
        
        colva, colwa = st.columns(2)
        with colva:
            maximal_sp = filter_old_years_sp.loc[filter_old_years_sp["Purchased Qty"].idxmax()]
            string_convert_max_sp = str(maximal_sp["Date"]) # J'ai convertir mon pandas serie en chaine des caracteres
            string_convert_max_sp = string_convert_max_sp.split() # avec split, je divise ma chaine de caracteres en deux partie en choisisant l'espace vide comme indice de separation
            st.metric(label="Best weekly purchase (Pcs)", value=db["Purchased Qty"].max(), delta= string_convert_max_sp[0])
            

        with colwa:
            minimal_sp = filter_old_years_sp.loc[filter_old_years_sp["Purchased Qty"].idxmin()]
            string_convert_min_sp = str(minimal_sp["Date"]) # J'ai convertir mon pandas serie en chaine des caracteres
            string_convert_min_sp = string_convert_min_sp.split() # avec split, je divise ma chaine de caracteres en deux partie en choisisant l'espace vide comme indice de separation
            st.metric(label="Bad weekly purchase (Pcs)", value=db["Purchased Qty"].min(), delta= string_convert_min_sp[0]) # Afficher le metric de la semaine avec moins d'achats
            
        #----------------------------

        fig_week_sp = px.line(filter_weeks_sp, x="Weeks", y="Purchased Qty", title=f"Weekly {annee_sp} purchase", text="Purchased Qty")
        fig_week_sp.update_traces(textposition = 'top center')
        st.plotly_chart(fig_week_sp)

    with col4a :
        weeks_enter_sp = st.number_input("Write the recent year")
        weeks_y_sp = dataset_SP_st.groupby(["Years", "Weeks"], as_index= False)["Purchased Qty"].sum()
        filter_weeks_y_sp = weeks_y_sp[weeks_y_sp["Years"]== weeks_enter_sp]

        #----------------------------
        recupMois_new_years_sp = dataset_SP_st.groupby(["Weeks", "Date", "Years"])["Purchased Qty"].sum().reset_index()
        filter_new_years_sp = recupMois_new_years_sp[recupMois_new_years_sp["Years"]== weeks_enter_sp ]
        db_new = filter_new_years_sp.groupby("Weeks")["Purchased Qty"].sum().reset_index() # Faire un group by sans index
        
        colxa, colya = st.columns(2)
        with colxa:
            maximal_new_sp = filter_new_years_sp.loc[filter_new_years_sp["Purchased Qty"].idxmax()]
            string_convert_max_new_sp = str(maximal_new_sp["Date"]) # J'ai convertir mon pandas serie en chaine des caracteres
            string_convert_max_new_sp = string_convert_max_new_sp.split() # avec split, je divise ma chaine de caracteres en deux partie en choisisant l'espace vide comme indice de separation
            st.metric(label="Best weekly purchase (Pcs)", value=db_new["Purchased Qty"].max(), delta= string_convert_max_new_sp[0])
            

        with colya:
            minimal_new_sp = filter_new_years_sp.loc[filter_new_years_sp["Purchased Qty"].idxmin()]
            string_convert_min_new_sp = str(minimal_new_sp["Date"]) # J'ai convertir mon pandas serie en chaine des caracteres
            string_convert_min_new_sp = string_convert_min_new_sp.split() # avec split, je divise ma chaine de caracteres en deux partie en choisisant l'espace vide comme indice de separation
            st.metric(label="Bad weekly purchase (Pcs)", value=db_new["Purchased Qty"].min(), delta= string_convert_min_new_sp[0]) # Afficher le metric de la semaine avec moins d'achats
            
        #----------------------------

        fig_week_y_sp = px.line(filter_weeks_y_sp, x="Weeks", y="Purchased Qty", title=f"Weekly {weeks_enter_sp} purchase", text="Purchased Qty")
        fig_week_y_sp.update_traces(textposition = 'top center')
        st.plotly_chart(fig_week_y_sp)


    # Style the metric
    style_metric_cards(background_color="#636363", border_left_color="#a8ff78", border_color="#9FC1FF")

    ##################################
    ## Situation par modeles
    ####
    st.subheader("ST Models situation", divider="grey")
    
    col5a, col6a = st.columns(2)

    with col5a:
        #models_year_sp = st.number_input("Put the old year")
        modeles_sp = dataset_SP_st.groupby(["Years", "Products"], as_index= False)["Purchased Qty"].sum()
        filter_mdl_sp = modeles_sp[modeles_sp["Years"] == annee_sp]

        fig_mdl_sp = px.bar(filter_mdl_sp, x="Products", y="Purchased Qty", color="Products", text="Purchased Qty", title=f"Models purchased for {annee_sp}")
        fig_mdl_sp.update_traces(textposition = 'outside')
        st.plotly_chart(fig_mdl_sp)

        # Pie Chart
        fig_mdl_pie_sp = go.Figure(data=[go.Pie(labels= filter_mdl_sp["Products"], values= filter_mdl_sp["Purchased Qty"], title=f"Models proportion for {annee_sp}", opacity= 0.5)])
        fig_mdl_pie_sp.update_traces (hoverinfo='label+percent', textfont_size=15,textinfo= 'label+percent', pull= [0.05, 0, 0, 0, 0],marker_line=dict(color='#FFFFFF', width=2))
        st.plotly_chart(fig_mdl_pie_sp)


    with col6a :
        
        mdl_sp = dataset_SP_st.groupby(["Years", "Products"], as_index= False)["Purchased Qty"].sum()
        filter_model_sp = mdl_sp[mdl_sp["Years"]== weeks_enter_sp]

        fig_model_sp = px.bar(filter_model_sp, x="Products", y="Purchased Qty", color="Products", text="Purchased Qty", title=f"Models purchased for {weeks_enter_sp}")
        fig_model_sp.update_traces(textposition = 'outside')
        st.plotly_chart(fig_model_sp)

        # Pie Chart
        fig_model_pie_sp = go.Figure(data=[go.Pie(labels= filter_model_sp["Products"], values= filter_model_sp["Purchased Qty"], title=f"Models proportion for {weeks_enter_sp}", opacity= 0.5)])
        fig_model_pie_sp.update_traces (hoverinfo='label+percent', textfont_size=15,textinfo= 'label+percent', pull= [0.05, 0, 0, 0, 0],marker_line=dict(color='#FFFFFF', width=2))
        st.plotly_chart(fig_model_pie_sp)

    ############################
    ## Histogram prices 
    ####

    col7a, col8a = st.columns(2)

    with col7a:
        # Create Histogram for prices

        date_groupby_sp = date_frame_st_sp.groupby(["Years", "Products", "Prices ($)"], as_index= False)["Purchased Qty"].sum()
        prices_filter_sp = date_groupby_sp[date_groupby_sp["Years"] == weeks_enter_sp]

        # Create a histogram
        fig_hist_sp = px.histogram(prices_filter_sp, x="Prices ($)", title="Distribution models on prices", hover_data=["Purchased Qty"])
        st.plotly_chart(fig_hist_sp)


    with col8a :
        key_model_sp = date_frame_st_sp.groupby(["Years", "Products","Prices ($)"], as_index= False)["Purchased Qty"].sum()
        key_filter_sp = key_model_sp[key_model_sp["Years"] == weeks_enter_sp]

        fig_key_sp = px.bar(key_filter_sp, x="Products", y="Prices ($)", text="Prices ($)", title="Graphic Models and Prices", color="Products")
        fig_key_sp.update_traces(textposition = 'outside')
        st.plotly_chart(fig_key_sp)

    ##################################
    ## ST Channel situation
    ####
    st.subheader("ST Channel situation", divider="grey")

    col9a, col0a = st.columns(2)

    with col9a :
        city = dataset_SP_st.groupby(["Years", "City"], as_index= False)["Purchased Qty"].sum()
        city_years_sp = city[city["Years"] == annee_sp]
        fig_city_sp = px.bar(city_years_sp, x="City", y="Purchased Qty", text="Purchased Qty", title=f"Situation of Channel Kin and Lushi for {annee_sp}", color="City")
        fig_city_sp.update_traces(textposition = 'outside')
        st.plotly_chart(fig_city_sp)

        st.markdown("___")
        # Pie Chart
        fig_city_pie_sp = go.Figure(data=[go.Pie(labels= city_years_sp["City"], values= city_years_sp["Purchased Qty"], title=f"Channel proportion for {annee_sp}", opacity= 0.5)])
        fig_city_pie_sp.update_traces (hoverinfo='label+percent', textfont_size=15,textinfo= 'label+percent', pull= [0.05, 0, 0, 0, 0],marker_line=dict(color='#FFFFFF', width=2))
        st.plotly_chart(fig_city_pie_sp)
        

    with col0a :
        #channel = date_frame_st.groupby(["Years", "City"], as_index= False)["Purchased Qty"].sum()
        channel_sp = city[city["Years"] == weeks_enter_sp]
        fig_channel_sp = px.bar(channel_sp, x="City", y="Purchased Qty", text="Purchased Qty", title=f"Situation of Channel Kin and Lushi for {weeks_enter_sp}", color="City")
        fig_channel_sp.update_traces(textposition = 'outside')
        st.plotly_chart(fig_channel_sp)

        st.markdown("___")
        # Pie Chart
        fig_channel_pie_sp = go.Figure(data=[go.Pie(labels= channel_sp["City"], values= channel_sp["Purchased Qty"], title=f"Channel proportion for {weeks_enter_sp}", opacity= 0.5)])
        fig_channel_pie_sp.update_traces (hoverinfo='label+percent', textfont_size=15,textinfo= 'label+percent', pull= [0.05, 0, 0, 0, 0],marker_line=dict(color='#FFFFFF', width=2))
        st.plotly_chart(fig_channel_pie_sp)



    ##############################
    #### PREDICTION DES ACHATS ###
    ##############################

    st.header("SP Future Purchasing Forecasts", divider="rainbow")

    #############################
    ## 1- Predictions Global

    st.subheader("1. 📊Global Forecasts")

    dataset_SP_st["Months"] = pd.to_datetime(dataset_SP_st["Months"])
    st.success(f"{len(dataset_SP_st)} lignes de données chargées avec succès ✅")

    # Regrouper les ventes par mois
    prediction_global_sp = dataset_SP_st.groupby("Months")["Purchased Qty"].sum().reset_index()
    prediction_global_sp = prediction_global_sp.rename(columns={"Months":"ds", "Purchased Qty":"y"})  # On renome la colonne "Months" en "ds" et celui de "Purchased Qty" en "y". Car Prophet ne reconnait que ces noms

    # Modèle Prophet
    purchases_global_sp = Prophet()
    purchases_global_sp.fit(prediction_global_sp)

    # Prévision sur 3 mois
    predict_futur_sp = purchases_global_sp.make_future_dataframe(periods=12, freq='M') # On fait une prediction de 3 Mois en tenant compte de l'histoire des achats
    forecast_global_sp = purchases_global_sp.predict(predict_futur_sp)

    # -------------------------------
    # 4️⃣ Affichage des données
    # -------------------------------
    
    with st.expander("📄 View raw forecast data"):
        st.dataframe(forecast_global_sp[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail())


    ##############################
    #### Affichage des résultats
    ##########

    # Graphique Plotly (interactif)

    fig_global_sp = plot_plotly(purchases_global_sp, forecast_global_sp)
    fig_global_sp.update_layout(
        title = "Prévision Globale des ventes Tecno",
        xaxis_title = "Date",
        yaxis_title ="Purchases Quantity",
        template ="plotly_white",
        
        plot_bgcolor = bg_color,     #'rgba(240,248,255,1)',  # 🔹 bleu très clair à l'intérieur du graphique
        paper_bgcolor = paper_color, #'rgba(255,255,255,1)', # 🔹 fond général blanc
    )

    st.plotly_chart(fig_global_sp, use_container_width=True)

    
    #############################
    ## 2- Predictions Par Ville
    
    st.header("2. 📈 Forecasts by City")

    # Vérifier les colonnes requises
    required_colums = {"City", "Months", "Purchased Qty"}
    if not required_colums.issubset(dataset_SP_st.columns):
        st.error(f"The files must contain the columns : {', '.join(required_colums)}")
        st.stop()

    # Préparer les données

    sp_city = dataset_SP_st.groupby(["City", "Months"], as_index= False)["Purchased Qty"].sum()
    sp_city = sp_city.rename(columns={"Months":"ds", "Purchased Qty":"y"})
    sp_city["ds"] = pd.to_datetime(sp_city["ds"])

    ville_cities = sorted(dataset_SP_st["City"].unique())

    # -------------------------------
    # Paramètres utilisateur
    # -------------------------------
    nb_mois_sp_st = st.slider("Numbers of months to predict", 1, 12, 3)  # 3 mois par défaut
    col1, col2 = st.columns(2)
    predictions_sp_st_all = []

    # -------------------------------
    # Prévision par ville
    # -------------------------------
    st.header("📈 Forecasts of SP by Cities for ST")

    for i, city_st in enumerate(ville_cities):
        city_data_st = sp_city[sp_city["City"] == city_st][["ds", "y"]]
        
        if len(city_data_st) < 2:
            st.warning(f"⚠️ Sorry too little data for {city_st}, forecast ignored.")
            continue

        model_ville_sp = Prophet()
        model_ville_sp.fit(city_data_st)
        future_ville_sp = model_ville_sp.make_future_dataframe(periods=nb_mois_sp_st, freq='M')
        forecast_ville_sp = model_ville_sp.predict(future_ville_sp)
        forecast_ville_sp["City"] = city_st
        predictions_sp_st_all.append(forecast_ville_sp)

        # Graphique interactif
        fig_sp = go.Figure()
        fig_sp.add_trace(go.Scatter(x=city_data_st["ds"], y=city_data_st["y"], mode="markers+lines", name="Historique"))
        fig_sp.add_trace(go.Scatter(x=forecast_ville_sp["ds"], y=forecast_ville_sp["yhat"], mode="lines", name="Prévision"))
        fig_sp.update_layout(title=f"📍 {city_st}", xaxis_title="Date", yaxis_title="Quantité", template="plotly_white")

        st.plotly_chart(fig_sp, use_container_width=True)
            

    # -------------------------------
    # 4️⃣ Comparatif entre villes
    # -------------------------------
    if predictions_sp_st_all:
        predictions_sp_st_all = pd.concat(predictions_sp_st_all)

        # Dernière date prévue = prévision la plus récente
        latest_date_sp = predictions_sp_st_all["ds"].max()
        summary = (
            predictions_sp_st_all[predictions_sp_st_all["ds"] == latest_date_sp]
            .groupby("City")["yhat"]
            .sum()
            .reset_index()
            .sort_values(by="yhat", ascending=False)
        )

        st.text("🏆 Ranking of Cities by Purchasing Forecast for SP-ST")
        
        col3a, col4a = st.columns([2, 1])
        with col3a:
            fig_bar_sp = px.bar(
                summary,
                x="City",
                y="yhat",
                title="Average purchasing forecasts by city SP-ST",
                labels={"yhat": "Expected quantity", "City": "City"},
                text_auto=".0f",
                color="City"
            )
            fig_bar_sp.update_layout(template="plotly_white")
            st.plotly_chart(fig_bar_sp, use_container_width=True)

        with col4a:
            st.dataframe(summary.rename(columns={"yhat": "Planned quantity"}), hide_index=True)

    else:
        st.info("⬆️ Import your Excel file to get started here.")


    ##############################
    ## 3- Predictions Par SERIES
    st.subheader("3. 📊SERIES Forecasts")

    # use dataset
    # Creation d'une selecteur multiple
    series_data_sp = dataset_SP_st["SERIES"].unique()
    select_series_all_sp = st.multiselect("Please can you select your modeles Series here ? (One model please ! ) : ", series_data_sp)

    # Filtrage des donnees en fonction de la selection
    st_series_choose_all_sp = dataset_SP_st[dataset_SP_st["SERIES"].isin(select_series_all_sp)]
    st_series_all_sp = st_series_choose_all_sp.groupby("Months")["Purchased Qty"].sum().reset_index()
    st_series_all_sp = st_series_all_sp.rename(columns={"Months": "ds", "Purchased Qty": "y"})

    series_forecast_all_sp = Prophet()
    series_forecast_all_sp.fit(st_series_all_sp)

    series_future_all_sp = series_forecast_all_sp.make_future_dataframe(periods=12, freq='M')
    forecast_series_all_sp = series_forecast_all_sp.predict(series_future_all_sp)

    st.write(f"📊 Forecast Evolution by {select_series_all_sp}")
    fig_series_preview_all_sp = plot_plotly(series_forecast_all_sp, forecast_series_all_sp)
    fig_series_preview_all_sp.update_layout(
        title = "ST purchase series forcast ",
        xaxis_title = "Months",
        yaxis_title ="Purchases Quantity by model",
        template ="plotly_white",
        
        plot_bgcolor = bg_color,     #'rgba(240,248,255,1)',  # 🔹 bleu très clair à l'intérieur du graphique
        paper_bgcolor = paper_color, #'rgba(255,255,255,1)', # 🔹 fond général blanc
    )
    st.plotly_chart(fig_series_preview_all_sp, use_container_width=True)


st.markdown("___")
st.markdown("")
st.markdown("")
##########################################################################################################################################################
########################################################### Partie 4 : SP-SD REPORT  ########################################################################
##########################################################################################################################################################
st.header("Party Four : SMART PHONE SUB-DEALERS REPORT")

file_sd_sp = st.file_uploader("📂 Insert your Excel file of 'SD SP Tecno' by pressing the 'Browse files' button", type=["xlsx","xls", "csv"])

if file_sd_sp is not None:

    #dataset_full_sd = pd.read_excel(file_sd)
    dataset_full_sd_sp = read_file(file_sd_sp)

    # Traitement des valeurs null
   
    dataset_sd_sp = dataset_full_sd_sp.dropna(subset="Purchases Qty (Pcs)") # Supprimer les valeurs null

    # Creation des dates
    col1z, col1y = st.columns(2)
    
    with col1z:
        st.text("Choose the Date Range")
        start_date_sd_sp = st.date_input(label="The First Dates")

    with col1y:
        st.text("Choose the Date Range")
        en_date_sd_sp = st.date_input(label="The Last Dates")

    # Provide a message for selected date range 
    st.success("Hello ! Here is your choose analytics from: "+str(start_date_sd_sp)+" to "+str(en_date_sd_sp))

    ##################
    # Filtre dates
    ###
    date_frame_sd_sp = dataset_sd_sp[(dataset_sd_sp["Date"]>=str(start_date_sd_sp)) & (dataset_sd_sp["Date"]<=str(en_date_sd_sp))]

    #################
    # Convertir en numérique
    ######
    dataset_sd_sp["Purchases Qty (Pcs)"] = pd.to_numeric(
    dataset_sd_sp["Purchases Qty (Pcs)"],
    errors="coerce"
    )

    date_frame_sd_sp["Purchases Qty (Pcs)"] = pd.to_numeric(
    date_frame_sd_sp["Purchases Qty (Pcs)"],
    errors="coerce"
    )


    #################################
    ## Situation general des achats
    ######
    st.subheader("SP : SD General situation", divider="rainbow")

    sd_years_sd_sp = dataset_sd_sp.groupby("Years", as_index= False)["Purchases Qty (Pcs)"].sum()
    
    fig_years_sd_sp = px.line(sd_years_sd_sp, x="Years", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title="Sub-dealers Situation purchase by years")
    fig_years_sd_sp.update_traces(textposition = 'top center')
    st.plotly_chart(fig_years_sd_sp)


    ###########################
    ## SD Monthly situation
    ############
    st.subheader("SP : SD Monthly situation", divider="blue")

    colax, colbx = st.columns(2)

    with colax :
        ans = st.number_input("Write your first year here :")

        sd_month_sp = date_frame_sd_sp.groupby(["Years", "Date"], as_index= False)["Purchases Qty (Pcs)"].sum()
        
        filtre_mois_sp = sd_month_sp[sd_month_sp["Years"] == ans]
        fig_month_sd_sp = px.line(filtre_mois_sp, x="Date", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Sub-dealers purchase Situation by Month for year {ans}")
        fig_month_sd_sp.update_traces(textposition = 'top center')
        st.plotly_chart(fig_month_sd_sp)

    with colbx :
        ans_last = st.number_input("Write your last year here :")

        sd_month_2_sp = date_frame_sd_sp.groupby(["Years", "Date"], as_index= False)["Purchases Qty (Pcs)"].sum()
        filtre_mois_sp2 = sd_month_2_sp[sd_month_2_sp["Years"] == ans_last]
        fig_month_sp2 = px.line(filtre_mois_sp2, x="Date", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Sub-dealers purchase Situation by Month for year {ans_last}")
        fig_month_sp2.update_traces(textposition = 'top center')
        st.plotly_chart(fig_month_sp2)
    
    ################################
    ## SD situation by region
    ########

    st.subheader("SD situation by region", divider="blue")

    col1c, col1d = st.columns(2)

    with col1c:
        region_sd_sp = date_frame_sd_sp.groupby(["Years", "Cities"], as_index= False)["Purchases Qty (Pcs)"].sum()
        filtre_region_sd_sp = region_sd_sp[region_sd_sp["Years"] == ans]
        fig_region_sd_sp = px.bar(filtre_region_sd_sp, x="Cities", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Sub-dealers purchase Situation by region for year {ans}", color="Cities")
        fig_region_sd_sp.update_traces(textposition = 'outside')
        st.plotly_chart(fig_region_sd_sp)

    with col1d:
        city_sd_sp = date_frame_sd_sp.groupby(["Years", "Cities"], as_index= False)["Purchases Qty (Pcs)"].sum()
        filtre_sd_sp = city_sd_sp[city_sd_sp["Years"] == ans_last]
        fig_city_sd = px.bar(filtre_sd_sp, x="Cities", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Sub-dealers purchase Situation by region for year {ans_last}", color="Cities")
        fig_city_sd.update_traces(textposition = 'outside')
        st.plotly_chart(fig_city_sd)
        
    ##########################
    ## SD model and Series situation
    #####

    st.subheader("SP : SD models and Series situation", divider="blue")

    keye, keyf = st.columns(2)

    with keye:
        region_sd_sp = date_frame_sd_sp.groupby(["Years", "Products"], as_index= False)["Purchases Qty (Pcs)"].sum()
        filtre_region_sd_sp = region_sd_sp[region_sd_sp["Years"] == ans]
        fig_region_sd_sp = px.bar(filtre_region_sd_sp, x="Products", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Sub-dealers purchase Situation by models for year {ans}", color="Products")
        fig_region_sd_sp.update_traces(textposition = 'outside')
        st.plotly_chart(fig_region_sd_sp)

        st.markdown("___")

        old_series_sp = date_frame_sd_sp.groupby(["Years", "SERIES"], as_index= False)["Purchases Qty (Pcs)"].sum()
        filtre_series_sd_sp = old_series_sp[old_series_sp["Years"] == ans]
        fig_series_sd_sp = px.bar(filtre_series_sd_sp, x="SERIES", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Sub-dealers purchase Situation by Series for year {ans}", color="SERIES")
        fig_series_sd_sp.update_traces(textposition = 'outside')
        st.plotly_chart(fig_series_sd_sp)

        st.markdown("___")

        old_market_sp = date_frame_sd_sp.groupby(["Years", "Market"], as_index= False)["Purchases Qty (Pcs)"].sum()
        market_sd_sp = old_market_sp[old_market_sp["Years"] == ans]
        fig_market_sd_sp = px.bar(market_sd_sp, x="Market", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Sub-dealers purchase Situation by Series for year {ans}", color="Market")
        fig_market_sd_sp.update_traces(textposition = 'outside')
        st.plotly_chart(fig_market_sd_sp)

        st.markdown("___")


    with keyf:
        city_sp_sd = date_frame_sd_sp.groupby(["Years", "Products"], as_index= False)["Purchases Qty (Pcs)"].sum()
        filtre_city_sp_sd = city_sp_sd[city_sp_sd["Years"] == ans_last]
        fig_city_sp_sd = px.bar(filtre_city_sp_sd, x="Products", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Sub-dealers purchase Situation by models for year {ans_last}", color="Products")
        fig_city_sp_sd.update_traces(textposition = 'outside')
        st.plotly_chart(fig_city_sp_sd)

        st.markdown("___")

        recent_series_sd = date_frame_sd_sp.groupby(["Years", "SERIES"], as_index= False)["Purchases Qty (Pcs)"].sum()
        sery = recent_series_sd[recent_series_sd["Years"] == ans_last]
        fig_series_sd_sp2 = px.bar(sery, x="SERIES", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Sub-dealers purchase Situation by Series for year {ans_last}", color="SERIES")
        fig_series_sd_sp2.update_traces(textposition = 'outside')
        st.plotly_chart(fig_series_sd_sp2)

        st.markdown("___")

        recent_market_sd = date_frame_sd_sp.groupby(["Years", "Market"], as_index= False)["Purchases Qty (Pcs)"].sum()
        market_sp = recent_market_sd[recent_market_sd["Years"] == ans_last]
        fig_market_sd_sp2 = px.bar(market_sp, x="Market", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Sub-dealers purchase Situation by Market for year {ans_last}", color="Market")
        fig_market_sd_sp2.update_traces(textposition = 'outside')
        st.plotly_chart(fig_market_sd_sp2)

        st.markdown("___")


    #####################
    ## SD Performance
    ######
    
    st.subheader("SD Performance", divider="blue")

    cog, coh = st.columns(2)

    with cog:
        subDealer_sp = date_frame_sd_sp.groupby(["Years", "Customers Name"], as_index= False)["Purchases Qty (Pcs)"].sum()
        filtre_subDealer_sp = subDealer_sp[subDealer_sp["Years"] == ans]
        fig_subDealer_sp = px.bar(filtre_subDealer_sp, x="Customers Name", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Sub-dealers purchase Situation for year {ans}", color="Customers Name")
        fig_subDealer_sp.update_traces(textposition = 'outside')
        st.plotly_chart(fig_subDealer_sp)

    with coh:
        sd_sp = date_frame_sd_sp.groupby(["Years", "Customers Name"], as_index= False)["Purchases Qty (Pcs)"].sum()
        filtre_sd_sp = sd_sp[sd_sp["Years"] == ans_last]
        fig_sd_sp = px.bar(filtre_sd_sp, x="Customers Name", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Sub-dealers purchase Situation for year {ans_last}", color="Customers Name")
        fig_sd_sp.update_traces(textposition = 'outside')
        st.plotly_chart(fig_sd_sp)
    
    ###
    # Comparer les achats par client
    donneer_client = date_frame_sd_sp.copy()
    clients_sd = donneer_client["Customers Name"].unique()

    ######################
    # Select customer
    ############
    select_sd_sp =  st.selectbox("Choose your favorite sub-dealer", clients_sd)

    ######################
    ### Yearly Purchase
    st.subheader("Yearly Purchase")
    
    ans_client =  dataset_sd_sp[dataset_sd_sp["Customers Name"] == select_sd_sp]
    choix_client = ans_client.groupby(["Customers Name", "Years"], as_index= False)["Purchases Qty (Pcs)"].sum()
    
    fig_ans = px.line(choix_client, x="Years", y="Purchases Qty (Pcs)", title=f"yearly purchase for {select_sd_sp} ", text="Purchases Qty (Pcs)")
    fig_ans.update_traces(textposition = 'top center')
    st.plotly_chart(fig_ans)

    ######################
    ### Monthly Purchase
    st.subheader("Monthly Purchase")

    mois = ans_client["Years"].unique()

     # Create the selector
    sd_yearsMonth = st.multiselect("Select your favorite years", mois)

    # Data Filtrage
    mois_st = ans_client.groupby(["Years", "Date"], as_index= False)["Purchases Qty (Pcs)"].sum()
    filter_moisons = mois_st[mois_st["Years"].isin(sd_yearsMonth)]
    fig_mois = px.line(filter_moisons, x="Date", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title="Monthly purchase")
    fig_mois.update_traces(textposition = 'top center')
    st.plotly_chart(fig_mois)  


    ############################
    #####
    coli, colj = st.columns(2)

    with coli :
        sub_dealerx = date_frame_sd_sp.groupby(["Years", "Customers Name", "Products"], as_index= False)["Purchases Qty (Pcs)"].sum()
        filtre_sub_dealer = sub_dealerx[sub_dealerx["Years"] == ans] # Definir l'annee
        
        filter_client =  filtre_sub_dealer[filtre_sub_dealer["Customers Name"] == select_sd_sp]
        
        fig_sub_dealer = px.bar(filter_client, x="Products", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Purchase situation of {select_sd_sp} for year {ans}", color="Products")
        fig_sub_dealer.update_traces(textposition = 'outside')
        st.plotly_chart(fig_sub_dealer)

    with colj :
        
        filtre_sub_client = sub_dealerx[sub_dealerx["Years"] == ans_last] # Definir l'annee
        filter_custo =  filtre_sub_client[filtre_sub_client["Customers Name"] == select_sd_sp]
        
        fig_sub_custo = px.bar(filter_custo, x="Products", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title= f"Purchase situation of {select_sd_sp} for year {ans_last}", color="Products")
        fig_sub_custo.update_traces(textposition = 'outside')
        st.plotly_chart(fig_sub_custo)


    ##############################
    #### PREDICTION DES ACHATS ###
    #############################
    
    st.header("FUTURE PURCHASING FORECASTS", divider="rainbow")

    #############################
    ## 1- Predictions Global

    st.subheader("1. 📊Global Forecasts")

    dataset_sd_sp["Date"] = pd.to_datetime(dataset_sd_sp["Date"])
    st.success(f"{len(dataset_sd_sp)} lignes de données chargées avec succès ✅")

    # Regrouper les ventes par mois
    prediction_sd_sp = dataset_sd_sp.groupby("Date")["Purchases Qty (Pcs)"].sum().reset_index()
    prediction_sd_sp = prediction_sd_sp.rename(columns={"Date":"ds", "Purchases Qty (Pcs)":"y"})  # On renome la colonne "Months" en "ds" et celui de "Purchased Qty" en "y". Car Prophet ne reconnait que ces noms

    # Modèle Prophet
    purchases_sd_sp = Prophet()
    purchases_sd_sp.fit(prediction_sd_sp)

    # Prévision sur 3 mois
    predict_futur_sp = purchases_sd_sp.make_future_dataframe(periods=12, freq='M') # On fait une prediction de 3 Mois en tenant compte de l'histoire des achats
    forecast_global_sp = purchases_sd_sp.predict(predict_futur_sp)
    

    # -------------------------------
    # 4️⃣ Affichage des données
    # -------------------------------
    with st.expander("📄 Voir les données de prévision brutes"):
        st.dataframe(forecast_global_sp[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail())


    ##############################
    #### Affichage des résultats
    ##########

    # Graphique Plotly (interactif)

    fig_global_sd_sp = plot_plotly(purchases_sd_sp, forecast_global_sp)
    fig_global_sd_sp.update_layout(
        title = "Prévision Globale des ventes Tecno",
        xaxis_title = "Date",
        yaxis_title ="Quantité achetée",
        template ="plotly_white",
        
        plot_bgcolor = bg_color,     #'rgba(240,248,255,1)',  # 🔹 bleu très clair à l'intérieur du graphique
        paper_bgcolor = paper_color, #'rgba(255,255,255,1)', # 🔹 fond général blanc
    )

    st.plotly_chart(fig_global_sd_sp, use_container_width=True)

    ##############################
    ## 2- Predictions Par SERIES
    st.subheader("2. 📊SERIES Forecasts")

    models_data_sd_sp = dataset_sd_sp["SERIES"].unique()  
    # Creation d'une selecteur multiple
    select_series_all_sp = st.multiselect("Please can you select your series here ? ", models_data_sd_sp)

    # Filtrage des donnees en fonction de la selection
    sd_series_choose_sp = dataset_sd_sp[dataset_sd_sp["SERIES"].isin(select_series_all_sp)]
    sd_serie_sp = sd_series_choose_sp.groupby("Date")["Purchases Qty (Pcs)"].sum().reset_index()
    sd_serie_sp = sd_serie_sp.rename(columns={"Date": "ds", "Purchases Qty (Pcs)": "y"})

    series_forecast_sp_sd = Prophet()
    series_forecast_sp_sd.fit(sd_serie_sp)

    series_future_sp_sd = series_forecast_sp_sd.make_future_dataframe(periods=12, freq='M')
    series_model_sp_sd = series_forecast_sp_sd.predict(series_future_sp_sd)

    st.write(f"📊 Forecast Evolution by {select_series_all_sp}")
    fig_series_preview_sd_sp = plot_plotly(series_forecast_sp_sd, series_model_sp_sd)
    fig_series_preview_sd_sp.update_layout(
        title = "Clients purchase series forcast ",
        xaxis_title = "Months",
        yaxis_title ="Purchases Quantity by model",
        template ="plotly_white",
        
        plot_bgcolor = bg_color,     #'rgba(240,248,255,1)',  # 🔹 bleu très clair à l'intérieur du graphique
        paper_bgcolor = paper_color, #'rgba(255,255,255,1)', # 🔹 fond général blanc
    )
    st.plotly_chart(fig_series_preview_sd_sp, use_container_width=True)


    #############################
    ## 3- Predictions Par Ville
    st.subheader("3. 📊Cities Forecasts")

    # Vérifier les colonnes requises
    required_colms_SD = {"Cities", "Date", "Purchases Qty (Pcs)"}
    if not required_colms_SD.issubset(dataset_sd_sp.columns):
        st.error(f"The file must contain the columns : {', '.join(required_colms_SD)}")
        st.stop()
    
    # Préparer les données
    
    date_ville_SD = dataset_sd_sp.groupby(["Cities", "Date"], as_index= False)["Purchases Qty (Pcs)"].sum() 
    date_ville_SD = date_ville_SD.rename(columns={"Date":"ds", "Purchases Qty (Pcs)":"y"})
    date_ville_SD["ds"] = pd.to_datetime(date_ville_SD["ds"])

    cities_SD = sorted(dataset_sd_sp["Cities"].unique())
    st.success(f"✅ {len(cities_SD)} cities detected : {', '.join(cities_SD)}")

    # -------------------------------
    # Paramètres utilisateur
    # -------------------------------
    nb_mois_SD = st.slider("Choose your number of months to predict", 1, 3, 12)  # 3 mois par défaut

    col1b, col2b = st.columns(2)
    predictions_all_SD = []

    # -------------------------------
    # Prévision par ville
    # -------------------------------
    st.header("📈 Forecasts by City")

    for i, city_SD in enumerate(cities_SD):
        city_data_SD = date_ville_SD[date_ville_SD["Cities"] == city_SD][["ds", "y"]]
        
        if len(city_data_SD) < 5:
            st.warning(f"⚠️ Too little data for {city_SD}, forecast ignored.")
            continue

        model_ville_SD = Prophet()
        model_ville_SD.fit(city_data_SD)
        future_ville_SD = model_ville_SD.make_future_dataframe(periods=nb_mois_SD, freq='M')
        forecast_ville_SD = model_ville_SD.predict(future_ville_SD)
        forecast_ville_SD["Cities"] = city_SD
        predictions_all_SD.append(forecast_ville_SD)

        # Graphique interactif
        fig_SD = go.Figure()
        fig_SD.add_trace(go.Scatter(x=city_data_SD["ds"], y=city_data_SD["y"], mode="markers+lines", name="Historique"))
        fig_SD.add_trace(go.Scatter(x=forecast_ville_SD["ds"], y=forecast_ville_SD["yhat"], mode="lines", name="Prévision"))
        fig_SD.update_layout(title=f"📍 {city_SD}", xaxis_title="Date", yaxis_title="Quantité", template="plotly_white")

        # Affichage côte à côte
        if i % 2 == 0:
            with col1b:
                st.plotly_chart(fig_SD, use_container_width=True)
        else:
            with col2b:
                st.plotly_chart(fig_SD, use_container_width=True)

    # -------------------------------
    # 4️⃣ Comparatif entre villes
    # -------------------------------
    if predictions_all_SD:
        predictions_all_SD = pd.concat(predictions_all_SD)

        # Dernière date prévue = prévision la plus récente
        latest_date_SD = predictions_all_SD["ds"].max()
        summary = (
            predictions_all_SD[predictions_all_SD["ds"] == latest_date_SD]
            .groupby("Cities")["yhat"]
            .sum()
            .reset_index()
            .sort_values(by="yhat", ascending=False)
        )

        st.text("🏆 Ranking of Cities by Purchasing Forecast")
        
        col3x, col4x = st.columns([2, 1])
        with col3x:
            fig_bar_SD = px.bar(
                summary,
                x="Cities",
                y="yhat",
                title="Average purchasing forecasts by city",
                labels={"yhat": "Expected quantity", "City": "City"},
                text_auto=".0f",
                color="Cities"
            )
            fig_bar_SD.update_layout(template="plotly_white")
            st.plotly_chart(fig_bar_SD, use_container_width=True)

        with col4x:
            st.dataframe(summary.rename(columns={"yhat": "Planned quantity"}), hide_index=True)

    else:
        st.info("⬆️ Import your Excel file to get started.")

st.markdown("___")
#############################
### FIN
#########################
st.title("THANKS FOR YOUR ATTENTION !")
# Librairies
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.metric_cards import style_metric_cards

st.markdown("<h1 style='text-align: center; color: blue;'> TECNO FEATURE PHONE YEARLY REPORT"
"</h1>", unsafe_allow_html= True)
st.markdown("<br/>", unsafe_allow_html= True)
st.markdown("<br/>", unsafe_allow_html= True)
st.markdown("<h6 style='text-align: center; color: red;'> Welcome in our feature phone report. In this report we can found the datas of ST and A sub-dealers"
" "
"</h6>", unsafe_allow_html= True)

st.markdown("___")
########################
# Load dataset
###

######################################################################################################################################
################################################### Partie 1 : ST REPORT #############################################################
######################################################################################################################################
file_st = st.file_uploader("Inserer votre fichier Excel ou CSV du 'ST FP Tecno' en appuyant sur le bouton 'Browse files'", type=["xlsx", "csv"])

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
    st.error("you have choosen analytics from: "+str(start_date_st)+" to "+str(en_date_st))

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

    month_st = date_frame_st.groupby(["Years", "Months"], as_index= False)["Purchased Qty"].sum()
    fig_month = px.line(month_st, x="Months", y="Purchased Qty", text="Purchased Qty", title="Monthly purchase")
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
            target_2025["Target"] = [16000, 16000, 16000, 17000, 17000, 17000]
            return target_2025["Target"]
        elif target_2025["Months"].nunique() == 7:
            target_2025["Target"] = [16000, 16000, 16000, 17000, 17000, 17000, 18500]
            return target_2025["Target"]
        elif target_2025["Months"].nunique() == 8:
            target_2025["Target"] = [16000, 16000, 16000, 17000, 17000, 17000, 18500, 18500]
            return target_2025["Target"]
        elif target_2025["Months"].nunique() == 9:
            target_2025["Target"] = [16000, 16000, 16000, 17000, 17000, 17000, 18500, 18500, 19000]
            return target_2025["Target"]
        elif target_2025["Months"].nunique() == 10:
            target_2025["Target"] = [16000, 16000, 16000, 17000, 17000, 17000, 18500, 18500, 19000, 20000]
            return target_2025["Target"]
        elif target_2025["Months"].nunique() == 11:
            target_2025["Target"] = [16000, 16000, 16000, 17000, 17000, 17000, 18500, 18500, 19000, 20000, 20000]
            return target_2025["Target"]
        elif target_2025["Months"].nunique() == 12:
            target_2025["Target"] = [16000, 16000, 16000, 17000, 17000, 17000, 18500, 18500, 19000, 20000, 20000, 20000]
            return target_2025["Target"]
        else:
            return None  # ou gérer autrement si plusieurs mois
        
    target = creer_target_si_un_mois(target_2025)

    #st.write(target)

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


##########################################################################################################################################################
########################################################### Partie 2 : SD REPORT  ########################################################################
##########################################################################################################################################################
file_sd = st.file_uploader("Inserer votre fichier Excel ou CSV du 'SD FP Tecno' en appuyant sur le bouton 'Browse files'", type=["xlsx", "csv"])

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
    st.error("Here is your choose analytics from: "+str(start_date_sd)+" to "+str(en_date_sd))

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
            SD_target_2025["Target"] = [9600, 9600, 9600, 10200]
            return SD_target_2025["Target"]
        elif SD_target_2025["Date"].nunique() == 5:
            SD_target_2025["Target"] = [9600, 9600, 9600, 10200, 10200]
            return SD_target_2025["Target"]
        elif SD_target_2025["Date"].nunique() == 6:
            SD_target_2025["Target"] = [9600, 9600, 9600, 10200, 10200, 10200]
            return SD_target_2025["Target"]
        elif SD_target_2025["Date"].nunique() == 7:
            SD_target_2025["Target"] = [9600, 9600, 9600, 10200, 10200, 10200, 11100]
            return SD_target_2025["Target"]
        elif SD_target_2025["Date"].nunique() == 8:
            SD_target_2025["Target"] = [9600, 9600, 9600, 10200, 10200, 10200, 11100, 11100]
            return SD_target_2025["Target"]
        elif SD_target_2025["Date"].nunique() == 9:
            SD_target_2025["Target"] = [9600, 9600, 9600, 10200, 10200, 10200, 11100, 11100, 11400]
            return SD_target_2025["Target"]
        elif SD_target_2025["Date"].nunique() == 10:
            SD_target_2025["Target"] = [9600, 9600, 9600, 10200, 10200, 10200, 11100, 11100, 11400, 12000]
            return SD_target_2025["Target"]
        elif SD_target_2025["Date"].nunique() == 11:
            SD_target_2025["Target"] = [9600, 9600, 9600, 10200, 10200, 10200, 11100, 11100, 11400, 12000, 12000]
            return SD_target_2025["Target"]
        elif SD_target_2025["Date"].nunique() == 12:
            SD_target_2025["Target"] = [9600, 9600, 9600, 10200, 10200, 10200, 11100, 11100, 11400, 12000, 12000, 12000]
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
        


    
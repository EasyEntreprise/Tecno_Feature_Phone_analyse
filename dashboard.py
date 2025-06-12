# Librairies
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.metric_cards import style_metric_cards


st.markdown("<h1 style='text-align: center; color: blue;'> TECNO FP ST DASHBOARD </h1>", unsafe_allow_html= True)
st.markdown("<br/>", unsafe_allow_html= True)
st.markdown("<br/>", unsafe_allow_html= True)
st.markdown("<h6 style='text-align: center; color: red;'> Welcome in our feature phone dashboard for Tecno brand DRC. This dashboard is important for following the ST purchase of customers."
"In this "
"</h6>", unsafe_allow_html= True)

st.markdown("___")

# Load dataset
file = st.file_uploader("Inserer votre fichier Excel en appuyant sur le bouton 'Browse files'", type=["xlsx","xls"])

if file is not None:
    dataset_full = pd.read_excel(file)
    #dataset = pd.read_excel(file)

    # Traitement des valeurs null
    #dataset = dataset_full.fillna(0) # Mettre les valeurs null à '0'
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

    col1.metric(label="Sum Purchase(Pcs)", value= date_frame["Purchased Qty"].sum(), delta="General Purchase(Pcs)")
    col2.metric(label="General Average(Pcs)", value= date_frame["Purchased Qty"].mean(), delta="General Average(Pcs)")
    col3.metric(label="High Price($)", value= date_frame["Prices ($)"].max(), delta = converter_high_price)
    col4.metric(label="Low Price($)", value= date_frame["Prices ($)"].min(), delta = converter_low_price)

    dbmax = db.loc[db["Purchased Qty"].idxmax()] # Recuperation de la semaine avec le plus grand achat
    dbmin = db.loc[db["Purchased Qty"].idxmin()] # Recuperation de la semaine avec le plus faible achat

    col5.metric(label="Best week (Pcs)", value=db["Purchased Qty"].max(), delta= dbmax["Weeks"]) # Afficher le metric de la semaine avec plus d'achats
    col6.metric(label="Bad week (Pcs)", value=db["Purchased Qty"].min(), delta= dbmin["Weeks"]) # Afficher le metric de la semaine avec moins d'achats


    a1, a2 = st.columns(2)

    with a1 :
        st.subheader("Graphic Keys models", divider="blue")
        models = date_frame["Products"].unique()    #["T101", "T353", "T528", "T528 New"]
        
        selecte_models = st.multiselect("Selecte your models here", models, default=["T101", "T353", "T528 New"])
        key_model = date_frame.groupby(["Products","Prices ($)"], as_index= False)["Purchased Qty"].sum()
        models_filter = key_model[key_model["Products"].isin(selecte_models)]

        fig_key = px.bar(models_filter, x="Products", y="Prices ($)", text="Prices ($)", title="Graphic Models and Prices", color="Products")
        st.plotly_chart(fig_key)

        #st.markdown("___")
        area_data = date_frame.groupby("City")["Purchased Qty"].sum().reset_index()
        fig_pie = go.Figure(data=[go.Pie(labels= area_data["City"], values= area_data["Purchased Qty"], title="Proportion purchase by City", opacity= 0.5)])
        fig_pie.update_traces (hoverinfo='label+percent', textfont_size=15,textinfo= 'label+percent', pull= [0.05, 0, 0, 0, 0],marker_line=dict(color='#FFFFFF', width=2))
        st.plotly_chart(fig_pie)

    #####   
    # Metric keys models
    with a2 :
        st.subheader("Keys Modeles", divider="rainbow")
        key1,key2 = st.columns(2)

        T101 = date_frame[date_frame["Products"]=="T101"]
        key1.metric(label="Model T101 (Pcs)", value= T101["Purchased Qty"].sum(), delta=T101["Purchased Qty"].mean()) 

        T353 = date_frame[date_frame["Products"]=="T353"]
        key2.metric(label="Model T353 (Pcs)", value= T353["Purchased Qty"].sum(), delta=T353["Purchased Qty"].mean()) 
        

        key3,key4 = st.columns(2)
        T528 = date_frame[date_frame["Products"]=="T528"]
        key3.metric(label="Model T528 (Pcs)", value= T528["Purchased Qty"].sum(), delta=T528["Purchased Qty"].mean()) 

        T528New = date_frame[date_frame["Products"]=="T528 New"]
        key4.metric(label="Model T528 New (Pcs)", value= T528New["Purchased Qty"].sum(), delta=T528New["Purchased Qty"].mean())

        dataset_kin = date_frame[date_frame["City"]=="KIN"]
        dataset_Lushi = date_frame[date_frame["City"]=="Lushi"]
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
    a3,a4 = st.columns(2)

    with a3 :
        # Creation d'une liste des models uniques
        models_data = date_frame["Products"].unique()

        # Creation d'une selecteur multiple
        selected_models = st.multiselect("Selecte your models", models_data, default=["T101", "T353", "T528 New"])

        # Filtrage des donnees en fonction de la selection
        date_groupby = date_frame.groupby(["City","Products"], as_index= False)["Purchased Qty"].sum()
        df_filtered = date_groupby[date_groupby["Products"].isin(selected_models)]
        
        fig_area = px.bar(df_filtered, x="City", y="Purchased Qty", text="Purchased Qty", title="Models purchase by region", color="Products", barmode="group")
        fig_area.update_traces(textposition = 'outside')
        st.plotly_chart(fig_area)
    

    with a4 :
        date_groupby = date_frame.groupby(["Products", "Prices ($)"], as_index= False)["Purchased Qty"].sum()

        # Create a histogram
        fig_hist = px.histogram(date_groupby, x="Prices ($)", title="Distribution models on prices", hover_data=["Purchased Qty"])
        st.plotly_chart(fig_hist)

    #####################
    # Situation Models
    ####
    
    st.subheader("Situation by Models", divider="rainbow")
    date_groupbyx = date_frame.groupby(["Products", "Prices ($)"], as_index= False)["Purchased Qty"].sum()
        
    fig_product = px.bar(date_groupbyx, x="Products", y="Purchased Qty", color="Products", text="Purchased Qty")
    fig_product.update_traces(textposition = 'outside')
    st.plotly_chart(fig_product)

    fig_product_pie = go.Figure(data = [go.Pie(labels = date_groupbyx["Products"], values= date_groupbyx["Purchased Qty"], title = "Proportions models", opacity=0.5)])
    fig_product_pie.update_traces (hoverinfo='label+percent', textfont_size=15,textinfo= 'label+percent', pull= [0.05, 0, 0, 0, 0],marker_line=dict(color='#FFFFFF', width=2))
    st.plotly_chart(fig_product_pie)


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
    data_weeks = px.line(db, x="Weeks", y="Purchased Qty", title="Situation purchase by weeks", text="Purchased Qty")
    data_weeks.update_traces(textposition = 'top center')
    st.plotly_chart(data_weeks)

    #############################
    # Target and Achievement
    # ####### 

    st.subheader("Target & Achievment", divider="rainbow")

    view_2025 = date_frame[date_frame["Years"] == 2025] # dataset_full
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
        bargap = 0.8
    )

    st.plotly_chart(fig_cmb)

    ##########################
    # Situation by years
    ####
    st.subheader("Situation purchase by Years", divider="rainbow")
    dataset_years = dataset.groupby("Years")["Purchased Qty"].sum().reset_index()
    data_years = px.line(dataset_years, x="Years", y="Purchased Qty", title="Situation purchase by years", text="Purchased Qty")
    data_years.update_traces(textposition = 'top center')
    st.plotly_chart(data_years)


    #########################
    ### Price List and Profit
    ####

    st.subheader("Price List & Profit", divider="rainbow")
    
    # Price List
    st.subheader("Price List")
    products = date_frame[["Products", "Prices ($)", "B Price($)", "R Price($)", "A-B Profit($)", "A-R Profit($)", "B-R Profit($)"]].drop_duplicates()
    st.write(products)

    # Profis
    c1, c2, c3 = st.columns(3)

    with c1:
        products_AB = date_frame[["Products", "Prices ($)", "B Price($)", "A-B Profit($)"]].drop_duplicates()
        barre_AB = px.bar(products, x="Products", y="A-B Profit($)", color="Products", text= "A-B Profit($)", title="Profit of A price on B price")
        barre_AB.update_traces(textposition = 'outside')
        st.plotly_chart(barre_AB)
        

    with c2:
        products_AR = date_frame[["Products", "Prices ($)", "R Price($)", "A-R Profit($)"]].drop_duplicates()
        barre_AR = px.bar(products, x="Products", y="A-R Profit($)", color="Products", text= "A-R Profit($)", title="Profit of A price on R price")
        barre_AR.update_traces(textposition = 'outside')
        st.plotly_chart(barre_AR)

    with c3:
        products_BR = date_frame[["Products", "B Price($)", "R Price($)", "B-R Profit($)"]].drop_duplicates()
        barre_BR = px.bar(products, x="Products", y="B-R Profit($)", color="Products", text= "B-R Profit($)", title="Profit of B price on R price")
        barre_BR.update_traces(textposition = 'outside')
        st.plotly_chart(barre_BR)

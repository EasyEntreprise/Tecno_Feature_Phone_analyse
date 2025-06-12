# Librairies
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.metric_cards import style_metric_cards


st.markdown("<h1 style='text-align: center; color: blue;'> TECNO FP SUB-DEALERS DASHBOARD </h1>", unsafe_allow_html= True)
st.markdown("<br/>", unsafe_allow_html= True)
st.markdown("<br/>", unsafe_allow_html= True)
st.markdown("<h6 style='text-align: center; color: red;'> Welcome in our SD purchases Dashboard for Tecno DRC feature phone. This dashboard is important for following the purchase of A sub-dealers."
" "
"</h6>", unsafe_allow_html= True)

st.markdown("___")
########################
# Load dataset
###
file = st.file_uploader("Insert your Excel file by pressing the 'Browse files' button", type=["xlsx","xls"])

if file is not None:
    dataset_full = pd.read_excel(file)

    # Traitement des valeurs null
    dataset = dataset_full.dropna(subset="Purchases Qty (Pcs)") # Mettre les valeurs null à '0'
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


        # Style the metric
        style_metric_cards(background_color="#3c4d66", border_left_color="#99f2c8", border_color="#0006a")
        
        

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

        col1.metric(label="Situation Kin", value= sit_kin["Purchases Qty (Pcs)"], delta=kin_sd["Purchases Qty (Pcs)"].sum()/kinshasa)
        col2.metric(label="Situation Kat", value= sit_kat["Purchases Qty (Pcs)"], delta=kat_sd["Purchases Qty (Pcs)"].sum()/katanga)
        col3.metric(label="Situation KC", value= sit_kc["Purchases Qty (Pcs)"], delta=kc_sd["Purchases Qty (Pcs)"].sum()/kcongo)
        col4.metric(label="Situation BK", value= sit_bk["Purchases Qty (Pcs)"], delta=bk_sd["Purchases Qty (Pcs)"].sum()/bkasai)
        col5.metric(label="Situation BE", value= sit_be["Purchases Qty (Pcs)"], delta=be_sd["Purchases Qty (Pcs)"].sum()/bequator)

        achat_year = date_frame.groupby("Cities", as_index= False)["Purchases Qty (Pcs)"].sum()
        fig_pie = go.Figure(data=[go.Pie(labels= achat_year["Cities"], values= achat_year["Purchases Qty (Pcs)"], title="Proportion des données par City", opacity= 0.5)])
        fig_pie.update_traces (hoverinfo='label+percent', textfont_size=15,textinfo= 'label+percent', pull= [0.05, 0, 0, 0, 0],marker_line=dict(color='#FFFFFF', width=2))
        st.plotly_chart(fig_pie)

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
    selected_models = st.multiselect("Selecte your models", models_data, default=["T101", "T353", "T528"])


    # Filtrage des donnees en fonction de la selection
    date_groupby = date_frame.groupby(["Products", "Date"], as_index= False)["Purchases Qty (Pcs)"].sum()
    df_filtered = date_groupby[date_groupby["Products"].isin(selected_models)]

    fig_select = px.line(df_filtered, x="Date", y="Purchases Qty (Pcs)", color="Products", text="Purchases Qty (Pcs)")
    fig_select.update_traces(textposition = 'top center')
    st.plotly_chart(fig_select)
 
    #fig_area = px.bar(df_filtered, x="City", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title="Models purchase by area", color="Products", barmode="group")
    #st.plotly_chart(fig_area)


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
            target_2025["Target"] = [9600, 9600, 9600, 10200]
            return target_2025["Target"]
        elif target_2025["Date"].nunique() == 5:
            target_2025["Target"] = [9600, 9600, 9600, 10200, 10200]
            return target_2025["Target"]
        elif target_2025["Date"].nunique() == 6:
            target_2025["Target"] = [9600, 9600, 9600, 10200, 10200, 9520]
            return target_2025["Target"]
        elif target_2025["Date"].nunique() == 7:
            target_2025["Target"] = [9600, 9600, 9600, 10200, 10200, 9520, 10640]
            return target_2025["Target"]
        elif target_2025["Date"].nunique() == 8:
            target_2025["Target"] = [9600, 9600, 9600, 10200, 10200, 9520, 10640, 10640]
            return target_2025["Target"]
        elif target_2025["Date"].nunique() == 9:
            target_2025["Target"] = [9600, 9600, 9600, 10200, 10200, 9520, 10640, 10640, 11760]
            return target_2025["Target"]
        elif target_2025["Date"].nunique() == 10:
            target_2025["Target"] = [9600, 9600, 9600, 10200, 10200, 9520, 10640, 10640, 11760, 11760]
            return target_2025["Target"]
        elif target_2025["Date"].nunique() == 11:
            target_2025["Target"] = [9600, 9600, 9600, 10200, 10200, 9520, 10640, 10640, 11760, 11760, 12880]
            return target_2025["Target"]
        elif target_2025["Date"].nunique() == 12:
            target_2025["Target"] = [9600, 9600, 9600, 10200, 10200, 9520, 10640, 10640, 117600, 11760, 12880, 14000]
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
    

    ########################
    # Profil des clients  
    ########
    st.subheader("Profils client", divider="rainbow")
    
    sd_unique = date_frame["Customers Name"].unique()
        
    select_sd = st.selectbox("Choose your sub-dealer name", sd_unique) # On selectionne les clients
    region = date_frame[date_frame["Customers Name"]==select_sd] # Recuperer la region du client selectionner
    total_buy = region.groupby("Customers Name", as_index= False)["Purchases Qty (Pcs)"].sum() # Total achat du client selectionner 
    total_inv = region.groupby("Customers Name", as_index= False)["Investments ($)"].sum() # Total achat du client invest

    nbr_line = region["Months"].unique() 

    col6, col7, col8 = st.columns(3)

    col6.metric(label="SD NAME", value=select_sd, delta=str(region["Cities"].unique()))
    col7.metric(label="Total Purchase (Pcs)", value=int(total_buy["Purchases Qty (Pcs)"]), delta=int(total_buy["Purchases Qty (Pcs)"])/int(nbr_line.shape[0]))
    col8.metric(label="Total Invest ($)", value=int(total_inv["Investments ($)"]), delta=int(total_inv["Investments ($)"])/int(nbr_line.shape[0]))

    # Graphic radar
    achat_models_sd = region.groupby(["Customers Name", "Products"], as_index = False)["Purchases Qty (Pcs)"].sum()

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
    achat_mensuel_sd = region.groupby(["Customers Name", "Date"], as_index = False)["Purchases Qty (Pcs)"].sum()
    fig_sd = px.line(achat_mensuel_sd, x="Date", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title=f"Purchases Sub-dealers {select_sd} by months")
    fig_sd.update_traces(textposition = 'top center')
    st.plotly_chart(fig_sd)
    st.markdown("___")

    # Graphic achat mensuel du client selectionner par models
        
    fig_sd_models = px.bar(achat_models_sd, x="Products", y="Purchases Qty (Pcs)", text="Purchases Qty (Pcs)", title=f"Purchases of  Sub-dealers {select_sd} by models", color="Products")
    fig_sd_models.update_traces(textposition = 'outside')
    st.plotly_chart(fig_sd_models)




    

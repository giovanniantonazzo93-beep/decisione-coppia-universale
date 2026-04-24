import streamlit as st
import google.generativeai as genai
import os

# Configurazione Pagina
st.set_page_config(page_title="Decision Bot Universale", layout="centered")
st.title("🤖 Decision Bot Universale per Coppie")

# Sidebar per API Key
api_key = st.sidebar.text_input("Inserisci Google API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    # Utilizzo del modello stabile per evitare errori 404
    model = genai.GenerativeModel('gemini-3-flash-preview')

    # Sezione Input
    with st.form("input_form"):
        col1, col2 = st.columns(2)
        with col1:
            citta = st.text_input("Città", value="Pesaro")
            orario = st.selectbox("Momento della giornata", ["Mattina", "Pomeriggio", "Sera", "Notte"])
            meteo = st.selectbox("Meteo", ["Sole", "Pioggia", "Freddo/Nuvole"])
        
        with col2:
            budget = st.select_slider("Budget", options=["€", "€€", "€€€"])
            mezzo = st.selectbox("Mezzo di trasporto", ["A piedi", "Mezzi pubblici", "Auto"])

        st.divider()
        c3, c4 = st.columns(2)
        with c3:
            stanchezza_lui = st.slider("Stanchezza Lui (1=Attivo, 10=Distrutto)", 1, 10, 5)
        with c4:
            stanchezza_lei = st.slider("Stanchezza Lei (1=Attivo, 10=Distrutto)", 1, 10, 5)
        
        submit = st.form_submit_button("Genera Proposte")

    if submit:
        # Costruzione del Prompt
        prompt = f"""
        Agisci come un esperto local di {citta}.
        Dati attuali: Orario {orario}, Meteo {meteo}, Mezzo: {mezzo}, Budget: {budget}.
        
        Profilo Lui: Stanchezza {stanchezza_lui}/10.
        Profilo Lei: Stanchezza {stanchezza_lei}/10.
        
        Fornisci 3 proposte reali basate su luoghi esistenti a {citta}:
        1. Proposta LUI: Favorisce i suoi interessi e livello di stanchezza.
        2. Proposta LEI: Favorisce i suoi interessi e livello di stanchezza.
        3. COMPROMESSO: Una via di mezzo perfetta per entrambi.
        
        Per ogni proposta indica: Nome del posto, Orario consigliato e Prezzo stimato.
        Sii conciso e simpatico.
        """

        try:
            with st.spinner("Consultando le stelle (e l'IA)..."):
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
        except Exception as e:
            st.error(f"Errore nella chiamata API: {e}")
            st.info("Verifica che il modello 'gemini-1.5-flash' sia abilitato per la tua regione e chiave API.")
else:
    st.warning("Per favore, inserisci la tua API Key nella sidebar per iniziare.")

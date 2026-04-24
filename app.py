import streamlit as st
import google.generativeai as genai
import os

# Configurazione Pagina
st.set_page_config(page_title="Decision Bot Universale", layout="centered")
st.title("🤖 Decision Bot Universale per Coppie")

# Sidebar per API Key
with st.sidebar:
    api_key = st.text_input("Inserisci Google API Key", type="password")
    if api_key:
        genai.configure(api_key=api_key)

# INPUT GENERALI
col1, col2 = st.columns(2)
with col1:
    citta = st.text_input("Città", value="Pesaro")
    meteo = st.selectbox("Meteo", ["Sole", "Pioggia", "Freddo", "Nuvole"])
with col2:
    orario = st.time_input("Orario attuale")
    budget = st.select_slider("Budget", options=["€", "€€", "€€€"])

st.divider()

# DATI LUI & LEI
c_lui, c_lei = st.columns(2)
with c_lui:
    st.subheader("Lui 👤")
    stanchezza_lui = st.slider("Stanchezza (Lui)", 1, 10, 5, key="s_lui")
    mezzo_lui = st.selectbox("Mezzo preferito (Lui)", ["Piedi", "Mezzi", "Auto"], key="m_lui")

with c_lei:
    st.subheader("Lei 👤")
    stanchezza_lei = st.slider("Stanchezza (Lei)", 1, 10, 5, key="s_lei")
    mezzo_lei = st.selectbox("Mezzo preferito (Lei)", ["Piedi", "Mezzi", "Auto"], key="m_lei")

# LOGICA GENERATIVA
if st.button("Genera Proposte ✨"):
    if not api_key:
        st.error("Per favore, inserisci l'API Key nella sidebar.")
    else:
        try:
            # Selezione del modello corretto (versione stabile)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            Agisci come un esperto local concierge a {citta}. 
            Pianifica 3 attività reali per una coppia considerando questi dati:
            - Meteo: {meteo}
            - Orario: {orario}
            - Budget massimo: {budget}
            
            Profilo Lui: Stanchezza {stanchezza_lui}/10, preferisce spostarsi con {mezzo_lui}.
            Profilo Lei: Stanchezza {stanchezza_lei}/10, preferisce spostarsi con {mezzo_lei}.
            
            REGOLE:
            1. Proposta LUI: Basata sui suoi interessi e basso sforzo fisico se stanco.
            2. Proposta LEI: Basata sui suoi interessi e preferenze di movimento.
            3. Proposta COMPROMESSO: Una via di mezzo perfetta che minimizza lo stress di entrambi.
            
            Per ogni proposta indica: Nome del posto reale a {citta}, motivo della scelta, orario consigliato e costo stimato.
            Rispondi in Italiano con un tono amichevole e sintetico.
            """
            
            with st.spinner('Interrogando Gemini...'):
                response = model.generate_content(prompt)
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Errore durante la generazione: {e}")
            st.info("Suggerimento: Verifica che il modello 'gemini-1.5-flash' sia disponibile per la tua regione o controlla la versione v1beta nell'URL dell'API.")

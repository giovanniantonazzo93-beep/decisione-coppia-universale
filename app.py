import streamlit as st
from google import genai
import sys

# Configurazione Pagina
st.set_page_config(page_title="Decision Bot Universale", layout="wide")

st.title("🤖 Decision Bot Universale per Coppie")
st.caption(f"Status: Pronto (Python {sys.version.split()[0]})")

# Sidebar per configurazione
with st.sidebar:
    st.header("Configurazione")
    api_key = st.text_input("Inserisci Google API Key", type="password")
    st.divider()
    citta = st.text_input("Città", value="Pesaro")
    meteo = st.selectbox("Meteo", ["Sole", "Pioggia", "Freddo", "Nuvole"])
    orario = st.time_input("Orario attuale")
    budget = st.select_slider("Budget di coppia", options=["€", "€€", "€€€"])

if not api_key:
    st.info("Per favore, inserisci l'API Key nella barra laterale per iniziare.")
    st.stop()

# Inizializzazione Client
client = genai.Client(api_key=api_key)

# DATI LUI & LEI
col_lui, col_lei = st.columns(2)

with col_lui:
    st.subheader("Lui 👤")
    stanchezza_lui = st.slider("Stanchezza (Lui)", 1, 10, 5, key="s_lui")
    mezzo_lui = st.selectbox("Mezzo preferito (Lui)", ["Piedi", "Mezzi", "Auto"], key="m_lui")

with col_lei:
    st.subheader("Lei 👤")
    stanchezza_lei = st.slider("Stanchezza (Lei)", 1, 10, 5, key="s_lei")
    mezzo_lei = st.selectbox("Mezzo preferito (Lei)", ["Piedi", "Mezzi", "Auto"], key="m_lei")

st.divider()

# LOGICA DI GENERAZIONE
if st.button("Genera Proposte per la Coppia ✨", use_container_width=True):
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
    
    try:
        with st.spinner('Interrogando Gemini...'):
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )
            st.markdown(response.text)
    except Exception as e:
        st.error(f"Errore durante la generazione: {e}")

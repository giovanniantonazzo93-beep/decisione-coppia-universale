import streamlit as st
from google import genai
import sys

# Configurazione iniziale
st.set_page_config(page_title="Decision Bot Universale", layout="wide")

# --- INTERFACCIA ---
st.title("🤖 Decision Bot Universale")
st.caption(f"Engine: Python {sys.version.split()[0]}")

with st.sidebar:
    st.header("1. Configurazione")
    api_key = st.text_input("Inserisci Google API Key", type="password")
    st.divider()
    st.header("2. Dettagli")
    citta = st.text_input("Città", value="Pesaro")
    meteo = st.selectbox("Meteo", ["Sole", "Pioggia", "Freddo", "Nuvole"])
    orario = st.time_input("Orario previsto")
    budget = st.select_slider("Budget di coppia", options=["€", "€€", "€€€"])

if not api_key:
    st.warning("Inserisci l'API Key nella sidebar.")
    st.stop()

# Inizializzazione Client
client = genai.Client(api_key=api_key, http_options={'api_version': 'v1'})
# --- PROFILI ---
col_lui, col_lei = st.columns(2)
with col_lui:
    st.subheader("Lui 👤")
    stanchezza_lui = st.slider("Stanchezza (Lui)", 1, 10, 5, key="s_lui")
    mezzo_lui = st.selectbox("Mezzo (Lui)", ["Piedi", "Mezzi", "Auto"], key="m_lui")

with col_lei:
    st.subheader("Lei 👤")
    stanchezza_lei = st.slider("Stanchezza (Lei)", 1, 10, 5, key="s_lei")
    mezzo_lei = st.selectbox("Mezzo (Lei)", ["Piedi", "Mezzi", "Auto"], key="m_lei")

# --- GENERAZIONE ---
if st.button("Genera Proposte ✨", use_container_width=True):
    prompt = f"""
    Agisci come un esperto local concierge a {citta}. 
    Pianifica 3 attività reali (Lui, Lei, Compromesso) considerando:
    Meteo: {meteo}, Orario: {orario}, Budget: {budget}.
    Lui: Stanchezza {stanchezza_lui}/10, Mezzo {mezzo_lui}.
    Lei: Stanchezza {stanchezza_lei}/10, Mezzo {mezzo_lei}.
    Includi nomi di posti reali a {citta}, orari e prezzi. Rispondi in Italiano.
    """
    
    try:
        with st.spinner('Consulto le stelle (e Gemini)...'):
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )
            if response.text:
                st.success("Trovato!")
                st.markdown(response.text)
    except Exception as e:
        st.error(f"Errore: {e}")

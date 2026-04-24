import streamlit as st
from google import genai
import sys

# Configurazione
st.set_page_config(page_title="Decision Bot 2026", layout="centered")

st.title("🤖 Decision Bot Universale")
st.caption(f"Running on Python {sys.version.split()[0]}")

# Sidebar per la Key
with st.sidebar:
    api_key = st.text_input("Google API Key", type="password")

if not api_key:
    st.warning("Inserisci l'API Key per continuare.")
    st.stop()

# Inizializzazione Client (Nuova libreria google-genai)
client = genai.Client(api_key=api_key)

# Input Utente
col1, col2 = st.columns(2)
with col1:
    citta = st.text_input("Città", "Pesaro")
    meteo = st.selectbox("Meteo", ["Sole", "Pioggia", "Freddo"])
with col2:
    budget = st.select_slider("Budget", ["€", "€€", "€€€"])
    stanchezza = st.slider("Stanchezza media coppia", 1, 10, 5)

if st.button("Genera Proposte ✨"):
    prompt = f"""
    Città: {citta}. Meteo: {meteo}. Budget: {budget}. Stanchezza: {stanchezza}/10.
    Fornisci 3 opzioni reali: una per lui, una per lei e un compromesso.
    Includi nomi di posti veri, orari e prezzi. Rispondi in Italiano.
    """
    
    try:
        with st.spinner("Consultando l'IA..."):
            # Nuova chiamata per Gemini 1.5 Flash
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )
            st.markdown(response.text)
    except Exception as e:
        st.error(f"Errore: {e}")

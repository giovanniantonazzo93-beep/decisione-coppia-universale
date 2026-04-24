import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Decision Bot", layout="centered")
st.title("🗺️ Decision Bot Universale")

with st.sidebar:
    st.header("Configurazione")
    api_key = st.text_input("Incolla la API Key", type="password")

st.subheader("🤵 LUI & 💃 LEI")
c1, c2 = st.columns(2)
with c1:
    stanc_lui = st.select_slider("Stanchezza Lui", options=list(range(1, 11)), value=5)
    budg_lui = st.radio("Budget Lui", ["€", "€€", "€€€"], horizontal=True)
    mezzo_lui = st.selectbox("Mezzo Lui", ["A piedi", "Mezzi", "Auto"])
with c2:
    stanc_lei = st.select_slider("Stanchezza Lei", options=list(range(1, 11)), value=5)
    budg_lei = st.radio("Budget Lei", ["€", "€€", "€€€"], horizontal=True)
    mezzo_lei = st.selectbox("Mezzo Lei", ["A piedi", "Mezzi", "Auto"])

citta = st.text_input("📍 Città", "Pesaro")
meteo = st.selectbox("🌦️ Meteo", ["Sole", "Pioggia", "Freddo"])

if st.button("🚀 TROVA COSA FARE"):
    if not api_key:
        st.error("Inserisci la chiave nella barra laterale!")
    else:
        try:
            genai.configure(api_key=api_key.strip())
            # Nome modello standard, senza fronzoli
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"Siamo a {citta} ({meteo}). Lui stanchezza {stanc_lui}, budget {budg_lui}. Lei stanchezza {stanc_lei}, budget {budg_lei}. Suggerisci 3 opzioni (Lui, Lei, Compromesso) con orari e prezzi. Rispondi in italiano."
            
            with st.spinner("Consulto l'oracolo..."):
                response = model.generate_content(prompt)
                st.markdown(response.text)
        except Exception as e:
            st.error(f"Errore: {e}")

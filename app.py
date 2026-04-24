import streamlit as st
import google.generativeai as genai
import os

# Configurazione API - Inserisci la tua chiave nei Secret di Streamlit o in un file .env
# genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

st.set_page_config(page_title="Decision Bot Universale", layout="centered")

def get_decision(city, time_of_day, weather, lui_data, lei_data):
    genai.configure(api_key=api_key) 
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Agisci come esperto local manager di {city}.
    Pianifica un'attività per una coppia:
    - Momento: {time_of_day}, Meteo: {weather}.
    - LUI: Stanchezza {lui_data['fatigue']}/10, Budget {lui_data['budget']}, Mezzo {lui_data['transport']}.
    - LEI: Stanchezza {lei_data['fatigue']}/10, Budget {lei_data['budget']}, Mezzo {lei_data['transport']}.

    PRODUCI 3 PROPOSTE REALI A {city} (Lui, Lei, Compromesso).
    Includi: Nome posto, Orario e Prezzo. Sii sintetico.
    """
    
    response = model.generate_content(prompt)
    return response.textt

# --- INTERFACCIA UI ---
st.title("🤖 Decision Bot Universale")
st.subheader("Basta indecisioni, decide l'IA.")

with st.sidebar:
    st.header("📍 Contesto")
    citta = st.text_input("Città", "Pesaro")
    orario = st.selectbox("Orario", ["Mattina", "Pomeriggio", "Sera", "Notte"])
    meteo = st.selectbox("Meteo", ["Sole", "Pioggia", "Freddo/Vento"])
    api_key = st.text_input("Google API Key", type="password")

col1, col2 = st.columns(2)

with col1:
    st.header("♂️ Lui")
    fatigue_lui = st.slider("Stanchezza Lui", 1, 10, 5)
    budget_lui = st.select_slider("Budget Lui", options=["€", "€€", "€€€"])
    mezzo_lui = st.selectbox("Mezzo Lui", ["Piedi", "Mezzi", "Auto"])

with col2:
    st.header("♀️ Lei")
    fatigue_lei = st.slider("Stanchezza Lei", 1, 10, 5)
    budget_lei = st.select_slider("Budget Lei", options=["€", "€€", "€€€"])
    mezzo_lei = st.selectbox("Mezzo Lei", ["Piedi", "Mezzi", "Auto"])

if st.button("Genera Soluzioni ✨"):
    if not api_key:
        st.error("Inserisci la tua API Key per continuare.")
    else:
        try:
            genai.configure(api_key=api_key)
            with st.spinner("Consultando le stelle (e le mappe)..."):
                lui = {"fatigue": fatigue_lui, "budget": budget_lui, "transport": mezzo_lui}
                lei = {"fatigue": fatigue_lei, "budget": budget_lei, "transport": mezzo_lei}
                
                risultato = get_decision(citta, orario, meteo, lui, lei)
                st.markdown("---")
                st.markdown(risultato)
        except Exception as e:
            st.error(f"Errore: {e}")

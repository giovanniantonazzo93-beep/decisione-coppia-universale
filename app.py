import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Decision Bot", layout="centered")

# --- INTERFACCIA ---
st.title("🗺️ Decision Bot Universale")

with st.sidebar:
    st.header("Configurazione")
    # Usiamo un nome diverso per la variabile per evitare conflitti
    chiave_input = st.text_input("Incolla la API Key qui", type="password")

st.subheader("🤵 LUI & 💃 LEI")
c1, c2 = st.columns(2)
with c1:
    stanc_lui = st.select_slider("Stanchezza Lui", options=list(range(1, 11)), value=5)
    mezzo_lui = st.selectbox("Mezzo Lui", ["A piedi", "Mezzi", "Auto"])
with c2:
    stanc_lei = st.select_slider("Stanchezza Lei", options=list(range(1, 11)), value=5)
    mezzo_lei = st.selectbox("Mezzo Lei", ["A piedi", "Mezzi", "Auto"])

citta = st.text_input("📍 Città", "Pesaro")
meteo = st.selectbox("🌦️ Meteo", ["Sole", "Pioggia", "Freddo"])

# --- LOGICA ---
if st.button("🚀 TROVA COSA FARE"):
    if not chiave_input:
        st.error("Manca la chiave nella barra laterale!")
    else:
        try:
            # Puliamo la chiave da eventuali spazi bianchi invisibili
            api_key_pulita = chiave_input.strip()
            genai.configure(api_key=api_key_pulita)
            
            # Usiamo il modello standard che ha funzionato nella tua chat
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"Siamo a {citta} ({meteo}). Lui stanchezza {stanc_lui}, Lei {stanc_lei}. Suggerisci 3 cose da fare reali (Lui, Lei, Compromesso) con orari e prezzi. Rispondi in italiano."
            
            with st.spinner("L'IA sta rispondendo..."):
                # Specifichiamo la sicurezza per evitare blocchi improvvisi
                response = model.generate_content(prompt)
                
                if response.text:
                    st.markdown("### Ecco i consigli per voi:")
                    st.write(response.text)
                else:
                    st.warning("Google ha risposto vuoto. Riprova tra un istante.")
                    
        except Exception as e:
            st.error(f"Errore tecnico: {e}")
            st.info("Controlla che la chiave non abbia spazi prima o dopo quando la incolli.")

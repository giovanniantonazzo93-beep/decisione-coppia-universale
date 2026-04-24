import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Decision Bot", layout="centered")

# --- INTERFACCIA ---
st.title("🗺️ Decision Bot Universale")

with st.sidebar:
    st.header("Configurazione")
    chiave_input = st.text_input("Incolla la API Key qui", type="password")
    st.info("La trovi su aistudio.google.com")

st.subheader("🤵 LUI & 💃 LEI")
c1, c2 = st.columns(2)
with c1:
    stanc_lui = st.select_slider("Stanchezza Lui", options=list(range(1, 11)), value=5)
    budg_lui = st.radio("Budget Lui", ["Economico", "Medio", "Lusso"], horizontal=True)
    mezzo_lui = st.selectbox("Mezzo Lui", ["A piedi", "Mezzi", "Auto"])
with c2:
    stanc_lei = st.select_slider("Stanchezza Lei", options=list(range(1, 11)), value=5)
    budg_lei = st.radio("Budget Lei", ["Economico", "Medio", "Lusso"], horizontal=True)
    mezzo_lei = st.selectbox("Mezzo Lei", ["A piedi", "Mezzi", "Auto"])

citta = st.text_input("📍 Città", "Pesaro")
meteo = st.selectbox("🌦️ Meteo", ["Sole", "Pioggia", "Freddo"])

# --- LOGICA ---
if st.button("🚀 TROVA COSA FARE"):
    if not chiave_input:
        st.error("Metti la chiave nella barra a sinistra!")
    else:
        try:
            # Pulizia chiave e configurazione
            api_key_pulita = chiave_input.strip()
            genai.configure(api_key=api_key_pulita)
            
            model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
            
            # Prompt super dettagliato con i budget
            prompt = f"""
            Siamo a {citta} ({meteo}). 
            LUI: stanchezza {stanc_lui}/10, budget {budg_lui}, mezzo {mezzo_lui}.
            LEI: stanchezza {stanc_lei}/10, budget {budg_lei}, mezzo {mezzo_lei}.
            Suggerisci 3 opzioni REALI (Lui, Lei, Compromesso).
            Usa un tono divertente ma preciso. Includi orari, prezzi medi e link.
            Rispondi in Italiano.
            """
            
            with st.spinner("Sto consultando l'oracolo..."):
                response = model.generate_content(prompt)
                st.markdown("### 💡 Ecco i miei consigli:")
                st.write(response.text)
                    
        except Exception as e:
            st.error(f"Errore: {e}")

import streamlit as st
import google.generativeai as genai

# Configurazione grafica
st.set_page_config(page_title="Global Couple Bot", layout="centered")
st.title("🗺️ Decision Bot Intelligente")
st.write("L'algoritmo che adatta il divertimento alla città e alla vostra stanchezza.")

# Sidebar per la configurazione
with st.sidebar:
    st.header("Configurazione")
    api_key = st.text_input("Inserisci la Gemini API Key", type="password")
    st.info("Prendila gratis su aistudio.google.com")

# --- INPUT LUI ---
st.subheader("🤵 PER LUI")
c1, c2, c3 = st.columns(3)
with c1: stanc_lui = st.select_slider("Stanchezza", options=list(range(1, 11)), value=5, key="l1")
with c2: budg_lui = st.select_slider("Budget", options=["$", "$$", "$$$"], value="$$", key="l2")
with c3: mezzo_lui = st.selectbox("Mezzo", ["A piedi", "Mezzi Pubblici", "Auto/Taxi"], key="l3")

# --- INPUT LEI ---
st.subheader("💃 PER LEI")
c4, c5, c6 = st.columns(3)
with c4: stanc_lei = st.select_slider("Stanchezza ", options=list(range(1, 11)), value=5, key="k1")
with c5: budg_lei = st.select_slider("Budget ", options=["$", "$$", "$$$"], value="$$", key="k2")
with c6: mezzo_lei = st.selectbox("Mezzo ", ["A piedi", "Mezzi Pubblici", "Auto/Taxi"], key="k3")

# --- CONTESTO ---
st.divider()
col_a, col_b = st.columns(2)
with col_a: citta = st.text_input("📍 Città attuale (es. Pesaro, Roma, Firenze)", "Pesaro")
with col_b: meteo = st.selectbox("🌦️ Meteo", ["Sole", "Pioggia", "Vento Forte", "Freddo"])

# ALGORITMO DISTANZA BASE (Verrà poi raffinato dall'IA)
def calcola_metri_base(stanc, mezzo):
    if mezzo == "A piedi":
        return 400 if stanc >= 8 else 1200 if stanc >= 4 else 3000
    elif mezzo == "Mezzi Pubblici":
        return 1000 if stanc >= 8 else 5000 if stanc >= 4 else 15000
    else: # Auto
        return 3000 if stanc >= 8 else 10000 if stanc >= 4 else 30000

m_lui = calcola_metri_base(stanc_lui, mezzo_lui)
m_lei = calcola_metri_base(stanc_lei, mezzo_lei)

# --- AZIONE ---
if st.button("🚀 TROVA COSA FARE"):
    if not api_key:
        st.error("Inserisci la API Key nella barra laterale!")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # PROVA AUTOMATICA DEI MODELLI (Così evitiamo l'errore 404)
            modelli_da_provare = ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-pro']
            model = None
            
            for nome_modello in modelli_da_provare:
                try:
                    m = genai.GenerativeModel(nome_modello)
                    # Facciamo un test rapidissimo per vedere se risponde
                    m.generate_content("test", generation_config={"max_output_tokens": 1})
                    model = m
                    break # Se arriviamo qui, il modello funziona!
                except:
                    continue # Se fallisce, prova il prossimo della lista
            
            if model is None:
                st.error("Nessun modello Gemini sembra rispondere. Controlla la tua API Key su Google AI Studio.")
            else:
                prompt = f"""
                Siamo a {citta}. Analizza questa città e il meteo ({meteo}).
                LUI: Stanchezza {stanc_lui}/10, Mezzo {mezzo_lui}.
                LEI: Stanchezza {stanc_lei}/10, Mezzo {mezzo_lei}.
                Trova 3 opzioni REALI (Lui, Lei, Compromesso).
                Dai orari, prezzi e link. Usa l'italiano.
                """
                
                with st.spinner(f"Cercando con {model.model_name}..."):
                    res = model.generate_content(prompt)
                    st.markdown(res.text)
                    
        except Exception as e:
            st.error(f"Errore tecnico: {e}")

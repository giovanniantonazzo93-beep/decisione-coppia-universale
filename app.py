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
           model = genai.GenerativeModel('gemini-pro')
            
            # IL PROMPT INTELLIGENTE CHE ANALIZZA LA CITTÀ
            prompt = f"""
            Siamo a {citta}. Analizza questa città: è una metropoli dispersiva o un centro raccolto? 
            Adatta i raggi d'azione di conseguenza (es. a Pesaro o Fano ci si sposta diversamente che a Roma).
            
            DATI ATTUALI:
            - Meteo: {meteo}
            - LUI: Stanchezza {stanc_lui}/10, Budget {budg_lui}, Mezzo {mezzo_lui}. Raggio indicativo: {m_lui} metri.
            - LEI: Stanchezza {stanc_lei}/10, Budget {budg_lei}, Mezzo {mezzo_lei}. Raggio indicativo: {m_lei} metri.
            
            PROPOSTE RICHIESTE (Reali e attive oggi):
            1. Opzione LUI (vicino a lui)
            2. Opzione LEI (vicino a lei)
            3. COMPROMESSO (media distanze e budget minimo)
            
            Spazia tra: Mostre, Cinema, Bowling, Musei, Parchi, Eventi temporanei, Ristoranti.
            Per ogni posto dai: NOME, PERCHÉ ANDARCI, ORARI, COSTI e LINK ufficiale.
            """
            
            with st.spinner(f"Analizzando {citta} e i vostri parametri..."):
                res = model.generate_content(prompt)
                st.markdown(res.text)
        except Exception as e:
            st.error(f"Si è verificato un errore: {e}")

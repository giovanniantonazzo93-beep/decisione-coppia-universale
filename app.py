import streamlit as st
import google.generativeai as genai
from streamlit_js_eval import get_geolocation

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="Decision Bot GPS", page_icon="📍", layout="centered")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; background-color: #007bff; color: white; }
    .reportview-container { background: #f0f2f6; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNZIONE LOGICA MORFOLOGICA ---
def get_urban_context(lat, lon):
    """
    Simulazione di analisi densità. 
    In una versione avanzata potresti usare reverse_geocoding per sapere il nome della città.
    Per ora passiamo il concetto di 'Elasticità' al prompt.
    """
    # Esempio: se non siamo a Roma/Milano, aumentiamo il raggio del 20-30%
    # Qui il bot chiederà a Gemini di valutare la città dalle coordinate.
    return {
        "morfologia_nota": "Valuta se la città è collinare (es. Siena) o densa (es. Roma).",
        "moltiplicatore": 1.2 # Il famoso +20% di base per città non metropolitane
    }

# --- SIDEBAR & API ---
st.sidebar.header("Impostazioni")
api_key = st.sidebar.text_input("Inserisci la tua Google API Key", type="password")

# --- RECUPERO GPS ---
st.sidebar.subheader("📍 Posizione")
modo_posizione = st.sidebar.radio("📍 Come troviamo la posizione?", ["GPS Live", "Inserimento Manuale"])

if modo_posizione == "GPS Live":
    loc = get_geolocation()
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        pos_context = f"Coordinate GPS: {lat}, {lon}."
        st.sidebar.success(f"Posizione acquisita: {lat:.4f}")
    else:
        pos_context = "Roma, Pigneto" # Fallback
else:
    citta = st.sidebar.text_input("Città", "Siena")
    quartiere = st.sidebar.text_input("Quartiere o Punto di riferimento", "Piazza del Campo")
    pos_context = f"Città: {citta}, Zona: {quartiere}."
loc = get_geolocation()

if loc:
    lat = loc['coords']['latitude']
    lon = loc['coords']['longitude']
    st.sidebar.success(f"Coordinate acquisite: {lat:.4f}, {lon:.4f}")
    pos_context = f"Coordinate GPS: {lat}, {lon}."
else:
    st.sidebar.info("In attesa del GPS... Fallback su Roma Pigneto.")
    pos_context = "Mi trovo a Roma, zona Pigneto."

# --- INTERFACCIA PRINCIPALE ---
st.title("🤖 Decision Bot GPS")
st.write("Risolviamo l'indecisione in base a stanchezza e morfologia urbana.")

with st.form("main_form"):
    col1, col2 = st.columns(2)
    with col1:
        orario = st.select_slider("🕒 Quando?", options=["Mattina", "Pomeriggio", "Sera", "Notte"], value="Sera")
        meteo = st.selectbox("☁️ Meteo attuale", ["Sole", "Pioggia", "Vento/Freddo"])
    with col2:
        budget = st.select_slider("💰 Budget", options=["€", "€€", "€€€"], value="€€")
        mezzo = st.selectbox("🚗 Come vi spostate?", ["A piedi", "Mezzi pubblici", "Auto"])

    st.divider()
    
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("**STATO LUI**")
        stanc_lui = st.slider("Stanchezza Lui", 1, 10, 5, key="sl")
    with c4:
        st.markdown("**STATO LEI**")
        stanc_lei = st.slider("Stanchezza Lei", 1, 10, 5, key="sk")
    
    submit = st.form_submit_button("Genera Proposte Localizzate")

# --- LOGICA GENERAZIONE ---
if submit:
    if not api_key:
        st.error("Inserisci la API Key nella barra laterale!")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-3-flash-preview')
            
            stanchezza_max = max(stanc_lui, stanc_lei)
            
            # PROMPT AGGIORNATO CON LOGICA DI ELASTICITÀ
            prompt = f"""
            Agisci come il Decision Bot Universale per coppie. 
            POSIZIONE: {pos_context}
            
            DATI COPPIA:
            - Stanchezza Lui: {stanc_lui}/10, Stanchezza Lei: {stanc_lei}/10
            - Budget: {budget} | Meteo: {meteo} | Mezzo: {mezzo}
            
            ISTRUZIONI GEOGRAFICHE (Morfologia Urbana):
            1. Identifica la città dalle coordinate o dal contesto.
            2. Applica il 'Coefficiente di Elasticità Urbana': 
               - In città iper-dense (Roma, Milano), raggio massimo 500-800m se stanchezza > 7.
               - In città con morfologia complessa o bassa densità (es. Siena, borghi, periferie), aumenta il raggio di spostamento del 20-30% rispetto allo standard, perché i punti di interesse sono più radi.
            3. Se la stanchezza di uno dei due è > 8, privilegia posti con pochissimo dislivello o raggiungibili senza sforzo.

            REGOLE DI OUTPUT:
            - Fornisci 3 opzioni REALI: [LUI], [LEI] e [IL COMPROMESSO].
            - Usa un tono ironico e intelligente.
            - Niente cliché turistici.
            
            FORMATO:
            - **Nome del Posto** (Indirizzo)
            - **Distanza e Pendenza**: Indica i metri e se c'è molta salita (importante per città come Siena).
            - **Link**: [Google Maps](https://www.google.com/maps/search/?api=1&query={{nome_posto_indirizzo}})
            """

            with st.spinner("Analizzando la morfologia della zona..."):
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Errore: {e}")

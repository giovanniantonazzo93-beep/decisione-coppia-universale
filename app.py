import streamlit as st
import google.generativeai as genai
from streamlit_js_eval import get_geolocation

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="Decision Bot GPS", page_icon="📍", layout="centered")

# CSS per rendere l'interfaccia più pulita
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; background-color: #007bff; color: white; }
    .reportview-container { background: #f0f2f6; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR & API ---
st.sidebar.header("Impostazioni")
api_key = st.sidebar.text_input("Inserisci la tua Google API Key", type="password")

# --- RECUPERO GPS ---
st.sidebar.subheader("📍 Posizione")
# Questa funzione attiva la richiesta di permessi nel browser
loc = get_geolocation()

if loc:
    lat = loc['coords']['latitude']
    lon = loc['coords']['longitude']
    st.sidebar.success(f"Coordinate acquisite: {lat:.4f}, {lon:.4f}")
    pos_context = f"Mi trovo esattamente a queste coordinate GPS: {lat}, {lon}."
else:
    st.sidebar.info("In attesa del GPS... Assicurati di aver dato il permesso al browser.")
    # Fallback se il GPS fallisce (es. utente nega il permesso)
    pos_context = "Mi trovo a Roma, zona Pigneto."

# --- INTERFACCIA PRINCIPALE ---
st.title("🤖 Decision Bot GPS")
st.write("Risolviamo l'indecisione senza farvi fare chilometri inutili.")

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
            # Utilizziamo l'alias 'latest' per essere sempre aggiornati
            model = genai.GenerativeModel('gemini-flash-latest')
            
            # Prompt super-dettagliato per evitare Trastevere se sei al Pigneto
            prompt = f"""
            Agisci come un esperto local di Roma. 
            POSIZIONE ATTUALE: {pos_context}
            
            DATI:
            - Orario: {orario}
            - Meteo: {meteo}
            - Budget: {budget}
            - Mezzo di trasporto: {mezzo}
            - Stanchezza media: {(stanc_lui + stanc_lei)/2}/10.
            
            REGOLE RIGIDE:
            1. Trova posti REALI e APERTI nel raggio di massimo 1-2 km dalla posizione indicata. 
            2. Se la stanchezza è alta (>7), proponi solo posti a meno di 10 minuti a piedi.
            3. Evita i soliti posti turistici (niente Centro/Trastevere se sono al Pigneto).
            4. Le 3 proposte (Lui, Lei, Compromesso) devono essere diverse tra loro (es: un bar, un locale con musica, un bistrot).
            
            FORMATO OUTPUT:
            Per ogni proposta scrivi:
            - **Nome del Posto** (con indirizzo)
            - **Perché andarci** (in relazione alla stanchezza e meteo)
            - **Distanza stimata**
            - **Link Google Maps** (genera un link del tipo https://www.google.com/maps/search/?api=1&query=Nome+Posto+Roma)
            """

            with st.spinner("Cercando i posti migliori vicino a te..."):
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Si è verificato un errore: {e}")

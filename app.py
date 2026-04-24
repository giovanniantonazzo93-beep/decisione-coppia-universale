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

# --- RECUPERO GPS ---
st.sidebar.subheader("📍 Posizione")
modo_posizione = st.sidebar.radio("Scegli come localizzarvi:", ["GPS Live", "Inserimento Manuale"])

if modo_posizione == "GPS Live":
    loc = get_geolocation()
    if loc:
        lat = loc['coords']['latitude']
        lon = loc['coords']['longitude']
        st.sidebar.success(f"Coordinate acquisite: {lat:.4f}, {lon:.4f}")
        pos_context = f"Mi trovo esattamente a queste coordinate GPS: {lat}, {lon}."
    else:
        st.sidebar.info("In attesa del GPS... Assicurati di aver dato i permessi al browser.")
        pos_context = "Mi trovo a Roma, zona Pigneto."
else:
    citta = st.sidebar.text_input("Città", "Siena")
    quartiere = st.sidebar.text_input("Quartiere o Punto di riferimento", "Piazza del Campo")
    pos_context = f"Mi trovo a {citta}, zona {quartiere}."

with st.form("main_form"):
    # --- NUOVA SEZIONE ATTIVITÀ ---
    st.subheader("🎯 Cosa vi va di fare?")
    opzioni_attivita = ["Tutto", "Cibo (Ristoranti/Trattorie)", "Bere (Cocktail/Wine Bar)", "Cultura (Musei/Eventi)", "Relax (Parchi/Librerie)", "Shopping"]
    
    col_a, col_b = st.columns([2, 1])
    with col_a:
        categorie = st.multiselect("Selezionate una o più categorie:", options=opzioni_attivita, default=["Tutto"])
    with col_b:
        stupiscimi = st.toggle("🎰 Stupiscimi!")

    st.divider()

    # --- LOGISTICA ---
    col1, col2 = st.columns(2)
    with col1:
        orario = st.select_slider("🕒 Quando?", options=["Mattina", "Pomeriggio", "Sera", "Notte"], value="Sera")
        meteo = st.selectbox("☁️ Meteo attuale", ["Sole", "Pioggia", "Vento/Freddo"])
    with col2:
        budget = st.select_slider("💰 Budget", options=["€", "€€", "€€€"], value="€€")
        mezzo = st.selectbox("🚗 Come vi spostate?", ["A piedi", "Mezzi pubblici", "Auto"])

    st.divider()
    
    # --- STANCHEZZA ---
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
            
            # --- AGGIUNTA LOGICA ATTIVITÀ ---
            if stupiscimi:
                istr_att = "MODALITÀ STUPISCIMI: Ignora la noia. Proponi qualcosa di bizzarro, insolito o segreto."
            elif "Tutto" in categorie or not categorie:
                istr_att = "Cerca tra qualsiasi attività (cibo, cultura, relax, shopping)."
            else:
                istr_att = f"Concentrati esclusivamente su queste categorie: {', '.join(categorie)}."
            
            # --- BLOCCO UNIFICATO: LOGICA + CATTIVERIA ---
            prompt = f"""
            Agisci come il 'Decision Bot Cinico'. Sei un esperto locale sarcastico e arrogante che non sopporta la pigrizia delle coppie.
            
            POSIZIONE: {pos_context}
            
            DATI COPPIA:
            - Stanchezza: Lui {stanc_lui}/10, Lei {stanc_lei}/10.
            - Budget: {budget} | Meteo: {meteo} | Mezzo: {mezzo}
            - Attività richiesta: {istr_att}

            ISTRUZIONI GEOGRAFICHE (Morfologia Urbana):
            1. Se la stanchezza massima supera il livello 7, il raggio di ricerca deve essere tra 500 e 800 metri. 
            2. Applica il 'Coefficiente di Elasticità Urbana': In città dense come Roma o Milano sii rigido sul raggio. In città come Siena o borghi collinari, aumenta il raggio del 20 percento ma insultali per la pendenza e la loro scarsa resistenza fisica.
            3. Se la stanchezza di uno dei due supera 8, privilegia posti senza dislivello (niente salite).
            4. Se piove, proponi solo posti al chiuso: non sono anatre.

            REGOLE DI RISPOSTA:
            - Esordisci con un commento acido sulla loro situazione (meteo, stanchezza o budget).
            - Fornisci 3 opzioni REALI: [LUI], [LEI] e [IL COMPROMESSO].
            - Usa un tono irriverente, intelligente e cinico.

            FORMATO OUTPUT:
            - **[NOME POSTO]** (Indirizzo)
            - **Fisica**: Distanza e pendenza (es. 400 metri di sofferenza).
            - **Il Verdetto**: Il tuo commento cattivo sul perché dovrebbero andarci.
            - **Link**: [Google Maps](https://www.google.com/maps/search/?api=1&query={pos_context.replace(' ', '+')})
            """

            with st.spinner("Analizzando la morfologia della zona..."):
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Errore: {e}")

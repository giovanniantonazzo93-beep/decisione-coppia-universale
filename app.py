import streamlit as st
import google.generativeai as genai
from streamlit_js_eval import get_geolocation

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="Decision Bot GPS", page_icon="📍", layout="centered")

# CSS "IMPATTO TOTALE": Ingrandisce slider, selettori e bottoni
st.markdown("""
    <style>
    /* Sfondo e font */
    .stApp {
        background-color: #f8f9fa !important;
    }

    /* TRASFORMAZIONE SLIDER: Rendiamo i pallini e le linee giganti */
    .stSlider [data-baseweb="slider"] {
        height: 20px !important;
        margin-bottom: 30px !important;
    }
    .stSlider [role="slider"] {
        width: 30px !important;
        height: 30px !important;
        background-color: #FF4B4B !important;
    }

    /* SELETTORI (Selectbox e Multiselect) */
    .stSelectbox div[data-baseweb="select"], .stMultiSelect div[data-baseweb="select"] {
        min-height: 60px !important;
        font-size: 18px !important;
    }

    /* IL BOTTONE: Ora è un vero pulsante da app */
    div.stButton > button {
        width: 100% !important;
        height: 80px !important;
        border-radius: 15px !important;
        background-color: #FF4B4B !important;
        color: white !important;
        font-size: 24px !important;
        font-weight: 800 !important;
        border: none !important;
        box-shadow: 0px 10px 20px rgba(255, 75, 75, 0.4) !important;
        margin-top: 30px !important;
        text-transform: uppercase !important;
    }

    /* TITOLI E ETICHETTE: Basta scritte piccole */
    label p {
        font-size: 20px !important;
        font-weight: bold !important;
        color: #1E1E1E !important;
    }
    
    .stSubheader p {
        font-size: 22px !important;
        color: #FF4B4B !important;
        font-weight: bold !important;
    }

    /* Nasconde i menu di sistema per pulizia */
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- INIZIALIZZAZIONE (Mettilo subito dopo il CSS) ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'dati' not in st.session_state:
    st.session_state.dati = {}

def avanti():
    st.session_state.step += 1

# --- LOGICA DELLE PAGINE ---

# STEP 1: POSIZIONE
if st.session_state.step == 1:
    st.subheader("📍 Dove siete finiti?")
    modo = st.radio("Scegli come localizzarvi:", ["GPS Live", "Inserimento Manuale"])
    
    if modo == "GPS Live":
        loc = get_geolocation()
        if loc:
            st.session_state.dati['pos'] = f"{loc['coords']['latitude']}, {loc['coords']['longitude']}"
            st.success("Vi ho trovati. Purtroppo.")
            st.button("Avanti ➔", on_click=avanti)
        else:
            st.info("Sto cercando il GPS... se non lo trovo è colpa del vostro telefono scadente.")
    else:
        citta = st.text_input("Città", "Roma")
        st.session_state.dati['pos'] = citta
        st.button("Conferma Città ➔", on_click=avanti)

# STEP 2: QUANDO E METEO
elif st.session_state.step == 2:
    st.subheader("🕒 Momento e Meteo")
    orario = st.select_slider("Quando?", options=["Mattina", "Pomeriggio", "Sera", "Notte"])
    meteo = st.selectbox("☁️ Com'è fuori?", ["Sole", "Pioggia", "Vento/Freddo"])
    
    st.session_state.dati['orario'] = orario
    st.session_state.dati['meteo'] = meteo
    
    if meteo == "Pioggia":
        st.warning("Piove? Che peccato, vi bagnerete i capelli costosi.")
    
    st.button("Prossimo passo ➔", on_click=avanti)

# STEP 3: BUDGET
elif st.session_state.step == 3:
    st.subheader("💰 Il portafoglio")
    budget = st.select_slider("Budget", options=["€", "€€", "€€€"])
    st.session_state.dati['budget'] = budget
    
    if budget == "€":
        st.error("Budget minimo? Siete i soliti spiantati.")
    elif budget == "€€€":
        st.info("Oh, abbiamo dei ricchi qui. Vediamo di non sprecarli tutti in una volta.")
        
    st.button("Continua l'agonia ➔", on_click=avanti)

# STEP 4: STANCHEZZA (ENTRAMBI)
elif st.session_state.step == 4:
    st.subheader("😫 Livello di sopportazione")
    stanc_lui = st.slider("Stanchezza Lui", 1, 10, 5)
    stanc_lei = st.slider("Stanchezza Lei", 1, 10, 5)
    
    st.session_state.dati['lui'] = stanc_lui
    st.session_state.dati['lei'] = stanc_lei
    
    if stanc_lui > 8 or stanc_lei > 8:
        st.warning("Siete quasi morti. Forse dovreste restare sul divano, ma io vi farò uscire comunque.")
        
    st.button("Quasi finita ➔", on_click=avanti)

# STEP 5: MEZZO
elif st.session_state.step == 5:
    st.subheader("🚗 Trasporto")
    mezzo = st.selectbox("Come vi muovete?", ["A piedi", "Mezzi pubblici", "Auto"])
    st.session_state.dati['mezzo'] = mezzo
    
    if mezzo == "A piedi":
        st.write("A piedi? Spero abbiate scarpe comode e polmoni nuovi.")
        
    st.button("Ultimo sforzo ➔", on_click=avanti)

# STEP 6: CATEGORIE O STUPISCIMI
elif st.session_state.step == 6:
    st.subheader("🎯 Cosa volete?")
    opzioni = ["Tutto", "Cibo", "Bere", "Cultura", "Relax"]
    categorie = st.multiselect("Categorie:", options=opzioni, default=["Tutto"])
    
    if st.button("🎰 STUPISCIMI!"):
        st.session_state.dati['stupiscimi'] = True
        st.session_state.dati['cat'] = "Qualcosa di assurdo"
        avanti()
        st.rerun()
        
    if st.button("GENERA OPZIONI"):
        st.session_state.dati['stupiscimi'] = False
        st.session_state.dati['cat'] = categorie
        avanti()
        st.rerun()

# STEP 7: RISULTATO FINALE
elif st.session_state.step == 7:
    # Qui richiamiamo Gemini (come nel codice precedente)
    # Alla fine mettiamo un tasto per ricominciare
    if st.button("Ricomincia il calvario"):
        st.session_state.step = 1
        st.rerun()

# Mantieni la tua API KEY nella barra laterale
api_key = st.sidebar.text_input("Inserisci Gemini API Key", type="password")
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
        st.error("Inserisci la API Key nella barra laterale, pigro!")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Calcolo stanchezza massima per decidere il raggio
            stanchezza_max = max(stanc_lui, stanc_lei)
            
            # Regola raggio Python 3.14 (simboli ok nel codice, parole nelle stringhe)
            raggio_calcolato = 800
            if stanchezza_max > 7:
                raggio_calcolato = 500

            # Logica Attività
            if stupiscimi:
                istr_att = "MODALITÀ STUPISCIMI: Proponi qualcosa di bizzarro o insolito."
            elif "Tutto" in categorie or not categorie:
                istr_att = "Qualsiasi attività (cibo, cultura, relax)."
            else:
                istr_att = f"Solo queste categorie: {', '.join(categorie)}."
            
            # Il Prompt Cinico definitivo
            prompt = f"""
            Agisci come il 'Decision Bot Cinico'. Sei sarcastico e arrogante.
            POSIZIONE: {pos_context}
            DATI COPPIA: Stanchezza Lui {stanc_lui}, Lei {stanc_lei}. Budget {budget}. Meteo {meteo}.
            ATTIVITÀ: {istr_att}
            
            LOGICA GEOGRAFICA:
            1. Il raggio massimo è di {raggio_calcolato} metri.
            2. Se siamo in un borgo o città collinare, aumenta il raggio del 20 percento ma insultali per la pendenza.
            
            FORMATO OUTPUT:
            - Esordio acido sulla loro condizione.
            - 3 opzioni REALI (Nome, Distanza, Il Verdetto cattivo).
            - Link Google Maps.
            """

            with st.spinner("Sto cercando... spero ne valga la pena."):
                response = model.generate_content(prompt)
                st.divider()
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Errore critico: {e}")

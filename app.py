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

import random

# --- DATABASE DI INSULTI ---
insulti_pos = [
    "GPS? Davvero non sapete nemmeno dove vi trovate? Imbarazzante.",
    "Ah, cercate aiuto da un satellite perché il vostro senso dell'orientamento è nullo.",
    "Vi ho trovati. Purtroppo non posso farvi sparire, quindi andiamo avanti.",
    "Coordinate ricevute. Il satellite ha appena riso della vostra posizione."
]

insulti_meteo = {
    "Sole": ["C'è il sole, ma scommetto che troverete comunque il modo di sudare e lamentarvi.", "☀️ Il sole splende su tutti, tranne che sul vostro buon umore."],
    "Pioggia": ["Piove. Spero che i vostri capelli non siano fatti di zucchero.", "☔️ Piove. Il meteo si adegua alla vostra allegria contagiosa."],
    "Vento/Freddo": ["Fa freddo. Copritevi, che non ho voglia di chiamare un'ambulanza.", "❄️ Vento e gelo. Ideale per gelare quel poco di cervello che vi è rimasto."]
}

insulti_budget = {
    "€": ["Budget da fame. Spero vi piacciano i campioni omaggio.", "Siete i soliti spiantati, eh?", "A pane e acqua si risparmia un sacco, sapete?"],
    "€€": ["La classe media colpisce ancora. Che scelta mediocre.", "Né ricchi né poveri. Solo... insipidi.", "Il giusto mezzo. Ovvero: non sapete cosa volete."],
    "€€€": ["Oh, guardate i nuovi ricchi!", "Volete buttare soldi? Dateli a me invece di mangiarveli.", "Spero che il lusso colmi il vostro vuoto interiore."]
}

insulti_stanchezza = {
    "riposati": ["Siete freschi come rose. Andate a correre una maratona invece di stressare me.", "Troppa energia. Mi fate venire il mal di testa."],
    "medi": ["Siete nella terra di nessuno. Praticamente dei mobili dell'IKEA.", "Né vivi né morti. La definizione perfetta di noia."],
    "distrutti": ["Praticamente due cadaveri. Restate a casa a fissare il soffitto, fate prima.", "Siete così stanchi che Gemini vi consiglierà un letto d'ospedale."]
}

insulti_mezzi = {
    "A piedi": ["A piedi? Spero abbiate scarpe comode e polmoni di ricambio.", "👟 Camminare fa bene, dicono. A voi servirebbe un miracolo."],
    "Mezzi pubblici": ["Mezzi pubblici? Preparatevi a odiare l'umanità più del solito.", "🚌 Ah, l'ebbrezza dell'autobus pieno. Buona fortuna."],
    "Auto": ["In auto? Pigri e inquinatori. Almeno non dovrete camminare, poverini.", "🚗 Spero che passiate mezz'ora a cercare parcheggio."]
}

# --- ORA LA LOGICA DI NAVIGAZIONE ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'dati' not in st.session_state:
    st.session_state.dati = {}

def avanti():
    st.session_state.step += 1

# --- INIZIALIZZAZIONE ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'dati' not in st.session_state:
    st.session_state.dati = {}

def avanti():
    st.session_state.step += 1

# --- LOGICA DELLE PAGINE ---

# --- STEP 1: POSIZIONE ---
if st.session_state.step == 1:
    st.subheader("📍 Dove siete finiti?")
    modo = st.radio("Scegli come localizzarvi:", ["GPS Live", "Inserimento Manuale"])
    
    if modo == "GPS Live":
        loc = get_geolocation()
        if loc:
            st.session_state.dati['pos'] = f"{loc['coords']['latitude']}, {loc['coords']['longitude']}"
            st.success("Vi ho trovati. Purtroppo.")
            st.write(f"🤖 {random.choice(insulti_pos)}")
            st.button("Avanti ➔", on_click=avanti)
        else:
            st.info("In attesa del GPS... muovetevi o date i permessi!")
    else:
        citta = st.text_input("Città", "Roma")
        st.session_state.dati['pos'] = citta
        st.write(f"🤖 {random.choice(insulti_pos)}")
        st.button("Conferma Città ➔", on_click=avanti)

# --- STEP 2: METEO ---
elif st.session_state.step == 2:
    st.subheader("🕒 Il momento del disagio")
    orario = st.select_slider("Quando?", options=["Mattina", "Pomeriggio", "Sera", "Notte"])
    meteo = st.selectbox("Meteo attuale", ["Sole", "Pioggia", "Vento/Freddo"])
    
    st.session_state.dati['orario'] = orario
    st.session_state.dati['meteo'] = meteo
    
    st.divider()
    st.write(f"🤖 {random.choice(insulti_meteo[meteo])}")
    st.button("Vediamo il resto ➔", on_click=avanti)

# --- STEP 3: BUDGET ---
elif st.session_state.step == 3:
    st.subheader("💰 Quanti soldi volete sprecare?")
    budget = st.select_slider("Budget", options=["€", "€€", "€€€"])
    st.session_state.dati['budget'] = budget
    
    st.divider()
    st.info(f"🤖 {random.choice(insulti_budget[budget])}")
    st.button("Continua l'agonia ➔", on_click=avanti)

# --- STEP 4: STANCHEZZA ---
elif st.session_state.step == 4:
    st.subheader("😫 Livello di agonia")
    l = st.slider("Stanchezza Lui", 1, 10, 5)
    s = st.slider("Stanchezza Lei", 1, 10, 5)
    st.session_state.dati.update({'lui': l, 'lei': s})
    
    media = (l + s) / 2
    if media <= 4: cat = "riposati"
    elif media <= 7: cat = "medi"
    else: cat = "distrutti"
    
    st.divider()
    st.write(f"🤖 {random.choice(insulti_stanchezza[cat])}")
    st.button("Quasi finito ➔", on_click=avanti)

# --- STEP 5: MEZZI ---
elif st.session_state.step == 5:
    st.subheader("🚗 Come volete trascinarvi?")
    mezzo = st.selectbox("Spostamento", ["A piedi", "Mezzi pubblici", "Auto"])
    st.session_state.dati['mezzo'] = mezzo
    
    st.divider()
    st.write(f"🤖 {random.choice(insulti_mezzi[mezzo])}")
    st.button("Ultima scelta ➔", on_click=avanti)

# --- STEP 6: CATEGORIE E GENERAZIONE ---
elif st.session_state.step == 6:
    st.subheader("🎯 Cosa cercate?")
    categorie = st.multiselect("Seleziona:", ["Cibo", "Bere", "Cultura", "Relax"], default=["Cibo"])
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎰 STUPISCIMI!"):
            st.session_state.dati['stupiscimi'] = True
            st.session_state.dati['cat'] = "Qualcosa di bizzarro"
            st.session_state.step = 7
            st.rerun()
    with col2:
        if st.button("GENERA OPZIONI"):
            st.session_state.dati['stupiscimi'] = False
            st.session_state.dati['cat'] = categorie
            st.session_state.step = 7
            st.rerun()

# --- STEP 7: IL VERDETTO (Gemini entra in azione) ---
elif st.session_state.step == 7:
    st.subheader("🔮 Il Verdetto del Bot")
    
    if not api_key:
        st.error("Inserisci la API Key nella barra laterale, o non muoverò un dito!")
        if st.button("Torna indietro"):
            st.session_state.step = 6
            st.rerun()
    


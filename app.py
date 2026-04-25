import streamlit as st
import google.generativeai as genai
from streamlit_js_eval import get_geolocation

# --- RECUPERO CHIAVE SEGRETA ---
api_key = st.secrets["GEMINI_KEY"]

# --- CONFIGURAZIONE ---
st.set_page_config(
    page_title="Judgmental Genius", # Oppure "Bitter Oracle" o "The Harsh Reality"
    page_icon="🤖", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

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

# --- CONFIGURAZIONE NAVIGAZIONE E DIARIO (UNICO BLOCCO) ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'dati' not in st.session_state:
    st.session_state.dati = {}
if 'commento_ai' not in st.session_state:
    st.session_state.commento_ai = "Benvenuto. Vediamo di che morte dovete morire."

def avanti():
    st.session_state.step += 1
    st.rerun()

def indietro():
    st.session_state.step -= 1
    st.rerun()

# --- DISPLAY FISSO PER IL TELEFONO ---
# Questa riga mostra il commento del bot in alto in ogni pagina
st.info(f"🤖 {st.session_state.commento_ai}")

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
    
    # Usiamo la key per l'orario
    orario = st.select_slider("Quando?", options=["Mattina", "Pomeriggio", "Sera", "Notte"], key="sel_orario")
    
    # Usiamo la key per il meteo e aggiorniamo istantaneamente il commento
    meteo = st.selectbox("Meteo attuale", ["Sole", "Pioggia", "Vento/Freddo"], key="sel_meteo")
    
    # Il commento ora legge direttamente dalla key della selectbox
    st.session_state.commento_ai = random.choice(insulti_meteo[st.session_state.sel_meteo])
    
    st.divider()
    
    if st.button("⬅ Indietro"):
        indietro()

    if st.button("Vediamo il resto ➔"):
        # Salviamo i valori definitivi dalle key
        st.session_state.dati['orario'] = st.session_state.sel_orario
        st.session_state.dati['meteo'] = st.session_state.sel_meteo
        avanti()

# --- STEP 3: BUDGET ---
elif st.session_state.step == 3:
    st.subheader("💰 Quanti soldi volete sprecare?")
    
    # Usiamo la key per il budget
    budget = st.select_slider("Budget", options=["€", "€€", "€€€"], key="sel_budget")
    
    # Il commento legge istantaneamente dalla key del selettore
    st.session_state.commento_ai = random.choice(insulti_budget[st.session_state.sel_budget])
    
    st.divider()
    
    if st.button("⬅ Indietro"):
        indietro()

    if st.button("Continua l'agonia ➔"):
        # Salviamo il valore definitivo dalla key
        st.session_state.dati['budget'] = st.session_state.sel_budget
        avanti()

# --- STEP 4: STANCHEZZA ---
elif st.session_state.step == 4:
    st.subheader("😫 Livello di agonia")
    
    # Usiamo le key per i cursori
    l = st.slider("Stanchezza Lui", 1, 10, 5, key="sel_lui")
    s = st.slider("Stanchezza Lei", 1, 10, 5, key="sel_lei")
    
    # Calcoliamo la categoria leggendo direttamente dalle key per evitare ritardi
    media_live = (st.session_state.sel_lui + st.session_state.sel_lei) / 2
    
    if media_live <= 4:
        cat_live = "riposati"
    elif media_live <= 7:
        cat_live = "medi"
    else:
        cat_live = "distrutti"
    
    # Aggiornamento istantaneo del commento basato sui cursori
    st.session_state.commento_ai = random.choice(insulti_stanchezza[cat_live])
    
    st.divider()
    
    if st.button("⬅ Indietro"):
        indietro()

    if st.button("Quasi finito ➔"):
        # Salviamo i valori definitivi
        st.session_state.dati.update({'lui': st.session_state.sel_lui, 'lei': st.session_state.sel_lei})
        avanti()
# --- STEP 5: MEZZI ---
elif st.session_state.step == 5:
    st.subheader("🚗 Come volete trascinarvi?")
    
    # Usiamo la key per agganciare subito la scelta del mezzo
    mezzo = st.selectbox("Spostamento", ["A piedi", "Mezzi pubblici", "Auto"], key="sel_mezzo")
    
    # Il commento legge istantaneamente il valore aggiornato dalla key
    st.session_state.commento_ai = random.choice(insulti_mezzi[st.session_state.sel_mezzo])
    
    st.divider()
    
    if st.button("⬅ Indietro"):
        indietro()

    if st.button("Ultima scelta ➔"):
        # Salviamo il mezzo definitivo
        st.session_state.dati['mezzo'] = st.session_state.sel_mezzo
        avanti()

# --- STEP 6: CATEGORIE E GENERAZIONE ---
elif st.session_state.step == 6:
    st.subheader("🎯 Cosa cercate?")
    
    # Usiamo la key per le categorie
    categorie = st.multiselect("Seleziona:", ["Cibo", "Bere", "Cultura", "Relax"], default=["Cibo"], key="sel_categorie")
    
    if st.button("⬅ Indietro"):
        indietro()
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎰 STUPISCIMI!"):
            st.session_state.dati['stupiscimi'] = True
            st.session_state.dati['cat'] = "Qualcosa di bizzarro"
            # Il commento viene impostato un istante prima del salto allo step 7
            st.session_state.commento_ai = "Oh, cercate l'effetto wow? Preparatevi a rimanere delusi."
            st.session_state.step = 7
            st.rerun()
            
    with col2:
        if st.button("GENERA OPZIONI"):
            st.session_state.dati['stupiscimi'] = False
            # Salviamo le categorie scelte dalla key
            st.session_state.dati['cat'] = st.session_state.sel_categorie
            st.session_state.commento_ai = "Analizzo le vostre mediocri opzioni... un momento."
            st.session_state.step = 7
            st.rerun()

# --- STEP 7: IL VERDETTO (Gemini entra in azione) ---
elif st.session_state.step == 7:
    st.subheader("🔮 Il Verdetto del Bot")
    
    d = st.session_state.dati
    
    # Verifichiamo se dobbiamo ancora generare la risposta definitiva
    if "Analizzo" in st.session_state.commento_ai or "Oh, cercate" in st.session_state.commento_ai:
        try:
            genai.configure(api_key=api_key) 
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Calcolo raggio basato sulla stanchezza salvata
            stanchezza_max = max(d.get('lui', 5), d.get('lei', 5))
            raggio = 500 if stanchezza_max > 7 else 800

            prompt = f"""
            Agisci come il 'Decision Bot Cinico'. Sei sarcastico e arrogante.
            POSIZIONE ATTUALE: {d.get('pos')}
            DATI COPPIA: Stanchezza Lui {d.get('lui')}/10, Lei {d.get('lei')}/10. 
            Budget: {d.get('budget')}. Meteo: {d.get('meteo')}. Mezzo: {d.get('mezzo')}.
            ATTIVITÀ RICHIESTE: {d.get('cat')}
            
            LOGICA GEOGRAFICA:
            1. Suggerisci posti reali entro un raggio di {raggio} metri dalla posizione fornita.
            2. Se la zona è collinare, aumenta il raggio del 20% ma insultali per la fatica che faranno.
            
            FORMATO OUTPUT:
            - Esordio acido sulla loro condizione.
            - 3 opzioni REALI (Nome, Distanza approssimativa, Il Verdetto cattivo).
            - Link Google Maps per ognuna.
            """

            with st.spinner("Sto decidendo il vostro destino... spero sia tragico."):
                response = model.generate_content(prompt)
                # Sostituiamo il commento temporaneo con la sentenza finale di Gemini
                st.session_state.commento_ai = response.text
                st.rerun()
                
        except Exception as e:
            st.error(f"Errore: Il Genio ha avuto un travaso di bile. Dettaglio: {e}")

    # Visualizzazione della sentenza finale (Markdown per link e grassetti)
    st.markdown(st.session_state.commento_ai)

    st.divider()
    
    # Bottone per resettare tutto e ricominciare
    if st.button("Ricomincia il calvario"):
        st.session_state.step = 1
        st.session_state.dati = {}
        st.session_state.commento_ai = "Bentornati. Pronti per un altro giro di umiliazioni?"
        st.rerun()
    


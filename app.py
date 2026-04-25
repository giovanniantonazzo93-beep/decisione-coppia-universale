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
    
    # Funzione per cambiare l'insulto solo quando serve
    def nuovo_insulto_pos():
        st.session_state.commento_ai = random.choice(insulti_pos)

    modo = st.radio("Scegli come localizzarvi:", ["GPS Live", "Inserimento Manuale"], key="modo_pos", on_change=nuovo_insulto_pos)
    
    if modo == "GPS Live":
        loc = get_geolocation()
        if loc:
            st.session_state.dati['pos'] = f"{loc['coords']['latitude']}, {loc['coords']['longitude']}"
            st.success("Vi ho trovati. Purtroppo.")
            # Se non c'è ancora un commento, ne mettiamo uno
            if "commento_ai" not in st.session_state or st.session_state.commento_ai == "Bentornati...":
                nuovo_insulto_pos()
            
            st.write(f"🤖 {st.session_state.commento_ai}")
            
            if st.button("Avanti ➔"):
                avanti()
        else:
            st.info("In attesa del GPS... muovetevi o date i permessi!")
    else:
        # Inserimento manuale
        citta = st.text_input("Città o indirizzo", value=st.session_state.dati.get('pos', 'Roma'), key="input_citta")
        
        # Generiamo l'insulto solo se l'utente ha scritto qualcosa
        if "commento_ai" not in st.session_state or st.session_state.commento_ai == "":
            nuovo_insulto_pos()
            
        st.write(f"🤖 {st.session_state.commento_ai}")
        
        if st.button("Conferma Città ➔"):
            st.session_state.dati['pos'] = st.session_state.input_citta
            # Reset del commento per lo step successivo così non rimane quello della posizione
            st.session_state.commento_ai = "" 
            avanti()

# --- STEP 2: METEO ---
elif st.session_state.step == 2:
    st.subheader("🕒 Il momento del disagio")
    
    # Funzione per cambiare l'insulto solo quando cambia il meteo
    def aggiorna_insulto_meteo():
        st.session_state.commento_ai = random.choice(insulti_meteo[st.session_state.sel_meteo])

    # Slider per l'orario (senza trigger per non incrociare i dati)
    st.select_slider(
        "Quando?", 
        options=["Mattina", "Pomeriggio", "Sera", "Notte"], 
        key="sel_orario"
    )
    
    # Selectbox con trigger chirurgico
    st.selectbox(
        "Meteo attuale", 
        ["Sole", "Pioggia", "Vento/Freddo"], 
        key="sel_meteo",
        on_change=aggiorna_insulto_meteo
    )
    
    # Inizializzazione: se entriamo nello step e non c'è un commento meteo, ne mettiamo uno
    if not any(insulto in st.session_state.commento_ai for lista in insulti_meteo.values() for insulto in lista):
        aggiorna_insulto_meteo()
    
    # Visualizzazione del commento (sempre aggiornato)
    st.write(f"🤖 {st.session_state.commento_ai}")
    
    st.divider()
    
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("⬅ Indietro"):
            indietro()

    with col_nav2:
        if st.button("Vediamo il resto ➔"):
            # Salvataggio dati e pulizia commento per lo step successivo
            st.session_state.dati['orario'] = st.session_state.sel_orario
            st.session_state.dati['meteo'] = st.session_state.sel_meteo
            st.session_state.commento_ai = "" # Reset per non portarsi dietro il meteo nel budget
            avanti()
# --- STEP 3: BUDGET ---
elif st.session_state.step == 3:
    st.subheader("💰 Quanti soldi volete sprecare?")
    
    # Funzione per cambiare l'insulto solo quando muovi lo slider del budget
    def aggiorna_insulto_budget():
        st.session_state.commento_ai = random.choice(insulti_budget[st.session_state.sel_budget])

    # Slider per il budget con trigger chirurgico
    st.select_slider(
        "Budget", 
        options=["€", "€€", "€€€"], 
        key="sel_budget",
        on_change=aggiorna_insulto_budget
    )
    
    # Inizializzazione: se entriamo e il commento è vuoto (o vecchio), ne mettiamo uno sul budget
    if st.session_state.commento_ai == "" or not any(insulto in st.session_state.commento_ai for lista in insulti_budget.values() for insulto in lista):
        aggiorna_insulto_budget()
    
    # Mostriamo l'insulto sui soldi
    st.write(f"🤖 {st.session_state.commento_ai}")
    
    st.divider()
    
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("⬅ Indietro"):
            indietro()

    with col_nav2:
        if st.button("Continua l'agonia ➔"):
            # Salviamo il valore definitivo
            st.session_state.dati['budget'] = st.session_state.sel_budget
            # Puliamo il commento per non portarlo nello step della stanchezza
            st.session_state.commento_ai = "" 
            avanti()
# --- STEP 4: STANCHEZZA ---
elif st.session_state.step == 4:
    st.subheader("😫 Livello di agonia")
    
    # Funzione per calcolare la categoria e aggiornare l'insulto
    def aggiorna_insulto_stanchezza():
        # Recuperiamo i valori direttamente dalle key
        l_val = st.session_state.sel_lui
        s_val = st.session_state.sel_lei
        media = (l_val + s_val) / 2
        
        if media <= 4:
            cat = "riposati"
        elif media <= 7:
            cat = "medi"
        else:
            cat = "distrutti"
        
        st.session_state.commento_ai = random.choice(insulti_stanchezza[cat])

    # Slider Lui
    st.slider("Stanchezza Lui", 1, 10, 5, key="sel_lui", on_change=aggiorna_insulto_stanchezza)
    
    # Slider Lei
    st.slider("Stanchezza Lei", 1, 10, 5, key="sel_lei", on_change=aggiorna_insulto_stanchezza)
    
    # Inizializzazione se il commento è vuoto o non pertinente
    if st.session_state.commento_ai == "" or not any(insulto in st.session_state.commento_ai for lista in insulti_stanchezza.values() for insulto in lista):
        aggiorna_insulto_stanchezza()
    
    # Mostriamo l'insulto sulla vostra pigrizia
    st.write(f"🤖 {st.session_state.commento_ai}")
    
    st.divider()
    
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("⬅ Indietro"):
            indietro()

    with col_nav2:
        if st.button("Quasi finito ➔"):
            # Salviamo i valori definitivi
            st.session_state.dati.update({
                'lui': st.session_state.sel_lui, 
                'lei': st.session_state.sel_lei
            })
            # Puliamo per il prossimo step
            st.session_state.commento_ai = "" 
            avanti()
# --- STEP 5: MEZZI ---
elif st.session_state.step == 5:
    st.subheader("🚗 Come volete trascinarvi?")
    
    # Funzione per aggiornare l'insulto solo quando cambia il mezzo
    def aggiorna_insulto_mezzi():
        scelta = st.session_state.sel_mezzo
        st.session_state.commento_ai = random.choice(insulti_mezzi[scelta])

    # Selectbox con trigger on_change
    st.selectbox(
        "Spostamento", 
        ["A piedi", "Mezzi pubblici", "Auto"], 
        key="sel_mezzo",
        on_change=aggiorna_insulto_mezzi
    )
    
    # Inizializzazione: se entriamo e il commento è vuoto o vecchio, ne generiamo uno
    if st.session_state.commento_ai == "" or not any(insulto in st.session_state.commento_ai for lista in insulti_mezzi.values() for insulto in lista):
        aggiorna_insulto_mezzi()
        
    # Visualizziamo l'insulto specifico per il mezzo
    st.write(f"🤖 {st.session_state.commento_ai}")
    
    st.divider()
    
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("⬅ Indietro"):
            indietro()

    with col_nav2:
        if st.button("Ultima scelta ➔"):
            # Salviamo il mezzo definitivo
            st.session_state.dati['mezzo'] = st.session_state.sel_mezzo
            # Pulizia per le categorie finali
            st.session_state.commento_ai = "" 
            avanti()

# --- STEP 6: CATEGORIE E GENERAZIONE ---
elif st.session_state.step == 6:
    st.subheader("🎯 Cosa cercate?")
    
    # Multiselect per le categorie
    st.multiselect(
        "Seleziona una o più opzioni:", 
        ["Cibo", "Bere", "Cultura", "Relax"], 
        default=["Cibo"], 
        key="sel_categorie"
    )
    
    # Visualizziamo un piccolo incoraggiamento acido se non c'è già un commento
    if st.session_state.commento_ai == "":
        st.session_state.commento_ai = "Scegliete in fretta, la mia pazienza ha un limite."
    
    st.write(f"🤖 {st.session_state.commento_ai}")
    
    st.divider()
    
    # Navigazione
    col_back, col_space = st.columns([1, 3])
    with col_back:
        if st.button("⬅ Indietro"):
            indietro()
    
    st.write(" ") # Spazio estetico
    
    # Bottoni di azione finale
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎰 STUPISCIMI!", use_container_width=True):
            st.session_state.dati['stupiscimi'] = True
            st.session_state.dati['cat'] = "Qualcosa di bizzarro e inaspettato"
            # Questo commento serve da trigger per lo Step 7
            st.session_state.commento_ai = "Oh, cercate l'effetto wow? Preparatevi a rimanere delusi."
            st.session_state.step = 7
            st.rerun()
            
    with col2:
        if st.button("GENERA OPZIONI", type="primary", use_container_width=True):
            if not st.session_state.sel_categorie:
                st.error("Seleziona almeno una categoria, non fatemi perdere tempo!")
            else:
                st.session_state.dati['stupiscimi'] = False
                st.session_state.dati['cat'] = st.session_state.sel_categorie
                # Questo commento serve da trigger per lo Step 7
                st.session_state.commento_ai = "Analizzo le vostre mediocri opzioni... un momento."
                st.session_state.step = 7
                st.rerun()
# --- STEP 7: IL VERDETTO (Gemini entra in azione) ---
elif st.session_state.step == 7:
    st.subheader("🔮 Il Verdetto del Bot")
    
    d = st.session_state.dati
    
    # Verifichiamo se abbiamo un trigger per generare la risposta
    # (Ovvero: il commento attuale è quello temporaneo impostato nello Step 6)
    trigger_generazione = any(frase in st.session_state.commento_ai for frase in ["Analizzo", "Oh, cercate"])
    
    if trigger_generazione:
        try:
            genai.configure(api_key=api_key) 
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Calcolo raggio dinamico
            stanchezza_max = max(d.get('lui', 5), d.get('lei', 5))
            raggio_base = 500 if stanchezza_max > 7 else 800

            prompt = f"""
            Agisci come il 'Decision Bot Cinico'. Sei sarcastico, arrogante e spietato.
            Il tuo compito è distruggere le speranze della coppia fornendo però opzioni reali.
            
            DATI CONTESTUALI:
            - POSIZIONE: {d.get('pos')}
            - STANCHEZZA: Lui {d.get('lui')}/10, Lei {d.get('lei')}/10. 
            - BUDGET: {d.get('budget')}
            - METEO: {d.get('meteo')}
            - MEZZO: {d.get('mezzo')}
            - COSA VOGLIONO: {d.get('cat')}
            
            LOGICA:
            1. Suggerisci 3 posti REALI che si trovano vicino a {d.get('pos')}.
            2. Usa un raggio di circa {raggio_base} metri.
            3. Se la zona è collinare o difficile, rinfaccia loro quanto sono pigri.
            
            FORMATO RICHIESTO:
            - Un insulto iniziale epico basato sulla loro combinazione di stanchezza e budget.
            - 3 Opzioni: **[Nome Posto]** - [Distanza]. Un commento acido sul perché dovrebbero andarci (o perché non li vorranno).
            - Link Google Maps per ogni posto (formato: https://www.google.com/maps/search/?api=1&query=NOME+POSTO+CITTA).
            """

            with st.spinner("Sto consultando gli astri (e le recensioni negative)..."):
                response = model.generate_content(prompt)
                # Sostituiamo il trigger con il testo finale per bloccare il loop
                st.session_state.commento_ai = response.text
                st.rerun()
                
        except Exception as e:
            st.error(f"Il sistema è collassato sotto il peso della vostra indecisione: {e}")
            if st.button("Riprova a pregare il bot"):
                st.rerun()

    # Visualizzazione finale del verdetto
    st.markdown(st.session_state.commento_ai)

    st.divider()
    
    # Bottone di reset totale
    if st.button("Ricomincia il calvario", type="secondary"):
        # Reset di tutte le variabili di stato
        st.session_state.step = 1
        st.session_state.dati = {}
        st.session_state.commento_ai = "Bentornati. Pronti per un altro giro di umiliazioni?"
        # Pulizia delle key dei widget
        for key in list(st.session_state.keys()):
            if key.startswith("sel_") or key.startswith("modo_"):
                del st.session_state[key]
        st.rerun()
    


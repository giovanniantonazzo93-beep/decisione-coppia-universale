Capisco perfettamente, resettiamo tutto e facciamo pulizia. Il problema del 404 con la nuova libreria google-genai su Streamlit spesso dipende da come il client comunica con l'endpoint.

Ecco la versione definitiva e completa di app.py. Ho ripristinato tutta la logica "Lui & Lei", ho pulito l'interfaccia e ho usato una configurazione del client che forza l'uso del modello corretto.

1. Assicurati che requirements.txt sia così:
Plaintext
streamlit
google-genai
2. Copia questo in app.py (Sovrascrivi tutto):
Python
import streamlit as st
from google import genai
import sys

# Configurazione iniziale della pagina
st.set_page_config(page_title="Decision Bot Universale", layout="wide")

# --- STILE E TITOLO ---
st.title("🤖 Decision Bot Universale per Coppie")
st.markdown(f"*Ambiente: Python {sys.version.split()[0]}*")

# --- SIDEBAR: CONFIGURAZIONE E DATI GENERALI ---
with st.sidebar:
    st.header("1. Configurazione")
    api_key = st.text_input("Inserisci Google API Key", type="password")
    
    st.divider()
    
    st.header("2. Dettagli Uscita")
    citta = st.text_input("Città", value="Pesaro")
    meteo = st.selectbox("Meteo", ["Sole", "Pioggia", "Freddo", "Nuvole"])
    orario = st.time_input("Orario previsto")
    budget = st.select_slider("Budget di coppia", options=["€", "€€", "€€€"])

# Controllo API Key
if not api_key:
    st.warning("⚠️ Inserisci l'API Key nella barra laterale per attivare il Bot.")
    st.stop()

# Inizializzazione Client Google GenAI
client = genai.Client(api_key=api_key)

# --- CORPO CENTRALE: DATI LUI & LEI ---
st.subheader("Profilo della Coppia")
col_lui, col_lei = st.columns(2)

with col_lui:
    st.markdown("### Lui 👤")
    stanchezza_lui = st.slider("Livello Stanchezza (Lui)", 1, 10, 5, key="s_lui")
    mezzo_lui = st.selectbox("Mezzo preferito (Lui)", ["Piedi", "Mezzi", "Auto"], key="m_lui")

with col_lei:
    st.markdown("### Lei 👤")
    stanchezza_lei = st.slider("Livello Stanchezza (Lei)", 1, 10, 5, key="s_lei")
    mezzo_lei = st.selectbox("Mezzo preferito (Lei)", ["Piedi", "Mezzi", "Auto"], key="m_lei")

st.divider()

# --- LOGICA DI GENERAZIONE ---
if st.button("Genera Proposte ✨", use_container_width=True):
    # Costruzione del prompt con le variabili attive
    prompt = f"""
    Agisci come un esperto local concierge a {citta}. 
    Pianifica 3 attività reali per una coppia considerando questi dati:
    - Meteo: {meteo}
    - Orario: {orario}
    - Budget: {budget}
    
    Profilo Lui: Stanchezza {stanchezza_lui}/10, preferisce spostarsi con {mezzo_lui}.
    Profilo Lei: Stanchezza {stanchezza_lei}/10, preferisce spostarsi con {mezzo_lei}.
    
    OUTPUT RICHIESTO (in Italiano):
    1. PROPOSTA LUI: Un'attività ideale per i suoi gusti e stanchezza.
    2. PROPOSTA LEI: Un'attività ideale per i suoi gusti e stanchezza.
    3. IL COMPROMESSO: L'attività perfetta che mette d'accordo entrambi.
    
    Per ogni proposta scrivi: Nome del posto reale a {citta}, motivo della scelta, orario e costo stimato.
    """
    
    try:
        with st.spinner('Lavoro per voi...'):
            # Chiamata al modello flash. 
            # Nota: Non usiamo prefissi 'models/' per evitare il 404 sulla nuova libreria.
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )
            
            if response.text:
                st.success("Ecco le vostre opzioni!")
                st.markdown(response.text)
            else:
                st.error("L'IA ha risposto ma il contenuto è vuoto. Riprova.")
                
    except Exception as e:
        st.error(f"Errore di sistema: {e}")
        st.info("Consiglio: Se l'errore è 404, prova a creare una NUOVA API Key su Google AI Stud

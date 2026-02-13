import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
import warnings

# --- Importation des dépendances ---
try:
    from google import genai
except ImportError:
    st.error("❌ **SDK non installé** : exécutez `pip install google-genai` puis redémarrez l'application.")
    st.stop()

# Ignorer les avertissements
warnings.simplefilter(action='ignore', category=FutureWarning)

# --- 1. CONFIGURATION ---
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("🔑 **Erreur** : la clé `GEMINI_API_KEY` est introuvable dans le fichier .env.")
    st.stop()

# Initialiser le client
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"❌ **Échec de l'initialisation de l'API** : {e}")
    st.stop()

st.set_page_config(page_title="Assistant Co-operators", layout="wide")

# --- 2. INTERFACE ---
st.title("🛡️ Plateforme IA Co-operators")

with st.sidebar:
    st.header("Données")
    uploaded_file = st.file_uploader("Charger CSV", type=['csv'])

# Initialiser l'historique des messages
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Bonjour ! Je suis votre assistant. Comment puis-je vous aider ?"}]

# Afficher l'historique du chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 3. LOGIQUE CHAT (gestion des erreurs) ---
if prompt := st.chat_input("Votre message..."):
    # Afficher le message de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Utiliser `gemini-flash-latest` pour un quota plus élevé
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )
        
        if response.text:
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        # Vérifier si le quota est épuisé (Erreur 429)
        if "429" in str(e):
            st.error("⚠️ **Quota épuisé (429)** : Limite de requêtes atteinte.")
            st.info("⏱️ L'API est en pause. Veuillez patienter environ 60 secondes avant de poser votre prochaine question.")
        else:
            st.error(f"⚠️ **Service indisponible** : {e}")
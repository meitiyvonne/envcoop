import streamlit as st
import pandas as pd
import numpy as np
import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- CONFIGURATION INITIALE ---
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="IA Co-operators", layout="wide")

# --- FONCTIONS DE BACK-END (LOGIQUE) ---

def diagnostiquer_donnees(df):
    """Analyse la qualité et la confidentialité des données."""
    rapport = []
    # Vérification PII (Confidentialité)
    mots_cles_pii = ['nom', 'prenom', 'telephone', 'email', 'adresse', 'nas', 'identite']
    colonnes_pii = [col for col in df.columns if any(k in col.lower() for k in mots_cles_pii)]
    
    if colonnes_pii:
        rapport.append(f"❌ **Alerte Confidentialité** : Colonnes sensibles détectées ({', '.join(colonnes_pii)}).")
    
    # Valeurs manquantes
    manquants = df.isnull().sum().sum()
    if manquants > 0:
        rapport.append(f"⚠️ **Alerte Qualité** : {manquants} valeurs manquantes détectées.")
    
    # Types de données
    colonnes_obj = df.select_dtypes(include=['object']).columns.tolist()
    if colonnes_obj:
        rapport.append(f"ℹ️ **Info Format** : Les colonnes {colonnes_obj} nécessitent un encodage (String).")
        
    return rapport, colonnes_pii

def nettoyer_donnees(df, colonnes_a_supprimer):
    """Exécute le nettoyage automatique."""
    # 1. Supprimer les PII
    df_propre = df.drop(columns=colonnes_a_supprimer)
    
    # 2. Remplir les valeurs manquantes
    for col in df_propre.columns:
        if df_propre[col].dtype in ['float64', 'int64']:
            df_propre[col] = df_propre[col].fillna(df_propre[col].mean())
        else:
            df_propre[col] = df_propre[col].fillna("Inconnu")
            
    return df_propre

# --- INTERFACE UTILISATEUR (STREAMLIT) ---

st.title("🛡️ Plateforme IA intelligente - Co-operators")

# Barre latérale
with st.sidebar:
    st.header("⚙️ Paramètres")
    fichier_charge = st.file_uploader("Charger des données (CSV, Excel)", type=['csv', 'xlsx'])
    if st.button("Déconnexion"):
        st.write("Déconnecté")

# Gestion de l'état de la session (Chat)
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Bonjour ! Je suis l'assistant IA de Co-operators. Veuillez charger un fichier pour commencer l'analyse."}]

# Affichage des messages du chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Logique principale après chargement
if fichier_charge:
    if 'df_original' not in st.session_state:
        st.session_state.df_original = pd.read_csv(fichier_charge)
    
    df = st.session_state.df_original
    
    # Diagnostic automatique
    rapport_erreurs, pii_trouves = diagnostiquer_donnees(df)
    
    with st.expander("🔍 Rapport de Diagnostic des Données", expanded=True):
        for msg in rapport_erreurs:
            st.write(msg)

    # Zone d'interaction Chat
    if prompt := st.chat_input("Ex: 'Nettoie les données' ou 'Analyse les risques'"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Logique de commande : NETTOYAGE
        if "nettoie" in prompt.lower() or "clean" in prompt.lower():
            df_nettoye = nettoyer_donnees(df, pii_trouves)
            st.session_state.df_original = df_nettoye # Mise à jour des données
            
            reponse_ia = "✅ **Nettoyage terminé !** J'ai supprimé les colonnes confidentielles et rempli les valeurs manquantes. Voici un aperçu :"
            with st.chat_message("assistant"):
                st.markdown(reponse_ia)
                st.dataframe(df_nettoye.head())
            st.session_state.messages.append({"role": "assistant", "content": reponse_ia})
        
        # Logique normale : IA Conversationnelle
        else:
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                instr_systeme = f"Tu es un expert en assurance chez Co-operators. Réponds professionnellement en français. Données actuelles : {df.columns.tolist()}"
                res = model.generate_content(f"{instr_systeme}\nUtilisateur: {prompt}")
                
                with st.chat_message("assistant"):
                    st.markdown(res.text)
                st.session_state.messages.append({"role": "assistant", "content": res.text})
            except Exception as e:
                st.error(f"Erreur : {e}")
else:
    st.info("💡 En attente du chargement d'un fichier CSV dans la barre latérale.")
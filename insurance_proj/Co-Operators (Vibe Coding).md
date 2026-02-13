Co-Operators (Vibe Coding)

**create folder**

(base)C:\Users\yvonne\envcoop

**create conda environment** (C:\Users\yvonne\envcoop)

(base)C:\Users\yvonne\envcoop > conda create -n envcoop python=3.10

**activate** 

C:\Users\yvonne\envcoop > conda activate envcoop

**envcoop path**

C:\Users\yvonne\anaconda3\envs\envcoop

(envcoop) PS C:\Users\yvonne\envcoop> python -V
Python 3.10.19

**install streamlit, pandas, google-generativeai, python-dotenv**

pip install streamlit streamlit-authenticator pandas google-generativeai python-dotenv

**chck pip list**

Package                      Version
---------------------------- -----------
altair                       6.0.0
annotated-types              0.7.0
attrs                        25.4.0
bcrypt                       5.0.0
blinker                      1.9.0
cachetools                   6.2.6
captcha                      0.7.1
certifi                      2026.1.4
cffi                         2.0.0
charset-normalizer           3.4.4
click                        8.3.1
colorama                     0.4.6
cryptography                 46.0.5
extra-streamlit-components   0.1.81
gitdb                        4.0.12
GitPython                    3.1.46
google-ai-generativelanguage 0.6.15
google-api-core              2.29.0
google-api-python-client     2.189.0
google-auth                  2.49.0.dev0
google-auth-httplib2         0.3.0
google-generativeai          0.8.6
googleapis-common-protos     1.72.0
grpcio                       1.78.0
grpcio-status                1.71.2
httplib2                     0.31.2
idna                         3.11
Jinja2                       3.1.6
jsonschema                   4.26.0
jsonschema-specifications    2025.9.1
MarkupSafe                   3.0.3
narwhals                     2.16.0
numpy                        2.2.6
packaging                    25.0
pandas                       2.3.3
pillow                       12.1.1
pip                          26.0.1
proto-plus                   1.27.1
protobuf                     5.29.6
pyarrow                      23.0.0
pyasn1                       0.6.2
pyasn1_modules               0.4.2
pycparser                    3.0
pydantic                     2.12.5
pydantic_core                2.41.5
pydeck                       0.9.1
PyJWT                        2.11.0
pyparsing                    3.3.2
python-dateutil              2.9.0.post0
python-dotenv                1.2.1
pytz                         2025.2
PyYAML                       6.0.3
referencing                  0.37.0
requests                     2.32.5
rpds-py                      0.30.0
setuptools                   80.10.2
six                          1.17.0
smmap                        5.0.2
streamlit                    1.54.0
streamlit-authenticator      0.4.2
tenacity                     9.1.4
toml                         0.10.2
tornado                      6.5.4
tqdm                         4.67.3
typing_extensions            4.15.0
typing-inspection            0.4.2
tzdata                       2025.3
uritemplate                  4.2.0
urllib3                      2.6.3
watchdog                     6.0.0
wheel                        0.46.3

**create requirements.txt**

(envcoop) PS C:\Users\yvonne\envcoop> pip freeze > requirements.txt

**copy & create requirements.txt**

(envcoop) PS C:\Users\yvonne\envcoop> pip install -r requirements.txt

**VS Code or Antigravity “Select Interpreter”**

Ctrl + Shift + P > Python: Select Interpreter : python 3.10.19

**create folder insurance_app**

(envcoop) PS C:\Users\yvonne\envcoop> mkdir insurance_app

(envcoop) PS C:\Users\yvonne\envcoop> cd insurance_app

**create app.py**

way-1:

(envcoop) PS C:\Users\yvonne\envcoop\insurance_app> python app.py

way-2

(envcoop) PS C:\Users\yvonne\envcoop\insurance_app>New-Item app.py

```python
import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. Configuration de sécurité
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="Assistant IA Co-operators", layout="wide")

# 2. Logique de diagnostic des données (Back-end)
def diagnose_data(df):
    report = []
    # Vérification de la confidentialité (PII)
    pii_keywords = ['nom', 'prenom', 'telephone', 'email', 'adresse', 'nas', 'identite']
    found_pii = [col for col in df.columns if any(k in col.lower() for k in pii_keywords)]
    if found_pii:
        report.append(f"❌ **Alerte Confidentialité**: Détection de données personnelles ({', '.join(found_pii)}). Cela peut enfreindre les politiques de protection de la vie privée.")
    
    # Vérification des valeurs manquantes
    null_counts = df.isnull().sum().sum()
    if null_counts > 0:
        report.append(f"⚠️ **Alerte Qualité**: Il y a {null_counts} valeurs manquantes, ce qui peut fausser les analyses.")
    
    # Vérification des formats de données
    str_cols = df.select_dtypes(include=['object']).columns.tolist()
    if str_cols:
        report.append(f"ℹ️ **Info Format**: Les colonnes {str_cols} sont au format texte et nécessiteront un encodage avant l'entraînement.")
        
    return report

# --- Interface Utilisateur (Front-end) ---
st.title("🛡️ Plateforme Collaborative IA Co-operators")

# Barre latérale : Centre de données
with st.sidebar:
    st.header("Centre de Données")
    uploaded_file = st.file_uploader("Charger un jeu de données (CSV, Excel, JSON)", type=['csv', 'xlsx', 'json'])
    
    if st.button("Se déconnecter"):
        st.info("Déconnexion réussie.")

# Initialisation de l'historique du chat
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Bonjour ! Je suis votre assistant IA Co-operators. Comment puis-je vous aider aujourd'hui ? Vous pouvez charger des données ou me poser des questions sur les risques d'assurance."}]

# Affichage des messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Traitement après chargement du fichier
if uploaded_file:
    try:
        # Lecture des données
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.info(f"Fichier '{uploaded_file.name}' chargé avec succès !")
        
        # Exécution du diagnostic
        issues = diagnose_data(df)
        
        if issues:
            with st.expander("🔍 Rapport de Diagnostic Automatique", expanded=True):
                for issue in issues:
                    st.write(issue)
                st.error("Note : La précision du modèle et la sécurité des données seront affectées tant que ces problèmes ne sont pas résolus.")
            
            # L'IA prend l'initiative
            if "diag_announced" not in st.session_state:
                diag_msg = "J'ai terminé le diagnostic initial. J'ai détecté des problèmes de confidentialité ou de qualité. Souhaitez-vous que je procède à un nettoyage automatique ? Ou avez-vous d'autres questions ?"
                st.session_state.messages.append({"role": "assistant", "content": diag_msg})
                st.session_state.diag_announced = True
                st.rerun()
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier : {e}")

# Zone de saisie du chat
if prompt := st.chat_input("Tapez votre commande ici..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Appel à Gemini avec un contexte d'expert en assurance
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Instruction système intégrée pour définir le rôle de l'IA
        context_prompt = f"Tu es un expert en science des données pour Co-operators Assurance. Réponds en français de manière professionnelle. Question : {prompt}"
        response = model.generate_content(context_prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Erreur d'appel IA : {e}")
```



**execute streamlit**

```python
streamlit run app.py	

#
 Welcome to Streamlit!

      If you'd like to receive helpful onboarding emails, news, offers, promotions,
      and the occasional swag, please enter your email address below. Otherwise,
      leave this field blank.

      Email: (enter)
```



![image-20260211200007156](C:\Users\yvonne\AppData\Roaming\Typora\typora-user-images\image-20260211200007156.png)

```tex
You can find our privacy policy at https://streamlit.io/privacy-policy

  Summary:
  - This open source library collects usage statistics.
  - We cannot see and do not store information contained inside Streamlit apps,
    such as text, charts, images, etc.
  - Telemetry data is stored in servers in the United States.
  - If you'd like to opt out, add the following to %userprofile%/.streamlit/config.toml,
    creating that file if necessary:

    [browser]
    gatherUsageStats = false


  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.2.25:8501

C:\Users\yvonne\anaconda3\envs\envcoop\lib\site-packages\google\api_core\_python_version_support.py:275: FutureWarning: You are using a Python version (3.10.19) which Google will stop supporting in new releases of google.api_core once it reaches its end of life (2026-10-04). Please upgrade to the latest Python version, or at least Python 3.11, to continue receiving updates for google.api_core past that date.
  warnings.warn(message, FutureWarning)
C:\Users\yvonne\envcoop\insurance_proj\insurance_app\app.py:3: FutureWarning:

All support for the `google.generativeai` package has ended. It will no longer be receiving
updates or bug fixes. Please switch to the `google.genai` package as soon as possible.
See README for more details:

https://github.com/google-gemini/deprecated-generative-ai-python/blob/main/README.md

  import google.generativeai as genai
```

![image-20260211200421859](C:\Users\yvonne\AppData\Roaming\Typora\typora-user-images\image-20260211200421859.png)



create a folder data & a file create_test_data.py for testing prompt

```python
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
```



**prompt > “Nettoie les données s'il vous plaît”**

![image-20260211201209906](C:\Users\yvonne\AppData\Roaming\Typora\typora-user-images\image-20260211201209906.png)

![image-20260211201508195](C:\Users\yvonne\AppData\Roaming\Typora\typora-user-images\image-20260211201508195.png)

![image-20260211201618796](C:\Users\yvonne\AppData\Roaming\Typora\typora-user-images\image-20260211201618796.png)

![image-20260211203140263](C:\Users\yvonne\AppData\Roaming\Typora\typora-user-images\image-20260211203140263.png)

```tex
AIzaSyAvLp9eMnvF8qFYWLoaprhI0KDmbCQOpg4
```



create a file “.env” 

```tex
GEMINI_API_KEY=AIzaSyAvLp9eMnvF8qFYWLoaprhI0KDmbCQOpg4
```


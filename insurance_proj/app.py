import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
import warnings

# --- 處理套件導入 ---
try:
    from google import genai
except ImportError:
    st.error("❌ **SDK 未安裝成功**：請在終端機執行 `pip install google-genai` 後重啟程式。")
    st.stop()

# 屏蔽警告
warnings.simplefilter(action='ignore', category=FutureWarning)

# --- 1. CONFIGURATION ---
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("🔑 **錯誤**：`.env` 檔案中找不到 `GEMINI_API_KEY`。")
    st.stop()

# 初始化客戶端
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"❌ **API 初始化失敗**：{e}")
    st.stop()

st.set_page_config(page_title="Assistant Co-operators", layout="wide")

# --- 2. INTERFACE ---
st.title("🛡️ Plateforme IA Co-operators")

with st.sidebar:
    st.header("Données")
    uploaded_file = st.file_uploader("Charger CSV", type=['csv'])

# 初始化對話紀錄
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Bonjour ! Je suis votre assistant. Comment puis-je vous aider ?"}]

# 顯示聊天歷史
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 3. LOGIQUE CHAT (整合錯誤處理) ---
if prompt := st.chat_input("Votre message..."):
    # 顯示使用者訊息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # 使用 gemini-1.5-flash，免費層級額度較高
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )
        
        if response.text:
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        # 判斷是否為額度耗盡 (Error 429)
        if "429" in str(e):
            st.error("⚠️ **Quota épuisé (429)** : Limite de requêtes atteinte.")
            st.info("⏱️ L'API est en pause. Veuillez patienter environ 60 secondes avant de poser votre prochaine question.")
        else:
            st.error(f"⚠️ **Service indisponible** : {e}")
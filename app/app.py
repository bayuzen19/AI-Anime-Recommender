import streamlit as st
import requests
from dotenv import load_dotenv

import os

FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")

st.set_page_config(
    page_title="🎌 Anime Recommendation",
    page_icon="🎌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF6B9D;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .sub-header {
        font-size: 1.2rem;
        color: #888;
        text-align: center;
        margin-bottom: 2rem;
    }
    .recommendation-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    .stButton>button {
        background: linear-gradient(90deg, #FF6B9D 0%, #FF8E53 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        border-radius: 25px;
        cursor: pointer;
        transition: transform 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        transform: scale(1.05);
    }
    .status-badge {
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
    }
    .status-online {
        background-color: #28a745;
        color: white;
    }
    .status-offline {
        background-color: #dc3545;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

def check_api():
    try:
        response = requests.get(f"{FASTAPI_URL}/health",timeout=15)
        if response.status_code ==200:
            return response.json()
        return None
    except requests.exceptions.RequestException:
        return None

def get_recommendation(query:str):
    try:
        response = requests.post(
            f"{FASTAPI_URL}/recommend",
            json={"query":query},
            timeout=120
        )

        if response.status_code == 200:
            return response.json()
        else:
            return {"error":response.json().get("detail","unknown error")}
    except requests.exceptions.RequestException as e:
        return {"error":str(e)}
    
with st.sidebar:
    st.image("https://i.imgur.com/6wj0hh6.jpeg",width=200)
    st.markdown("---")

    st.markdown("### 🕸️ Status API")
    health = check_api()

    if health and health.get("status")== "healthy":
        st.success("✅ API Online")

        if health.get("pipeline_loaded"):
            st.info("🧠 Pipeline Ready")
        else:
            st.warning("⚠️ Pipeline Loading")
    else:
        st.error("💀 API Offline")
    

    st.markdown("---")
    st.markdown("### 📚 About")
    st.markdown("""
    **Anime Recommnder** adalah aplikasi berbasis AI yang memberikan rekomendasi Anime berdasarkan Prefrences User.
    Powered by:
    - 🚀 FastAPI
    - 🎈 Streamlit
    - 🔗 LangChain
    - 🤖 Azure OpenAI
    """)

#--main content---
st.markdown('<h1 class="main-header">🎌 Anime Recommender</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Temukan anime baru berdasarkan preferensi Anda dengan bantuan AI!</p>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📱 Rekomendasi","📖 Panduan"])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 💬 Ceritakan Preferensi Anda")

        example = [
            "Saya ingin anime mirip seperti Bleach",
            "Anime yang seperti Naruto",
            "Rekomendasi Anime Sports"
        ]

        selected_box  = st.selectbox("Contoh Pilihan",
                                     ["-- Pilih Contoh --"]+example,
                                     label_visibility="collapsed")

        if selected_box != "-- Pilih Contoh --":
            default_query = selected_box
        else:
            default_query=""
        
        query = st.text_area(
            "Masukkan Preferences atau deskripsi anime yang sedang anda cari: ",
            value=default_query,
            height=150,
            placeholder="Contoh: berikan saya rekomendasi anime seperti onepiece"
        )

        submit_btn = st.button("🔍 Dapatkan Rekomendasi", use_container_width=True)

    with col2:
        st.markdown("### Daftar References")
        genres=["Action", "Romance", "Comedy", "Drama", "Fantasy", "Sci-Fi", "Horror", "Sports"]

        for i in range(0, len(genres),2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                if i+j < len(genres):
                    if col.button(genres[i+j], key=f"genre_{i+j}"):
                        st.session_state["selected_genre"] = genres[i+j]
    
    if submit_btn and query:
        health =check_api()

        if not health or health.get("status") != "healthy":
            st.error("❌ API tidak tersedia. Pastikan FastAPI backend sudah berjalan!")
        
        else:
           with st.spinner("🔮 Menganalisis preferensi Anda..."):
                result = get_recommendation(query)

                if "error" in result:
                    st.error(f"❌ Error: {result['error']}")
                else:
                    st.markdown(f"""
                        <div class="recommendation-box">
                            <h4>📝 Query Anda:</h4>
                            <p><em>{result.get('query', query)}</em></p>
                            <hr style="border-color: rgba(255,255,255,0.3);">
                            <h4>🎯 Rekomendasi:</h4>
                            <p>{result.get('recommendation', 'Tidak ada rekomendasi')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.success("✨ Rekomendasi berhasil dibuat!")

                    col1, col2 = st.columns(2)

                    with col1:
                        if st.button("🔄 Minta Rekomendasi Baru"):
                            st.rerun()
                    with col2:
                        if st.button("📋 Salin Rekomendasi"):
                            st.write("Rekomendasi telah disalin!")
    
    elif submit_btn and not query:
        st.warning('⚠️ Silakan masukkan deskripsi preferensi anime Anda!')


with tab2:
    st.markdown("""
    ## 📖 Cara Menggunakan
    
    ### 1. Pastikan API Berjalan
    Jalankan FastAPI backend terlebih dahulu:
    ```bash
    cd f:/programming/project/fastcampus/part_7
    uvicorn api.main:app --reload
    ```
    
    ### 2. Akses Streamlit
    Jalankan Streamlit app:
    ```bash
    streamlit run app/app.py
    ```
    
    ### 3. Masukkan Preferensi
    - Jelaskan jenis anime yang Anda sukai
    - Sebutkan anime favorit sebagai referensi
    - Deskripsikan elemen yang Anda cari (action, romance, dll)
    
    ### 4. Dapatkan Rekomendasi
    Klik tombol "Dapatkan Rekomendasi" dan tunggu AI menganalisis preferensi Anda!
    
    ---
    
    ## 🛠️ Arsitektur Sistem
    
    ```
    ┌──────────────┐     HTTP      ┌──────────────┐
    │   Streamlit  │ ◄──────────► │   FastAPI    │
    │   Frontend   │   Request    │   Backend    │
    └──────────────┘              └──────┬───────┘
                                         │
                                         ▼
                                ┌──────────────┐
                                │   LangChain  │
                                │   Pipeline   │
                                └──────┬───────┘
                                       │
                          ┌────────────┴────────────┐
                          ▼                         ▼
                   ┌─────────────┐          ┌─────────────┐
                   │  ChromaDB   │          │ Azure OpenAI│
                   │ Vector Store│          │     LLM     │
                   └─────────────┘          └─────────────┘
    ```
    
    ---
    
    ## 📡 API Endpoints
    
    | Method | Endpoint | Deskripsi |
    |--------|----------|-----------|
    | GET | `/` | Health check & welcome |
    | GET | `/health` | Status API & pipeline |
    | POST | `/recommend` | Dapatkan rekomendasi |
    
    ### Contoh Request
    ```json
    POST /recommend
    {
        "query": "Anime action dengan plot twist menarik"
    }
    ```
    
    ### Contoh Response
    ```json
    {
        "query": "Anime action dengan plot twist menarik",
        "recommendation": "Berdasarkan preferensi Anda...",
        "status": "success"
    }
    ```
    """)


# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 1rem;">
    <p>Made with ❤️ using Streamlit & FastAPI</p>
    <p>© 2024 Anime Recommender | Powered by AI</p>
</div>
""", unsafe_allow_html=True)

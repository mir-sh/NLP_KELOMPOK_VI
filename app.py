import streamlit as st
import joblib
import re

svm_model = joblib.load("svm_model.pkl")
tfidf = joblib.load("tfidf.pkl")

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

st.set_page_config(
    page_title="Deteksi Spam Komentar Youtube",
    page_icon="🛡️",
    layout="centered"
)

st.markdown("""
<style>
    .stButton>button {
        background-color: #1b5e20;
        color: white;
        border-radius: 8px;
        height: 45px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #2e7d32;
        color: white;
    }
    textarea {
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)
col1, col2 = st.columns([1,4])

with col1:
    st.image("youtube.png", width=90)

with col2:
    st.markdown(
        "<h2 style='color:#1b5e20; margin-bottom:0;'>Deteksi Spam Komentar YouTube</h2>"
        "<p style='margin-top:0;'>TF-IDF + SVM</p>",
        unsafe_allow_html=True
    )

st.markdown("---")

user_input = st.text_area(
    "✍️ Masukkan komentar:",
    height=150,
    placeholder="Contoh: Tolong subscribe channel saya..."
)

if st.button("🔍 Deteksi Komentar"):
    if user_input.strip() == "":
        st.warning("⚠️ Komentar tidak boleh kosong")
    else:
        cleaned = clean_text(user_input)
        vector = tfidf.transform([cleaned])
        prediction = svm_model.predict(vector)[0]

        st.markdown("---")

        if prediction == 1:
            st.error("🚨 **SPAM TERDETEKSI**\n\nHindari komentar yang mengandung penipuan atau promosi berlebihan.")
        else:
            st.success("✅ **KOMENTAR AMAN (HAM)**\n\nKomentar tidak mengandung unsur spam.")

st.markdown("---")
st.markdown(
    "<p style='text-align:center; font-size:12px;'>"
    "Dibuat sebagai UAS NLP | © KEL6 2026<br>"
    "</p>",
    unsafe_allow_html=True
)

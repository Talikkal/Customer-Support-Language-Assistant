import pickle
import streamlit as st
import numpy as np
from googletrans import Translator
import fitz  # PyMuPDF

# Load model
with open("model.pckl", "rb") as f:
    Lrdetect_Model = pickle.load(f)

translator = Translator()
st.set_page_config(page_title="Customer Support Tool", layout="centered")
st.title("Customer Support Language Assistant")

# Language code map
supported_languages = {
    "English": "en",
    "Hindi": "hi",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Bengali": "bn",
    "Marathi": "mr",
    "Urdu": "ur",
    "Odia": "or",
    "Assamese": "as",
    "Maithili": "mai",
    "Santali": "sat",
    "French": "fr",
    "Spanish": "es",
    "Portuguese": "pt",
    "Italian": "it",
    "Russian": "ru",
    "Swedish": "sv",
    "Dutch": "nl",
    "Arabic": "ar",
    "Turkish": "tr",
    "German": "de",
    "Danish": "da",
    "Greek": "el",
}

# Initialize session state
for key in [
    "detected_text",
    "detected_pdf",
    "lang_text",
    "lang_pdf",
    "translated_msg",
    "translated_reply",
]:
    if key not in st.session_state:
        st.session_state[key] = ""

# =========================
# TEXT BASED DETECTION
# =========================
st.header("Detect Language")
text_input = st.text_area("Enter received message:")
if st.button("🔍 Detect Language "):
    if text_input.strip():
        st.session_state.detected_text = text_input
        pred = Lrdetect_Model.predict([text_input])
        conf = np.max(Lrdetect_Model.predict_proba([text_input]))
        st.session_state.lang_text = pred[0]
        st.success(f"✅ Detected Language: **{pred[0]}** (Confidence: {conf*100:.2f}%)")
    else:
        st.warning("⚠️ Please enter a message.")

# =========================
# PDF BASED DETECTION
# =========================
st.header("📄 PDF-Based Language Detection")

pdf_file = st.file_uploader("Upload PDF file", type="pdf")

if st.button("📥 Extract & Detect Language"):
    if pdf_file:
        pdf = fitz.open(stream=pdf_file.read(), filetype="pdf")
        extracted = "".join([page.get_text() for page in pdf])
        st.session_state.detected_pdf = extracted
        pred = Lrdetect_Model.predict([extracted])
        conf = np.max(Lrdetect_Model.predict_proba([extracted]))
        st.session_state.lang_pdf = pred[0]
        st.success(f"✅ PDF Language: **{pred[0]}** (Confidence: {conf*100:.2f}%)")
        st.text_area("Extracted PDF Text:", value=extracted, height=150)
    else:
        st.warning("⚠️ Please upload a PDF file.")

# =========================
# TRANSLATION SECTION
# =========================
if st.session_state.lang_text or st.session_state.lang_pdf:
    st.markdown("---")
    st.header("🌍 Translate Detected Message")

    # Determine active source
    active_text = st.session_state.detected_text or st.session_state.detected_pdf
    detected_lang = st.session_state.lang_text or st.session_state.lang_pdf

    st.info(f"Detected Language: **{detected_lang}**")

    target_lang = st.selectbox(
        "Translate message to:", list(supported_languages.keys())
    )

    if st.button("🌐 Translated Message"):
        try:
            trans = translator.translate(
                active_text, dest=supported_languages[target_lang]
            )
            st.session_state.translated_msg = trans.text
            st.success(f"📝 Translated Message:\n\n{trans.text}")
        except Exception as e:
            st.error(f"❌ Translation error: {e}")

# =========================
# REPLY SECTION
# =========================
if st.session_state.translated_msg:
    st.markdown("---")
    st.header("✍️ Compose Reply in Your Language")

    reply_input = st.text_area("Enter your reply:")

    if st.button("🔁 Convert Reply to Customer Language"):
        try:
            customer_lang_code = translator.detect(active_text).lang
            reply_translated = translator.translate(
                reply_input, dest=customer_lang_code
            )
            st.session_state.translated_reply = reply_translated.text
            st.success(f"📬 Reply in Customer's Language:\n\n{reply_translated.text}")
        except Exception as e:
            st.error(f"❌ Conversion error: {e}")



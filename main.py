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

# Function: Tooltip with fallback to original word

def generate_hover_html_with_mapping_and_meaning(
    source_text, target_text, source_lang_code, target_lang_code
):
    source_words = source_text.split()
    target_words = target_text.split()
    html_parts = []

    min_len = min(len(source_words), len(target_words))

    for i in range(min_len):
        src_word = source_words[i]
        tgt_word = target_words[i]
        try:
            meaning = translator.translate(
                src_word, src=source_lang_code, dest=target_lang_code
            ).text
            if meaning.strip().lower() == src_word.strip().lower():
                meaning = "(same as original)"
        except:
            meaning = "(same as original)"

        tooltip = f"{src_word} → {meaning}"
        html_parts.append(
            f'<span style="padding:4px 6px;" title="{tooltip}">{tgt_word}</span>'
        )

    for word in target_words[min_len:]:
        html_parts.append(
            f'<span style="padding:4px 6px;" title="(no match)">{word}</span>'
        )

    return " ".join(html_parts)

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

# Text-Based Detection
st.header(" Language Detection")
text_input = st.text_area("Enter received message:")
if st.button("🔍 Detect Language"):
    if text_input.strip():
        st.session_state.detected_text = text_input
        pred = Lrdetect_Model.predict([text_input])
        conf = np.max(Lrdetect_Model.predict_proba([text_input]))
        st.session_state.lang_text = pred[0]
        st.success(f"✅ Detected Language: **{pred[0]}** (Confidence: {conf*100:.2f}%)")
    else:
        st.warning("⚠️ Please enter a message.")

# PDF-Based Detection
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

# Translation Section
if st.session_state.lang_text or st.session_state.lang_pdf:
    st.markdown("---")
    st.header("🌍 Translate Detected Message")

    active_text = st.session_state.detected_text or st.session_state.detected_pdf
    detected_lang = st.session_state.lang_text or st.session_state.lang_pdf

    st.info(f"Detected Language: **{detected_lang}**")

    target_lang = st.selectbox(
        "Translate message to:", list(supported_languages.keys())
    )

    if st.button("🌐 Translated Message"):
        try:
            target_code = supported_languages[target_lang]
            trans = translator.translate(active_text, dest=target_code)
            st.session_state.translated_msg = trans.text

            hover_html = generate_hover_html_with_mapping_and_meaning(
                source_text=active_text,
                target_text=trans.text,
                source_lang_code=detected_lang,
                target_lang_code=target_code,
            )
            st.markdown("📝Translated Message:", unsafe_allow_html=True)
            st.markdown(hover_html, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Translation error: {e}")

# Reply Section
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

            reply_hover = generate_hover_html_with_mapping_and_meaning(
                source_text=reply_input,
                target_text=reply_translated.text,
                source_lang_code=supported_languages[target_lang],
                target_lang_code=customer_lang_code,
            )

            st.markdown(
                "📬 Reply in Customer's Language:",
                unsafe_allow_html=True,
            )
            st.markdown(reply_hover, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Conversion error: {e}")




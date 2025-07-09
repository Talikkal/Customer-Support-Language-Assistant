# 🗣️ Customer Support Language Assistant

This is a Streamlit-based web application that detects the language of customer messages, translates them to a preferred language, and helps compose replies in the customer’s original language. It supports both direct text and PDF input, providing enhanced functionality for multilingual customer support.

---

## 🚀 Features

- 🔍 **Language Detection**
  - Detect language from plain text input
  - Detect language from uploaded PDF documents

- 🌐 **Message Translation**
  - Translate detected messages into selected target languages
  - Hover on translated text to view original word mapping and meaning

- ✍️ **Reply Assistant**
  - Compose a reply in your own language
  - Automatically converts the reply to the customer's original language
  - Hover-enabled explanation for word-by-word mapping

---

## 🛠️ Built With

- **Frontend**: Streamlit
- **Machine Learning**: scikit-learn model (`model.pckl`)
- **Translation**: googletrans API
- **PDF Extraction**: PyMuPDF (`fitz`)

---

## 📁 Project Structure

```
.
├── app.py / main.py           # Main application code
├── model.pckl                # Trained language detection model
├── Language Detection.csv    # Dataset used for training
├── .gitignore
├── README.md                 # Project documentation
```

---

 **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

 **Run the Streamlit app**
   ```bash
   streamlit run app.py
   ```


## 📦 Dependencies

You can use this `requirements.txt`:

```txt
streamlit
numpy
scikit-learn
googletrans==4.0.0-rc1
PyMuPDF
```

## 🧠 Model Details

- The application uses a pre-trained classification model (`model.pckl`) for language detection.
- It outputs the detected language with prediction confidence.

---

## 💡 Use Cases

- Multilingual customer support
- Automatic language detection from forms, tickets, and PDFs
- Reply assistance for support agents
- Educational translation tool

---

## ⚠️ Notes

- Translations are powered by `googletrans` (unofficial Google Translate API) and may occasionally experience rate limits or temporary issues.
- Word mapping with hover is approximate and may not be 100% accurate in all cases.

---

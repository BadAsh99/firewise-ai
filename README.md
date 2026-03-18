# 🔥 Firewise AI – Posture Validator

Firewise AI is a GenAI-powered security validation tool for Palo Alto Networks PAN-OS configurations. It allows users to upload XML/CSV configs, query posture validation with Gemini or GPT-4, and export the results.

## 🚀 Features

- ✅ Streamlit-based web UI
- ✅ Upload PAN-OS XML or CSV files
- ✅ Live Q&A with Gemini or GPT-4 (toggleable)
- ✅ Streaming responses for real-time feedback
- ✅ Downloadable CSV export of all Q&A

## 🛠️ Local Dev Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py

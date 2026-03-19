# Firewise AI

> GenAI-powered PAN-OS security posture validator

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.33-red?logo=streamlit)
![Gemini](https://img.shields.io/badge/Google-Gemini-blue?logo=google)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green?logo=openai)

---

## Overview

Firewise AI is a GenAI-powered security validation tool for **Palo Alto Networks PAN-OS configurations**. Upload an XML firewall config, ask natural language questions about your security posture, and get AI-generated analysis backed by real configuration context.

Built for network security engineers who need to rapidly audit PAN-OS deployments without manually parsing thousands of lines of XML.

---

## Architecture

```
Streamlit UI (app.py)
    │
    ├── XML Config Upload
    │       └── config_parser.py → extract_config_summary() → JSON context
    │
    ├── Model Selector
    │       └── Gemini  or  GPT-4
    │
    ├── Q&A Input
    │       └── full_prompt = config_context + user_question
    │
    └── ai_engines.py (get_ai_stream)
            ├── _stream_gemini()   →  google-generativeai
            └── _stream_gpt()      →  openai
            │
            ▼
        st.write_stream() → Live streaming response
            │
            ▼
        export_tracker.py → CSV session log
```

---

## Features

- **XML config upload** — parse and summarize PAN-OS firewall configurations automatically
- **Natural language Q&A** — ask posture questions in plain English, get context-aware answers
- **Dual AI engine** — toggle between Google Gemini and OpenAI GPT-4 mid-session
- **Streaming responses** — real-time answer generation via Streamlit's `write_stream()`
- **CSV export** — download the full Q&A session log for audit records or reporting
- **Session tracking** — all interactions logged with timestamps for traceability

---

## Example Questions

```
"Are any security zones missing egress rules?"
"Is the management interface exposed to untrusted zones?"
"Which policies allow any-to-any traffic?"
"Are there missing application-default service profiles?"
"Does this config comply with CIS PAN-OS Benchmark recommendations?"
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| UI | Streamlit 1.33 |
| AI | google-generativeai 0.7, OpenAI 1.35 |
| Config parsing | xmltodict 0.13 |
| Data | Pandas 2.2 |
| HTTP | httpx 0.27 (proxy-bypass for network flexibility) |
| Config | python-dotenv |

---

## Getting Started

```bash
git clone https://github.com/BadAsh99/firewise-ai.git
cd firewise-ai
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add API keys
streamlit run app.py
```

---

## Environment Variables

```env
GOOGLE_API_KEY=
OPENAI_API_KEY=
```

---

## Supported Config Formats

- PAN-OS XML configuration exports (full and partial)
- CSV-based policy exports

---

## Use Cases

- Pre-deployment security posture review
- Rapid audit of inherited or undocumented firewall configurations
- Compliance gap analysis against PAN-OS security best practices
- Security team onboarding — understand an unfamiliar firewall config fast

---

## Author

**Ash Clements** — Sr. Principal Security Consultant | Cloud & AI Security | Palo Alto Networks Specialist
[github.com/BadAsh99](https://github.com/BadAsh99)

import streamlit as st
import os
import json
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
from utils.parser import extract_summary
import google.generativeai as genai

# Load API keys from .env
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Initialize OpenAI client
openai_client = OpenAI(api_key=openai_api_key)

# Configure Gemini
genai.configure(api_key=gemini_api_key)
gemini_model = genai.GenerativeModel("gemini-1.5-pro")

# Streamlit UI
st.set_page_config(page_title="Firewise AI - PAN-OS Posture Validator")
st.title("🔥 Firewise AI – PAN-OS Posture Validator")
st.markdown("Upload your PAN-OS config `.xml` file to receive an AI-driven security posture assessment.")

# Upload UI
uploaded_file = st.file_uploader("📁 Upload PAN-OS config file", type=["xml"])
model_choice = st.radio("🧠 Choose LLM Engine", ["GPT-4.1 (OpenAI)", "Gemini Pro (Google)"])

if uploaded_file:
    file_contents = uploaded_file.read()
    st.success("✅ File uploaded successfully.")

    config_summary = extract_summary(file_contents)

    if st.button("🔍 Run Firewise Validation"):
        with st.spinner(f"Analyzing with {model_choice}..."):
            try:
                full_prompt = (
                    "You are a cybersecurity expert specializing in Palo Alto Networks PAN-OS firewall configurations.\n\n"
                    "Analyze the following PAN-OS configuration summary. Identify security misconfigurations or risks and return a list of findings in JSON format. "
                    "Each finding should include:\n"
                    "- finding: A short description of the issue\n"
                    "- risk_level: High, Medium, or Low\n"
                    "- recommendation: A best-practice fix or improvement\n\n"
                    "Only return a raw JSON array. Do not include any explanation or Markdown formatting."
                )

                if model_choice == "GPT-4.1 (OpenAI)":
                    response = openai_client.chat.completions.create(
                        model="gpt-4.1",
                        messages=[
                            {"role": "system", "content": full_prompt},
                            {"role": "user", "content": str(config_summary)}
                        ]
                    )
                    raw_json_text = response.choices[0].message.content.strip()

                else:  # Gemini Pro with Streaming
                    streamed_text = ""
                    for chunk in gemini_model.generate_content(
                        f"{full_prompt}\n\n{config_summary}",
                        stream=True
                    ):
                        if chunk.text:
                            streamed_text += chunk.text
                            st.markdown("```json\n" + streamed_text + "\n```")

                    raw_json_text = streamed_text.strip()

                # Parse and show
                parsed_json = json.loads(raw_json_text)
                df = pd.DataFrame(parsed_json)
                st.success("✅ JSON parsed successfully")
                st.dataframe(df)

                # Save outputs
                with open("output/firewise_report.json", "w") as jf:
                    json.dump(parsed_json, jf, indent=2)
                df.to_csv("output/firewise_report.csv", index=False)
                st.success("📄 Saved: JSON + CSV")

            except Exception as e:
                st.error(f"❌ LLM request failed: {e}")

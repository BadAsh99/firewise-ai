import streamlit as st
from dotenv import load_dotenv
import json

# ✅ Must be first Streamlit command
st.set_page_config(page_title="🔥 Firewise AI", layout="wide")

# ✅ Load environment variables
load_dotenv()

# ✅ Import supporting modules
from utils.parser import extract_config_summary
from config_parser import format_config_for_display
from ai_engines import get_ai_stream
from export_tracker import add_log_entry, get_export_dataframe

# 🔥 App title and description
st.title("🔥 Firewise AI – Posture Validator")
st.markdown("Upload a PAN-OS XML config file, choose your AI engine, and ask posture validation questions.")

# 📁 Upload config file
uploaded_file = st.file_uploader("📁 Upload Config File", type=["xml"])

if uploaded_file:
    file_bytes = uploaded_file.read()
    
    # Process the file for both display and AI analysis
    display_config = format_config_for_display(uploaded_file.name, file_bytes)
    config_summary_str = extract_config_summary(file_bytes)
    
    st.subheader("📄 Configuration Preview")
    st.code(display_config, language="xml")

    # 💬 User question
    st.subheader("💬 Ask a Question")
    question = st.text_input("e.g., Are any admin accounts missing password complexity?", key="user_question")

    # 🔄 Model selector
    model_choice = st.radio("Choose AI engine:", ("Gemini", "GPT-4"), horizontal=True)

    # 🧠 Run question
    if st.button("🧠 Get Answer"):
        if not question:
            st.warning("Please enter a question.")
        else:
            full_prompt = f"Here is the firewall configuration summary in JSON format:\n{config_summary_str}\n\nUser Question: {question}"
            
            st.subheader("🧠 AI Response")
            try:
                response_stream = get_ai_stream(model_choice, full_prompt)
                full_response = st.write_stream(response_stream)
                
                # ✅ Log the successful Q&A interaction
                add_log_entry(question, model_choice, full_response)

            except (ValueError, RuntimeError) as e:
                st.error(str(e))

# 📦 Export Session Log
st.subheader("📦 Export Session Log")
log_df = get_export_dataframe()

if not log_df.empty:
    st.dataframe(log_df)
    csv = log_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Log as CSV",
        data=csv,
        file_name="firewise_ai_log.csv",
        mime="text/csv",
    )
else:
    st.caption("Your Q&A log is empty.")
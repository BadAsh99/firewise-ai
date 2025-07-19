import argparse
import json
import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
from utils.parser import extract_summary
import google.generativeai as genai
import pandas as pd

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Initialize OpenAI
openai_client = OpenAI(api_key=openai_api_key)

# Initialize Gemini
genai.configure(api_key=gemini_api_key)
gemini_model = genai.GenerativeModel("gemini-1.5-pro")

# 🧠 Prompt used by both models
prompt = (
    "You are a cybersecurity expert specializing in Palo Alto Networks PAN-OS firewall configurations.\n\n"
    "Analyze the following PAN-OS configuration summary. Identify security misconfigurations or risks and return a list of findings in JSON format. "
    "Each finding should include:\n"
    "- finding: A short description of the issue\n"
    "- risk_level: High, Medium, or Low\n"
    "- recommendation: A best-practice fix or improvement\n\n"
    "Only return a raw JSON array. Do not include any explanation or Markdown formatting."
)

# 🧪 Run audit function
def run_audit(config_file_path, llm_choice):
    print(f"🔍 Parsing and analyzing: {config_file_path} using {llm_choice.upper()}")

    try:
        with open(config_file_path, "r") as f:
            raw_xml = f.read()
        summary = extract_summary(raw_xml)

        if llm_choice == "gemini":
            response = gemini_model.generate_content(f"{prompt}\n\n{summary}")
            raw_json = response.text.strip()
        else:
            response = openai_client.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": str(summary)}
                ]
            )
            raw_json = response.choices[0].message.content.strip()

        parsed = json.loads(raw_json)
        df = pd.DataFrame(parsed)

        os.makedirs("output", exist_ok=True)
        json_path = "output/firewise_report.json"
        csv_path = "output/firewise_report.csv"

        with open(json_path, "w") as jf:
            json.dump(parsed, jf, indent=2)
        df.to_csv(csv_path, index=False)

        print(f"✅ Audit completed: {csv_path}")
    except Exception as e:
        print(f"❌ Audit failed: {e}")
        sys.exit(1)

# 🧾 CLI Entry Point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Firewise AI - PAN-OS CLI Auditor")
    parser.add_argument("config_path", help="Path to the PAN-OS config XML file")
    parser.add_argument("--llm", choices=["gpt", "gemini"], default="gpt", help="LLM engine to use (gpt or gemini)")
    args = parser.parse_args()

    run_audit(args.config_path, args.llm)

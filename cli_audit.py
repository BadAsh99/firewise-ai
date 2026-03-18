import argparse
import json
import os
import sys
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
import google.generativeai as genai
from utils.parser import extract_config_summary

# A helper for logging to stderr
def log_stderr(message):
    print(message, file=sys.stderr)

# --- Configuration & Client Initialization ---
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")
PROMPT_PATH = "prompts/validator_prompt.txt" # Path to the external prompt

openai_client = OpenAI(api_key=openai_api_key)
genai.configure(api_key=gemini_api_key)
gemini_model = genai.GenerativeModel("gemini-1.5-pro-latest")

# --- Main Audit Function ---
def run_audit(config_file_path, llm_choice, output_path):
    log_stderr(f"🔍 Analyzing '{config_file_path}' using {llm_choice.upper()}...")

    try:
        # Load the external prompt file
        with open(PROMPT_PATH, "r") as f:
            json_prompt = f.read()

        with open(config_file_path, "r") as f:
            raw_config_str = f.read()
        
        summary_str = extract_config_summary(raw_config_str)
        
        if llm_choice == "gemini":
            response = gemini_model.generate_content(f"{json_prompt}\n\n{summary_str}")
            raw_json = response.text
        else: # Assumes 'gpt'
            response = openai_client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": json_prompt},
                    {"role": "user", "content": summary_str}
                ]
            )
            raw_json = response.choices[0].message.content

        # Clean the response to ensure it's valid JSON
        json_start = raw_json.find('[')
        json_end = raw_json.rfind(']') + 1
        cleaned_json = raw_json[json_start:json_end]
        
        parsed = json.loads(cleaned_json)
        df = pd.DataFrame(parsed)

        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        json_path = output_path + ".json"
        csv_path = output_path + ".csv"

        with open(json_path, "w") as jf:
            json.dump(parsed, jf, indent=2)
        df.to_csv(csv_path, index=False)

        log_stderr(f"\n✅ Audit complete. Reports saved to:")
        log_stderr(f"   - {json_path}")
        log_stderr(f"   - {csv_path}")

    except Exception as e:
        log_stderr(f"\n❌ Audit Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Firewise AI - PAN-OS CLI Auditor")
    parser.add_argument("config_path", help="Path to the PAN-OS config XML file.")
    parser.add_argument("--llm", choices=["gpt", "gemini"], default="gpt", help="LLM engine to use (default: gpt).")
    parser.add_argument("--output", default="output/firewise_report", help="Path and filename for the output report, without extension.")
    args = parser.parse_args()

    run_audit(args.config_path, args.llm, args.output)
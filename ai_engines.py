import os
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv
import httpx # ✅ Import the new library

# Load environment variables
load_dotenv()

# --- Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-pro-latest")
GPT_MODEL = os.getenv("GPT_MODEL", "gpt-4-turbo")

# --- AI System Prompt ---
SYSTEM_PROMPT = (
    "You are Firewise AI, a cybersecurity expert specializing in Palo Alto Networks PAN-OS firewall configurations. "
    "Analyze the provided configuration and answer the user's question with a focus on security posture, best practices, and potential risks. "
    "Provide clear, concise, and actionable advice."
)

# --- Gemini Initialization ---
try:
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel(GEMINI_MODEL)
    else:
        gemini_model = None
except Exception as e:
    print(f"[Gemini Init Error] {e}")
    gemini_model = None

# --- Internal Streaming Functions ---
def _stream_gpt(prompt: str):
    if not OPENAI_API_KEY:
        raise ValueError("[GPT Error] OPENAI_API_KEY is not set.")
    
    try:
        # ✅ Create a custom HTTP client that explicitly ignores system proxies
        http_client = httpx.Client(proxies={})

        # ✅ Pass the custom client to OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY, http_client=http_client)
        
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            stream=True
        )
        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    except Exception as e:
        raise RuntimeError(f"[GPT Error] {str(e)}")


def _stream_gemini(prompt: str):
    if not gemini_model:
        raise ValueError("[Gemini Error] GEMINI_API_KEY is missing or the model failed to initialize.")

    try:
        stream = gemini_model.generate_content(
            f"{SYSTEM_PROMPT}\n\nUser Prompt: {prompt}",
            stream=True
        )
        for chunk in stream:
            yield chunk.text
    except Exception as e:
        raise RuntimeError(f"[Gemini Error] {str(e)}")

# --- Public Factory Function ---
def get_ai_stream(model_choice: str, prompt: str):
    """
    Returns the appropriate AI model stream based on user choice.
    """
    if model_choice == "Gemini":
        return _stream_gemini(prompt)
    elif model_choice == "GPT-4":
        return _stream_gpt(prompt)
    else:
        raise ValueError(f"Unknown model choice: {model_choice}")
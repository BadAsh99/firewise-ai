import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

try:
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content("Say hello")
    print("✅ Gemini says:", response.text)
except Exception as e:
    print("❌ Gemini Error:", e)

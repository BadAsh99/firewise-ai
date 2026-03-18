import os
import google.generativeai as genai

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    def ask_gemini(prompt):
        return "[ERROR] GOOGLE_API_KEY is not set. Please configure it in Azure App Service."
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-pro")

    def ask_gemini(prompt):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"[Gemini Error] {str(e)}"

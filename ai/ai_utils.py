# ai/ai_utils.py
import google.generativeai as genai

genai.configure(api_key="AIzaSyCQwmLtnOvE5i8MjdAAd0lYl51sPEC082k")  # Replace with your Gemini API key

model = genai.GenerativeModel("gemini-2.0-flash")  # or "gemini-1.5-flash" if available

def get_explanation(query):
    try:
        response = model.generate_content(query)
        return response.text
    except Exception as e:
        return f"[Error] Gemini API failed: {str(e)}"

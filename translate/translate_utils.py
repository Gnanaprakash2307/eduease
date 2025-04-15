# translate/translate_utils.py
from deep_translator import GoogleTranslator

def translate_to_tamil(text):
    try:
        return GoogleTranslator(source='auto', target='ta').translate(text)
    except Exception as e:
        return f"[Translation Error] {str(e)}"

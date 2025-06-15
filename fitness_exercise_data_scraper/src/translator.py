from deep_translator import GoogleTranslator
from src.utils import logger

class Translator:
    """Handles text translation from English to Turkish."""
    
    def __init__(self, source="en", target="tr"):
        self.translator = GoogleTranslator(source=source, target=target)
    
    def translate(self, text):
        """Translates the given text."""
        if not text or not isinstance(text, str):
            logger.warning(f"Invalid text for translation: {text}")
            return ""
        try:
            translated = self.translator.translate(text)
            logger.debug(f"Text translated: {text} -> {translated}")
            return translated
        except Exception as e:
            logger.error(f"Error during translation: {e}")
            return text  # Return original text on error
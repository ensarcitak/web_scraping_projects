import re
import logging

def setup_logging():
    """Initializes logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("scraper.log"),
            logging.StreamHandler(),
        ],
    )
    return logging.getLogger(__name__)

logger = setup_logging()

def format_search_term(term):
    """Formats the Turkish search term for URL."""
    if not term or not isinstance(term, str):
        logger.warning(f"Invalid term: {term}")
        return None
    term = term.lower().strip()
    replacements = {
        "ç": "c", "ğ": "g", "ı": "i", "ö": "o", "ş": "s", "ü": "u",
        "Ç": "c", "Ğ": "g", "İ": "i", "Ö": "o", "Ş": "s", "Ü": "u"
    }
    for turkish_char, english_char in replacements.items():
        term = term.replace(turkish_char, english_char)
    term = re.sub(r'[^a-z0-9-]', '', term.replace(" ", "-"))
    return term if term else None

def load_search_terms(file_path):
    """Reads search terms from the txt file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            terms = file.read().strip().split(',')
        formatted_terms = [format_search_term(term) for term in set(terms) if term.strip()]
        logger.info(f"{len(formatted_terms)} arama terimi yüklendi.")
        return [term for term in formatted_terms if term]
    except FileNotFoundError:
        logger.error(f"File could not find: {file_path}")
        return []
    except Exception as e:
        logger.error(f"Error while reading the terms from the file: {e}")
        return []
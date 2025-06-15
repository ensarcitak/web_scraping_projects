import logging
import os

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

def ensure_directory(directory):
    """Ensures the directory exists, creates it if not."""
    try:
        os.makedirs(directory, exist_ok=True)
        logger.debug(f"Directory created or already exists: {directory}")
    except Exception as e:
        logger.error(f"Error creating directory: {e}")
        raise
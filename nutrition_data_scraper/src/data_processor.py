import pandas as pd
from src.config import CONFIG
from src.utils import logger

class DataProcessor:
    """Process scraped data and save it to an Excel file."""
    
    def __init__(self):
        self.config = CONFIG
        self.df = pd.DataFrame(columns=self.config["COLUMNS"])
    
    def process_data(self, product_data):
        """Adds scraped data to the DataFrame."""
        try:
            temp_df = pd.DataFrame(product_data)
            self.df = pd.concat([self.df, temp_df], ignore_index=True)
            logger.info(f"product data added: {len(product_data)}")
        except Exception as e:
            logger.error(f"Error while data is processing: {e}")
    
    def save_data(self):
        """Saves the data to an Excel file."""
        try:
            self.df.drop_duplicates(inplace=True)
            self.df.to_excel(self.config["OUTPUT_FILE"], index=False)
            logger.info(f"Data is saved to {self.config['OUTPUT_FILE']}")
        except Exception as e:
            logger.error(f"Error while data is saving: {e}")
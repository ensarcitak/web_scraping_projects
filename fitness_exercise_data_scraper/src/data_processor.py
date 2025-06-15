import pandas as pd
from src.config import CONFIG
from src.utils import logger
from src.translator import Translator

class DataProcessor:
    """Processes scraped data and saves to Excel."""
    
    def __init__(self):
        self.config = CONFIG
        self.translator = Translator()
        self.df = pd.DataFrame(columns=self.config["COLUMNS"])
    
    def process_data(self, exercise_data):
        """Processes and translates exercise data."""
        if not exercise_data:
            return
        
        # Translations
        if exercise_data.get("Body Part"):
            exercise_data["Body Part"] = self.translator.translate(exercise_data["Body Part"])
        if exercise_data.get("Equipment"):
            exercise_data["Equipment"] = self.translator.translate(exercise_data["Equipment"])
        if exercise_data.get("Instructions"):
            exercise_data["Instructions"] = self.translator.translate(exercise_data["Instructions"])
        
        # Add to dataframe
        try:
            temp_df = pd.DataFrame([exercise_data])
            self.df = pd.concat([self.df, temp_df], ignore_index=True)
            logger.info(f"Exercise data added: {exercise_data.get('Exercise Name', 'Unknown')}")
        except Exception as e:
            logger.error(f"Error processing data: {e}")
    
    def save_data(self):
        """Saves processed data to Excel."""
        try:
            if self.df.empty:
                logger.warning("No data to save.")
                return
            
            # Translation corrections
            self.df.loc[self.df["Body Part"] == "Back", "Body Part"] = "Sırt"
            
            # Clean missing data
            self.df.dropna(inplace=True)
            self.df.reset_index(drop=True, inplace=True)
            
            # Save to Excel
            self.df.to_excel(self.config["EXCEL_FILE"], index=False)
            logger.info(f"Data saved: {self.config['EXCEL_FILE']}")
        
        except Exception as e:
            logger.error(f"Error saving data: {e}")
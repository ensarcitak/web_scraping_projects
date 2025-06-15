from src.scraper import NutritionScraper
from src.data_processor import DataProcessor
from src.utils import load_search_terms, logger
from src.config import CONFIG

def main():
    logger.info("The application is starting.")
    
    # Load search terms from the input file
    search_terms = load_search_terms(CONFIG["INPUT_FILE"])
    if not search_terms:
        logger.error("Search terms not found, terminating the application.")
        return
    
    # Start the scraper and processor
    scraper = NutritionScraper()
    processor = DataProcessor()
    
    try:
        scraper.setup_driver()
        
        # Scrape data for each search term
        for term in search_terms:
            logger.info(f"Search term is processing: {term}")
            product_data = scraper.scrape_product_data(term)
            processor.process_data(product_data)
        
        # Save the processed data to an Excel file
        processor.save_data()
        
    except Exception as e:
        logger.error(f"error while the app starting: {e}")
    finally:
        scraper.close_driver()
        logger.info("Uygulama sonlandırıldı. the application is terminated.")
        logger.info("WebDriver is closed.")

if __name__ == "__main__":
    main()
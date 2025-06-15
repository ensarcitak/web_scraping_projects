from src.scraper import ExerciseScraper
from src.data_processor import DataProcessor
from src.utils import logger

def main():
    """Main function to orchestrate scraping and data processing."""
    logger.info("Application starting.")
    
    scraper = ExerciseScraper()
    processor = DataProcessor()
    
    try:
        # Collect exercise links
        exercise_links = scraper.get_exercise_links()
        if not exercise_links:
            logger.error("No exercise links found, application terminating.")
            return
        
        # Scrape data for each link
        for index, url in enumerate(exercise_links, 1):
            logger.info(f"Scraping exercise {index}/{len(exercise_links)}: {url}")
            exercise_data = scraper.scrape_exercise_data(url)
            processor.process_data(exercise_data)
        
        # Save data
        processor.save_data()
        
    except Exception as e:
        logger.error(f"Error running application: {e}")
    finally:
        scraper.close()
        logger.info("Application terminated.")

if __name__ == "__main__":
    main()
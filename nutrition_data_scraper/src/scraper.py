from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from src.config import CONFIG
from src.utils import logger
import time

class NutritionScraper:
    """Scrapes nutrition data from Diyetkolik.com."""
    
    def __init__(self):
        self.driver = None
        self.config = CONFIG
    
    def setup_driver(self):
        """Starts WebDriver."""
        try:
            service = Service(ChromeDriverManager().install())
            options = webdriver.ChromeOptions()
            options.add_argument("--headless") # Run in headless mode
            options.add_argument("--disable-gpu")
            self.driver = webdriver.Chrome(service=service, options=options)
            logger.info("WebDriver startes.")
        except Exception as e:
            logger.error(f"Error while WebDriver is starting: {e}")
            raise
    
    def close_driver(self):
        """Closes WebDriver."""
        if self.driver:
            self.driver.quit()
            logger.info("WebDriver closed.")
    
    def scrape_product_data(self, search_term):
        """Scrapes product data for the given search term."""
        formatted_term = search_term
        product_data = []
        page_number = 1
        
        while True:
            url = f"{self.config['BASE_URL']}{formatted_term}?p={page_number}"
            logger.info(f"data scraping from the page: {url}")
            self.driver.get(url)
            
            try:
                results = WebDriverWait(self.driver, self.config['TIMEOUT']).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.config['SELECTORS']['search_results']))
                )
            except Exception as e:
                logger.warning(f"Nothing found for {search_term}: {e}")
                break
            
            for index in range(len(results)):
                try:
                    results = self.driver.find_elements(By.CSS_SELECTOR, self.config['SELECTORS']['search_results'])
                    result = results[index]
                    product_name = result.text
                    result.click()
                    
                    # Choose 100 gram value
                    value_input = WebDriverWait(self.driver, self.config['TIMEOUT']).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, self.config['SELECTORS']['value_input']))
                    )
                    value_input.clear()
                    value_input.send_keys("100")
                    
                    # Choose gram unit
                    dropdown = WebDriverWait(self.driver, self.config['TIMEOUT']).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, self.config['SELECTORS']['unit_dropdown']))
                    )
                    dropdown.click()
                    gram_option = WebDriverWait(self.driver, self.config['TIMEOUT']).until(
                        EC.presence_of_element_located((By.XPATH, self.config['SELECTORS']['gram_option']))
                    )
                    gram_option.click()
                    
                    # Pull data
                    data = {"Urun_adi": product_name}
                    kcal_value = WebDriverWait(self.driver, self.config['TIMEOUT']).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, self.config['SELECTORS']['kcal_value']))
                    ).text
                    data["Kalori (kcal)"] = kcal_value
                    
                    table = self.driver.find_element(By.CSS_SELECTOR, self.config['SELECTORS']['nutrition_table'])
                    rows = table.find_elements(By.CSS_SELECTOR, self.config['SELECTORS']['table_rows'])
                    for row in rows:
                        th_elements = row.find_elements(By.CSS_SELECTOR, "tbody th")
                        if th_elements:
                            first_td = row.find_elements(By.TAG_NAME, "td")
                            if first_td:
                                key = th_elements[0].text
                                value = first_td[0].text
                                data[key] = value
                    
                    product_data.append(data)
                    self.driver.back()
                except Exception as e:
                    logger.warning(f"Error while scraping the product data: {e}")
                    self.driver.back()
                    continue
            
            # pagination check
            try:
                pagination = self.driver.find_element(By.CSS_SELECTOR, "ul.pagination")
                last_page_item = pagination.find_elements(By.TAG_NAME, "li")[-1]
                max_page_number = int(last_page_item.text)
                if page_number >= max_page_number:
                    break
            except Exception:
                break
            
            page_number += 1
            time.sleep(1)  # wair for rate limiting
        
        return product_data
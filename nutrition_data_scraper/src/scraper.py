from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from src.config import CONFIG
from src.utils import logger
import time

class NutritionScraper:
    """Scrapes nutritional data from diyetkolik.com."""
    
    def __init__(self):
        self.driver = None
        self.config = CONFIG
    
    def setup_driver(self):
        """start the WebDriver."""
        try:
            service = Service(ChromeDriverManager().install())
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")  # headless mode
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")  # for Linux environments
            options.add_argument("--disable-dev-shm-usage")  # for docker environments
            self.driver = webdriver.Chrome(service=service, options=options)
            logger.info("WebDriver started.")
        except Exception as e:
            logger.error(f"WebDriver starting error: {e}")
            raise
    
    def close_driver(self):
        """WebDriver closing."""
        if self.driver:
            self.driver.quit()
            logger.info("WebDriver closed.")
    
    def handle_cookie_popup(self):
        """Closes the cookie consent pop-up."""
        try:
            cookie_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            cookie_button.click()
            logger.info("Cookie consent pop-up closed.")
            time.sleep(1)  # wait until the popup is closed
        except TimeoutException:
            logger.debug("Could not find cookie popup, continuing.")
        except Exception as e:
            logger.warning(f"Error while processing cookie popup: {e}")
    
    def scrape_product_data(self, search_term):
        """Scrapes product data for the given search term."""
        formatted_term = search_term
        product_data = []
        page_number = 1
        
        while True:
            url = f"{self.config['BASE_URL']}{formatted_term}?p={page_number}"
            logger.info(f"data is scraping from the page: {url}")
            self.driver.get(url)
            
            # Çerez pop-up'ını kontrol et
            self.handle_cookie_popup()
            
            try:
                results = WebDriverWait(self.driver, self.config['TIMEOUT']).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.config['SELECTORS']['search_results']))
                )
                logger.info(f"found {len(results)} products.")
            except TimeoutException:
                logger.warning(f"no result found for {search_term}.")
                break
            except Exception as e:
                logger.error(f"error while search results are taking: {e}")
                break
            
            for index, result in enumerate(results):
                try:
                    # Ürün adını al
                    product_name = result.text
                    logger.debug(f"The product is processing: {product_name}")
                    
                    # Element tıklanabilir olana kadar bekle
                    WebDriverWait(self.driver, self.config['TIMEOUT']).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, self.config['SELECTORS']['search_results']))
                    )
                    result.click()
                    
                    # choose 100 gram
                    value_input = WebDriverWait(self.driver, self.config['TIMEOUT']).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, self.config['SELECTORS']['value_input']))
                    )
                    value_input.clear()
                    value_input.send_keys("100")
                    
                    # choose gram uint
                    dropdown = WebDriverWait(self.driver, self.config['TIMEOUT']).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, self.config['SELECTORS']['unit_dropdown']))
                    )
                    dropdown.click()
                    gram_option = WebDriverWait(self.driver, self.config['TIMEOUT']).until(
                        EC.element_to_be_clickable((By.XPATH, self.config['SELECTORS']['gram_option']))
                    )
                    gram_option.click()
                    
                    # pull data
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
                    logger.info(f"product data is added: {product_name}")
                    self.driver.back()
                    time.sleep(1)  # wait for the page to load
                except ElementClickInterceptedException as e:
                    logger.warning(f"Click banned: {e}")
                    self.driver.execute_script(self.config['SCROLL_SCRIPT'])
                    time.sleep(1)
                    continue
                except TimeoutException as e:
                    logger.warning(f"timeout error: {e}")
                    self.driver.back()
                    continue
                except NoSuchElementException as e:
                    logger.warning(f"Element not found: {e}")
                    self.driver.back()
                    continue
                except Exception as e:
                    logger.error(f"error while scraping product data: {e}")
                    self.driver.back()
                    continue
            
            # Pagination control
            try:
                pagination = self.driver.find_element(By.CSS_SELECTOR, "ul.pagination")
                last_page_item = pagination.find_elements(By.TAG_NAME, "li")[-1]
                max_page_number = int(last_page_item.text)
                if page_number >= max_page_number:
                    break
            except NoSuchElementException:
                logger.debug("Paging is not found, only one page.")
                break
            except ValueError:
                logger.warning("Page number could not be retrieved." )
                break
            except Exception as e:
                logger.error(f"Pagination control error: {e}")
                break
            
            page_number += 1
            time.sleep(2)  # Wait for the new page to load
        
        return product_data
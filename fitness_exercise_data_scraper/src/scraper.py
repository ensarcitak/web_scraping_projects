import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os
from src.config import CONFIG
from src.utils import logger, ensure_directory

class ExerciseScraper:
    """Scrapes exercise data and videos from exercisetimer.net."""
    
    def __init__(self):
        self.config = CONFIG
        self.session = requests.Session()
        ensure_directory(self.config["VIDEO_DIR"])
    
    def get_exercise_links(self):
        """Collects exercise links from library pages."""
        exercise_links = []
        for page_number in range(0, self.config["MAX_PAGES"]):
            url = self.config["LIBRARY_URL"] if page_number == 0 else f"{self.config['LIBRARY_URL']}?page={page_number}"
            logger.info(f"Scraping page: {url}")
            
            try:
                response = self.session.get(url, timeout=self.config["TIMEOUT"])
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                
                links = soup.select(self.config["SELECTORS"]["exercise_links"])
                for link in links:
                    href = link.get("href")
                    if href:
                        full_url = href if href.startswith("http") else f"{self.config['BASE_URL']}{href}"
                        exercise_links.append(full_url)
                logger.info(f"Found {len(links)} links.")
            
            except requests.RequestException as e:
                logger.error(f"Error scraping page: {e}")
                continue
        
        logger.info(f"Collected {len(exercise_links)} exercise links.")
        return list(set(exercise_links))  # Remove duplicates
    
    def scrape_exercise_data(self, url):
        """Scrapes data and downloads video for a single exercise."""
        exercise_data = {}
        try:
            response = self.session.get(url, timeout=self.config["TIMEOUT"])
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Exercise name
            title = soup.select_one(self.config["SELECTORS"]["title"])
            exercise_data["Exercise Name"] = title.get_text(strip=True) if title else ""
            
            # Video URL and download
            video_source = soup.select_one(self.config["SELECTORS"]["video_tag"])
            if video_source and video_source.get("src"):
                video_url = video_source["src"]
                video_url = video_url if video_url.startswith("http") else f"{self.config['BASE_URL']}{video_url}"
                
                parsed_url = urlparse(video_url)
                video_filename = os.path.basename(parsed_url.path)
                video_filepath = os.path.join(self.config["VIDEO_DIR"], video_filename)
                
                if not os.path.exists(video_filepath):
                    video_response = self.session.get(video_url, stream=True, timeout=self.config["TIMEOUT"])
                    video_response.raise_for_status()
                    with open(video_filepath, "wb") as video_file:
                        for chunk in video_response.iter_content(chunk_size=1024):
                            if chunk:
                                video_file.write(chunk)
                    logger.info(f"Video downloaded: {video_filepath}")
                else:
                    logger.debug(f"Video already exists: {video_filepath}")
                
                exercise_data["Video URL"] = video_filepath
            else:
                logger.warning(f"No video found: {url}")
            
            # Body part and equipment
            content_divs = soup.select(self.config["SELECTORS"]["content_divs"])
            if len(content_divs) >= 2:
                exercise_data["Equipment"] = content_divs[0].get_text(strip=True)
                exercise_data["Body Part"] = content_divs[1].get_text(strip=True)
            else:
                logger.warning(f"Insufficient content divs found: {url}")
            
            # Instructions
            description_items = soup.select(self.config["SELECTORS"]["description_list"])
            if description_items:
                steps = [item.get_text(strip=True) for item in description_items]
                exercise_data["Instructions"] = " ".join(steps)
            else:
                logger.warning(f"No instructions found: {url}")
            
            return exercise_data
        
        except requests.RequestException as e:
            logger.error(f"Error scraping exercise data: {e}")
            return {}
    
    def close(self):
        """Closes the session."""
        self.session.close()
        logger.info("Requests session closed.")
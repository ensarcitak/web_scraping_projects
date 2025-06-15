# Nutrition Data Scraper

This project scrapes **nutritional data** (calories, protein, fat, carbohydrates, etc.) for Turkish foods, drinks, and brands from [diyetkolik.com](https://www.diyetkolik.com), and saves the results into an Excel file. It uses **Selenium** for web automation and reads search terms from a `.txt` file to allow flexibility and easy customization.

> ⚠️ **Note:** The structure of diyetkolik.com may change over time. If the CSS selectors or page layout is updated, you may need to modify the scraping logic accordingly in `config.py`.

---

## 🚀 Features

- Automatically scrapes nutrition data for Turkish food, beverages, and brand-name items.
- Dynamically reads search terms from `data/input/search_terms.txt`. (This txt file includes the names of foods, beverages and brands. To give some examples: "pirinç pilavı, cacık, kahve, ülker, eti...")
- Saves results in a clean Excel file: `data/output/calorie_dataset.xlsx`.
- Modular codebase: scraping, data processing, and utility functions are separated.
- Robust error handling and logging for stable operation.

---

## 🗂️ Project Structure

```bash
nutrition_data_scraper/
├── src/
│ ├── init.py
│ ├── scraper.py # Scraping logic
│ ├── data_processor.py # Data processing and export
│ ├── config.py # Configuration and CSS selectors
│ └── utils.py # Helper functions
├── data/
│ ├── input/
│ │ └── terimler.txt # Search terms (comma-separated)
│ └── output/
│ └── calorie_dataset.xlsx
├── main.py # Entry point for the scraper
├── requirements.txt # Python dependencies
├── README.md # Project documentation
```

---

## ⚙️ Installation

### Python Requirements

- Python 3.8 or higher is required.

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Chrome and ChromeDriver

- Google Chrome must be installed.
- webdriver_manager automatically downloads the correct ChromeDriver version.

---

## 📥 Input File: Search Terms

The scraper reads comma-separated keywords from the following file:

```bash
data/input/search_terms.txt
```
To add new items, simply edit this file.

---

## ▶️ Usage

Clone the repository:

```bash
git clone https://github.com/[your-username]/nutrition_data_scraper.git
```

Navigate to the project directory:

```bash
cd nutrition_data_scraper
```

(Optional) Create a virtual environment:

```bash
python -m venv nutrition_scraper_venv
source nutrition_scraper_venv/bin/activate      # Linux/Mac
nutrition_scraper_venv\Scripts\activate         # Windows
```

> ⚠️ **Note:** search_terms.txt is not shared to you. Create the data and input folders and put your search_terms.txt file inside of input folder.


Run the main script:

```bash
python main.py
```

## Output

Scraped data is saved in: **data/output/calorie_dataset.xlsx**

**Logs are printed** to console and written to **scraper.log**

---

## 🛠️ Troubleshooting

- Cookie pop-ups: If the website displays a cookie banner, handle_cookie_popup() in scraper.py handles it. Update the cookie_accept selector in config.py if it changes.

- Timeout errors: If the page doesn't load properly, increase the TIMEOUT value in config.py (e.g., to 20 seconds).

- Layout changes: If the page structure changes, update the SELECTORS dictionary in config.py.

- Always check the scraper.log file for detailed error messages.

---

## 📬 Contact
For any questions or suggestions, please open an issue on the GitHub repository.

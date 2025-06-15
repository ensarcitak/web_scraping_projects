# 🏋️‍♂️ Fitness Exercise Data Scraper

**Fitness Exercise Data Scraper** is a Python-based tool designed to scrape exercise data from [exercisetimer.net](https://exercisetimer.net). It extracts comprehensive exercise information, including:

- Exercise names
- Targeted body parts
- Required equipment
- Instructional videos
- Step-by-step instructions

The data is translated from English to Turkish using the Google Translate API, cleaned, and exported into a structured Excel file. Additionally, exercise videos are downloaded and saved locally.

> ⚠️ **Note:** The structure of exercisetimer.net may change over time, requiring updates to selectors or scraping logic. The Google Translate API has free usage limits that may impact large-scale scraping.

---

## 🔧 Features

- **Web Scraping:** Extracts exercise data from multiple pages of the exercise library.
- **Video Downloading:** Downloads instructional videos and saves them locally.
- **Translation:** Translates exercise metadata and instructions into Turkish.
- **Data Processing:** Cleans and deduplicates data, saving it as an Excel file.
- **Modular Design:** Logic is split into well-structured Python modules.
- **Error Handling:** Gracefully handles network issues, missing data, and translation failures.
- **Logging:** Logs all operations to both the console and a `scraper.log` file.
- **Cross-Platform:** Uses dynamic paths to ensure compatibility with different OS environments.

---

## 📁 Project Structure

```
fitness_exercise_data_scraper/
├── src/
│   ├── __init__.py
│   ├── scraper.py              # Scraping and video download logic
│   ├── translator.py           # Translation logic
│   ├── data_processor.py       # Excel creation and data cleaning
│   ├── config.py               # Centralized configuration
│   └── utils.py                # Logging, path handling, etc.
├── data/
│   └── output/
│       ├── videos/             # Downloaded videos
│       └── fitness_exercises_dataset.xlsx
├── main.py                     # Application entry point
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

## ✅ Prerequisites

- **Python** 3.8 or above
- **OS**: Windows / Linux / macOS
- **Internet connection**: Required for scraping, downloading, and translation
- **Disk space**: Enough to store downloaded videos

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/fitness_exercise_data_scraper.git
cd fitness_exercise_data_scraper
```

### 2. (Optional) Create a Virtual Environment

```bash
python -m venv venv
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

### 1. Navigate to the Project Directory

```bash
cd fitness_exercise_data_scraper
```

### 2. Activate the Virtual Environment (if created)

```bash
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 3. Run the Scraper

```bash
python main.py
```

---

## 📆 Output

- **Excel File**: `data/output/fitness_exercises_dataset.xlsx`
- **Videos**: Saved to `data/output/videos/`
- **Logs**: Detailed logs in `scraper.log`

### Excel File Columns

- `Exercise Name` – e.g., “Push-Up”
- `Body Part` – e.g., “Chest” (translated: “Göğüs”)
- `Equipment` – e.g., “None” (translated: “Hiçbiri”)
- `Video URL` – Local path to downloaded video
- `Instructions` – Translated step-by-step exercise guide

---

## 🛠 Configuration

You can modify the following parameters in `src/config.py`:

```python
CONFIG = {
    "BASE_URL": "https://exercisetimer.net",
    "LIBRARY_URL": "https://exercisetimer.net/exercise-library",
    "OUTPUT_DIR": "data/output",
    "VIDEO_DIR": "data/output/videos",
    "EXCEL_FILE": "data/output/fitness_exercises_dataset.xlsx",
    "SELECTORS": {
        "EXERCISE_LINK": "a.card",
        ...
    },
    "TIMEOUT": 10,
    "MAX_PAGES": 65
}
```

---

## 🧪 Troubleshooting

### 🔌 Network Errors

**Symptom:** Timeout errors\
**Fix:** Check your connection or increase `TIMEOUT` in `config.py`.

### 🌐 Translation Errors

**Symptom:** Missing translations\
**Fix:** Google Translate API limits may have been reached. Wait or switch to another API.

### 🧱 Website Structure Changed

**Symptom:** Empty or incomplete data\
**Fix:** Update CSS selectors in `config.py`.

### 📼 Video Download Fails

**Symptom:** Videos not downloaded\
**Fix:** Ensure `data/output/videos/` is writable and has enough disk space.

### 📊 Excel File Not Created

**Symptom:** No Excel output\
**Fix:** Install missing dependencies like `openpyxl`, and check logs.

---

## 🤝 Contributing

Contributions are welcome!\
Please:

1. Fork the repo
2. Create a feature branch
3. Commit your changes
4. Push and open a Pull Request

```bash
git checkout -b feature/my-feature
git add .
git commit -m "Add my feature"
git push origin feature/my-feature
```

Also, please follow [PEP8](https://peps.python.org/pep-0008/) and add tests or documentation updates when applicable.

---

## 💡 Development Notes

- **Dynamic Pagination**: Currently hardcoded as 65 pages. Can be improved by detecting the last page dynamically.
- **Rate Limiting**: Add `time.sleep()` delays between requests to avoid throttling.
- **Alternative Translation APIs**: Integrate services like DeepL or Microsoft Translator if needed.
- **Parallel Requests**: Use `concurrent.futures` to speed up scraping.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 📬 Contact

For questions or feedback, open an issue on the [GitHub Issues](https://github.com/your-username/fitness_exercise_data_scraper/issues) page.

**Last Updated:** June 15, 2025


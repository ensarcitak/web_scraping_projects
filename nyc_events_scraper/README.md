# NYC Events Scraper and Transformer

This repository contains a Python-based pipeline to scrape event data from the New York events website and transform it into a structured, clean format for analysis.

---

## Overview

The project includes a scraper module (`scraper.py`) that collects event data from [https://new-york.events/](https://new-york.events/), a transformer module (`transformer.py`) that processes and cleans the data, and a main script (`main.py`) to orchestrate the pipeline. The output is saved as an Excel file (`nyc_events_cleaned.xlsx`) in the `output` directory.

---

## Features

- Scrapes event data categorized by type from the New York events website.
- Parses and transforms raw JSON data into a structured DataFrame.
- Exports cleaned data into an Excel file with relevant fields such as event name, date, time, duration, and location.
- Handles errors gracefully and logs the number of errors encountered during scraping.

---

## Requirements

- Python 3.x
- Required packages are listed in `requirements.txt`. Install them using:

```bash
pip install -r requirements.txt
```

---

## Installation

```bash
git clone <repository-url>
cd nyc_events_scraper
pip install -r requirements.txt
```

---

## Usage

Run the main script to execute the entire pipeline:

```bash
python main.py
```

This will:

Scrape event data and save it to data/nyc_events_data_all.json.

Transform the data and save the cleaned output to output/nyc_events_cleaned.xlsx.

Print progress and summary statistics to the console.

---

## Project Structure

```bash
nyc_events/
├── __init__.py          # Package initialization
├── scraper.py           # Web scraping logic
├── transformer.py       # Data transformation and export logic
data/                    # Directory for raw scraped data
output/                  # Directory for processed data output
main.py                  # Main script to run the pipeline
requirements.txt         # Project dependencies
```

---


For any questions or issues, please open an issue on the repository.








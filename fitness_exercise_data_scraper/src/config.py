import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG = {
    "BASE_URL": "https://exercisetimer.net",
    "LIBRARY_URL": "https://exercisetimer.net/exercise-library",
    "OUTPUT_DIR": os.path.join(BASE_DIR, "data", "output"),
    "VIDEO_DIR": os.path.join(BASE_DIR, "data", "output", "videos"),
    "EXCEL_FILE": os.path.join(BASE_DIR, "data", "output", "fitness_exercises_dataset.xlsx"),
    "COLUMNS": [
        "Exercise Name",
        "Body Part",
        "Equipment",
        "Video URL",
        "Instructions"
    ],
    "SELECTORS": {
        "exercise_links": "a.card",
        "video_tag": "video source",
        "title": "h1.description__title.h1",
        "content_divs": "div.description__content",
        "description_list": "ul.description__list li",
    },
    "TIMEOUT": 10,  # seconds for requests
    "MAX_PAGES": 65,  # Fixed number of pages (can be made dynamic)
}
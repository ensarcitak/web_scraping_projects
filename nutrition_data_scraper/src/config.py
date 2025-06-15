import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG = {
    "BASE_URL": "https://www.diyetkolik.com/kac-kalori/arama/",
    "INPUT_FILE": os.path.join(BASE_DIR, "data", "input", "search_terms.txt"),
    "OUTPUT_FILE": os.path.join(BASE_DIR, "data", "output", "calorie_dataset.xlsx"),
    "COLUMNS": [
        "Urun_adi",
        "Kalori (kcal)",
        "Karbonhidrat (g)",
        "Protein (g)",
        "Yag (g)",
        "Lif (g)",
        "Kolesterol (mg)",
        "Sodyum (mg)",
        "Potasyum (mg)",
    ],
    "SELECTORS": {
        "search_results": ".kkfs16.maviLink.d-block",
        "kcal_value": ".kkBigNumber.nut_kcal_count2",
        "nutrition_table": ".kkTable",
        "table_rows": "tr",
        "value_input": "#value_input",
        "unit_dropdown": ".select2-selection.select2-selection--single",
        "gram_option": "//li[contains(text(), 'Gram')]",
        "cookie_accept": "#onetrust-accept-btn-handler",
    },
    "TIMEOUT": 15,  # Artırılmış zaman aşımı süresi
    "SCROLL_SCRIPT": "window.scrollBy(0, 300);",
}
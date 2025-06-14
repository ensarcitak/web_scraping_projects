import requests
from bs4 import BeautifulSoup
import json
import os

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'
}


def get_all_events(output_path="data/nyc_events_data_all.json"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    print("Scraping started...")

    base_url = "https://new-york.events/"
    response = requests.get(base_url, headers=HEADERS)
    soup_home = BeautifulSoup(response.content, "html.parser")

    categories = soup_home.select(
        "li[id*='menu-item']:not([class*='menu-item-type-custom']):not([class*='menu-item-home'])"
    )

    events = []
    errors = 0

    for category in categories:
        a_tag = category.find("a")
        category_name = a_tag.get_text(strip=True)

        if category_name in {"Venues", "Tours"}:
            continue

        print(f"Fetching category: {category_name}")
        page = 1

        while True:
            category_url = f"{a_tag['href']}?pagenum={page}"
            res = requests.get(category_url, headers=HEADERS)
            soup = BeautifulSoup(res.content, "html.parser")

            if soup.select_one("div.no-dates"):
                break

            ul = soup.select_one("ul.dates-list")
            if not ul:
                break

            scripts = ul.find_all("script")
            for script in scripts:
                try:
                    data = json.loads(script.get_text())
                    data["eventCategory"] = category_name
                    events.append(data)
                except json.JSONDecodeError:
                    errors += 1

            print(f"  → Page {page} done.")
            page += 1

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=4)

    print(f"Scraping complete. Total events: {len(events)}, Errors: {errors}")

from playwright.sync_api import sync_playwright
import pandas as pd
import os
import re
from urllib.parse import urljoin
import requests

def create_photos_folder():
    if 'photos' not in os.listdir():
        os.mkdir('photos')

def read_excel_file(filename):
    return pd.read_excel(filename)

selectors = {
    'searchBar': '.form-control.header__search-input'  # Only if needed
}

create_photos_folder()
df = read_excel_file('posters.xlsx')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    for i in range(len(df)):
        baseName = str(df['title'][i])
        game = baseName.lower().replace(' ', '-')

        try:
            # Navigate directly to game stats page
            full_url = f'https://games-stats.com/steam/game/{game}/'
            print(f"Opening {full_url}")
            page.goto(full_url)
            page.wait_for_timeout(5000)

            # Try to get the image
            img_src = page.locator(".img-fluid").first.get_attribute("src")
            if img_src:
                img_url = urljoin(page.url, img_src)
                img_data = requests.get(img_url).content

                # Clean filename
                safe_name = re.sub(r'[\\/*?:"<>|]', "", baseName)
                file_path = os.path.join("photos", f"{safe_name}.jpg")

                with open(file_path, "wb") as f:
                    f.write(img_data)
                print(f"Downloaded image for {baseName}")
            else:
                print(f"No image found for {baseName}")

        except Exception as e:
            print(f"Failed to process {baseName}: {e}")

    browser.close()

from playwright.sync_api import sync_playwright
import pycountry
from time import sleep
from testing_folium import add_country_circle
import pathlib
import os

# Resetting STATE Files
if os.path.exists("circles.json"):
    os.remove("circles.json")

# Constants
URL = "https://countryguessr.mrdo.fr"
refresh_timeout_ms = 2000
timeout_s = 1
current = None

print("Launching Chromium...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False) 

    # --- Tab 1: Game ---
    page = browser.new_page()
    page.add_init_script("""localStorage.setItem("isFirstTime", "True");""")
    page.goto(URL)
    page.wait_for_selector("h1", timeout=refresh_timeout_ms)

    # --- Tab 2: Map ---
    filepath = pathlib.Path("map.html").resolve()
    map_page = browser.new_page()
    map_page.goto(f"file://{filepath}")

    # --- Loop ---
    while True:
        value = str(page.evaluate("() => window.localStorage.getItem('submittedCountries')"))
        result = value.replace(']', "").replace('[', "").replace('"', "").replace(',', "")

        if not value:
            print('No country has been submitted yet')
        else:
            country = pycountry.countries.get(alpha_3=result[-3:])

            sleep(timeout_s)

            dt = page.evaluate("""() => {
                const country_distance = document.querySelector('[class="answerSquare answer7 badAnswer"]');
                const data = country_distance?.querySelector('.answerContent')?.innerText.trim();
                return data;
            }""")

            if country:
                str_dt = str(dt).replace(' ', "")
                int_dt = int(str_dt)

                # Prevent duplicate circles
                if result != current:
                    name = getattr(country, "name", None)
                    if name:
                        add_country_circle(name, int_dt)

                        # Refresh map tab instead of creating a new one
                        map_page.reload()

        current = result

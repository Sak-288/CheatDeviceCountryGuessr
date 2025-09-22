from playwright.sync_api import sync_playwright
import pycountry
from time import *
from testing_folium import draw_country_circle

# Setting up constants
URL = "https://countryguessr.mrdo.fr"
refresh_timeout_ms = 2000
timeout_s = 2
current = None

print("Launching Chromium...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False) 
    page = browser.new_page() # Launching Chromium
    page.add_init_script("""
    localStorage.setItem("isFirstTime", "True");
    """) # Adding cookies to fake being a customed user
    page.goto(URL) # Going to countryguessr

    # wait for the page to populate (adjust selector)
    page.wait_for_selector("h1", timeout=refresh_timeout_ms)
    # Loop
    while True:
        # Run JS in page to pick the newest guessed country and the info box
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
            }""").replace(" ", "")

            int_dt = int(dt)

            # Using map circle drawing function

            # Trying not to draw infinite circles
            if result == current:
                inputed = 1
            else:
                inputed = 0

            # Drawing circles on map ONLY if circle has not been drawn in the last guess
            if inputed > 0:
                pass
            elif country is None:
                pass
            else:
                my_country = country.__dict__
                name = my_country.get("_fields", {}).get("name")
                draw_country_circle(name, int_dt)
                inputed += 1
        current = result
      
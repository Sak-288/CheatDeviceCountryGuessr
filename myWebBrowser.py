from playwright.sync_api import sync_playwright
import pycountry
from time import *

# Setting up constants
URL = "https://countryguessr.mrdo.fr"
refresh_timeout_ms = 10000
timeout_s = 3

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
        value = page.evaluate("() => window.localStorage.getItem('submittedCountries')")
        print(f'This is VALUE : {value}')
        ex_val = str(value)
        ex_val.replace(']', "")
        ex_val.replace('[', "")
        ex_val.replace('"', "")
        print(f'This is EX VALUE : {ex_val}')
        if not value:
            print('No country has been submitted yet')
        else:
            print(f"This is THE VALUE : {value[-1]}")
            country = pycountry.countries.get(alpha_3=value[-1])

            dt = page.evaluate("""() => {const country_distance = document.querySelector('.answerSquare answer7 badAnswer');
            const data = country_distance.querySelector('.answerContent')?.innerText.trim();
            return data}""")

            print(dt)
        
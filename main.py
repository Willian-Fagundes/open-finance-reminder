import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# 1. Setup target URL and headers
url = "https://openfinancebrasil.atlassian.net/wiki/spaces/OF/pages/223773060/Campos+regulat+rios+-+DA+Canais+de+Atendimento" # <-- Replace with your target URL
def save_page_as_pdf(url, output_filename="webpage.pdf"):
    with sync_playwright() as p:
        # Launch a headless browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print(f"Loading {url}...")
        # Navigate and wait until the network is completely idle (images loaded)
        page.goto(url, wait_until="networkidle")
        
        # Emulate screen media to capture the desktop website look
        page.emulate_media(media="screen")
        
        print("Generating PDF...")
        # Save the rendered page directly to a PDF file
        page.pdf(
            path=output_filename, 
            format="A4", 
            print_background=True  # Keeps background colors and images intact
        )
        
        browser.close()
        print(f"Success! Visual PDF saved as '{output_filename}'")

# Execute the function
save_page_as_pdf(url)

import base64
import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

import csv
import time
import subprocess

from config import CHROME_PATH, CHROME_DEBUG_PORT, CHROME_PROFILE_DIR, BASE_URL, SEARCH_BASE, OUTPUT_FILE
from repo.db import init_db, save_results

DOC_URL = "https://www.cia.gov/readingroom/document/cia-rdp96-00788r001900760001-9"
OUTPUT_PATH = "documents/pdfs"


def directory_setup(path: str | Path) -> Path:
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def launch_chrome():
    """Launch Chrome with remote debugging enabled."""
    print("Launching Chrome...")
    subprocess.Popen([
        CHROME_PATH,
        f"--remote-debugging-port={CHROME_DEBUG_PORT}",
        f"--user-data-dir={CHROME_PROFILE_DIR}"
    ])


def get_driver():
    options = Options()
    options.add_experimental_option("debuggerAddress", f"127.0.0.1:{CHROME_DEBUG_PORT}")
    return webdriver.Chrome(options=options)


def navigate_to_root(driver):
    """Navigate to the CIA Reading Room root page to establish session cookie."""
    print(f"Navigating to root page: {BASE_URL}")
    driver.get(BASE_URL)
    time.sleep(2)
    print(f"Current URL: {driver.current_url}")


def scrap_cia_search_page(driver):
    result = []

    try:
        print(f"Scraping: {driver.current_url}")
        soup = BeautifulSoup(driver.page_source, "html.parser")
        result = parse_results(soup)
        print(f"Found {len(result)} results")

        if not result:
            with open("debug_page.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("No results found — saved debug_page.html for inspection")

    except Exception as e:
        print(f"Error: {e}")

    return result


def parse_results(soup):
    matches = []
    items = soup.select("ol.search-results li")

    for item in items:
        title_tag = item.select_one("h3.title a")
        title = title_tag.get_text(strip=True) if title_tag else "N/A"
        link = title_tag["href"] if title_tag and title_tag.has_attr("href") else "N/A"
        matches.append({"title": title, "link": link})

    return matches


def save_to_csv(records, filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "link"])
        writer.writeheader()
        writer.writerows(records)
    print(f"\nSaved {len(records)} records to '{filename}'")


def fetch_pdf_via_js(driver, pdf_url):
    """
    Use browser-side fetch() to get the PDF as base64, then write to disk.
    Since the fetch runs inside Chrome with the active session cookies,
    it bypasses the redirect protection.
    """
    print(f"Fetching PDF via browser fetch(): {pdf_url}")
    pdf_b64 = driver.execute_async_script("""
        var url = arguments[0];
        var callback = arguments[arguments.length - 1];
        fetch(url)
            .then(function(r) { return r.blob(); })
            .then(function(blob) {
                var reader = new FileReader();
                reader.onloadend = function() {
                    callback(reader.result.split(',')[1]);
                };
                reader.readAsDataURL(blob);
            })
            .catch(function(err) {
                callback(null);
            });
    """, pdf_url)
    return pdf_b64


def save_pdf(pdf_b64, filename):
    filepath = os.path.join(OUTPUT_PATH, filename)

    with open(filepath, "wb") as f:
        f.write(base64.b64decode(pdf_b64))


if __name__ == '__main__':
    try:
        directory_setup(OUTPUT_PATH)
        init_db()

        launch_chrome()
        time.sleep(2)

        web_driver = get_driver()
        navigate_to_root(web_driver)

        web_driver.get(SEARCH_BASE)
        time.sleep(2)
        print(f"Current URL: {web_driver.current_url}")
        results = scrap_cia_search_page(web_driver)

        save_to_csv(results, OUTPUT_FILE)
        save_results(results)

        print(f"Navigating to document page: {DOC_URL}")
        web_driver.get(DOC_URL)
        time.sleep(3)

    except FileNotFoundError:
        print(f"Chrome not found at: {CHROME_PATH}")

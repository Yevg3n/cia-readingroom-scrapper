from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import time
import subprocess

from config import CHROME_PATH, CHROME_DEBUG_PORT, CHROME_PROFILE_DIR, BASE_URL


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


if __name__ == '__main__':
    try:

        launch_chrome()
        time.sleep(2)

        web_driver = get_driver()
        navigate_to_root(web_driver)

    except FileNotFoundError:
        print(f"Chrome not found at: {CHROME_PATH}")

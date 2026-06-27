
SEARCH_KEYWORD = "stargate"
BASE_URL = "https://www.cia.gov/readingroom/"
SEARCH_BASE = f"https://www.cia.gov/readingroom/search/site/{SEARCH_KEYWORD}"
PAGES_TO_SCRAPE = 4
OUTPUT_FILE = f"cia_{SEARCH_KEYWORD}_results.csv"

# Chrome related
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CHROME_DEBUG_PORT = 9222
CHROME_PROFILE_DIR = r"C:\chrome-debug-profile"
from pathlib import Path

# =========================
# Website
# =========================
BASE_URL = "https://elpais.com"
OPINION_URL = f"{BASE_URL}/opinion/"

# =========================
# Browser
# =========================
HEADLESS = False
WAIT_TIME = 15

# =========================
# Scraper Settings
# =========================
MAX_ARTICLES = 5
MAX_RETRIES = 3
RETRY_WAIT_SECONDS = 10

# =========================
# Directories
# =========================
ROOT_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = ROOT_DIR / "output"
IMAGE_DIR = ROOT_DIR / "images"

OUTPUT_DIR.mkdir(exist_ok=True)
IMAGE_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "articles.json"

# =========================
# CSS SELECTORS
# =========================
ARTICLE_CARD = "article"
ARTICLE_TITLE = "h2 a"
ARTICLE_CATEGORY = "header a.c_k"

# =========================
# Article Selectors
# =========================
ARTICLE_BODY = "div.a_c.clearfix"
ARTICLE_HEADING = "h1"
ARTICLE_PARAGRAPHS = "p"
ARTICLE_IMAGE = "figure img"
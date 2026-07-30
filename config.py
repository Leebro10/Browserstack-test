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
# Directories
# =========================

ROOT_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = ROOT_DIR / "output"

IMAGE_DIR = ROOT_DIR / "images"

OUTPUT_DIR.mkdir(exist_ok=True)

IMAGE_DIR.mkdir(exist_ok=True)
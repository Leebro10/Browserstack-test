from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager


class ElPaisScraper:

    def __init__(self):

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

        self.wait = WebDriverWait(self.driver, 15)

    def open_opinion_page(self):

        self.driver.get("https://elpais.com/opinion/")

    def get_first_five_articles(self):

        self.wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "article h2 a")
            )
        )

        title_links = self.driver.find_elements(
            By.CSS_SELECTOR,
            "article h2 a"
        )

        articles = []

        seen = set()

        for link in title_links:

            title = link.text.strip()

            url = link.get_attribute("href")

            if not title:
                continue

            if url in seen:
                continue

            seen.add(url)

            articles.append(
                {
                    "title": title,
                    "url": url
                }
            )

            if len(articles) == 5:
                break

        return articles

    def close(self):

        self.driver.quit()
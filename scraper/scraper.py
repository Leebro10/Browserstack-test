from bs4 import BeautifulSoup  # Very important to fetch article content
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from exceptions.scraper_exceptions import VerificationPageException

from webdriver_manager.chrome import ChromeDriverManager

from config import (
    OPINION_URL,
    WAIT_TIME,
    HEADLESS,
    ARTICLE_CARD,
    ARTICLE_TITLE,
    ARTICLE_CATEGORY,
    ARTICLE_HEADING,
    ARTICLE_BODY,
    ARTICLE_PARAGRAPHS,
    ARTICLE_IMAGE,
)

from utils.logger import logger


class ElPaisScraper:

    def __init__(self):

        options = webdriver.ChromeOptions()

        if HEADLESS:
            options.add_argument("--headless=new")

        options.add_argument("--start-maximized")

        options.add_argument("--disable-notifications")

        options.add_argument("--disable-popup-blocking")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options,
        )

        self.wait = WebDriverWait(self.driver, WAIT_TIME)

    def check_verification_page(self):  # In future you might change this
        """
        Save the current page for debugging and raise an exception.
        """
        cards = self.driver.find_elements(By.CSS_SELECTOR, ARTICLE_CARD)

        body = self.driver.find_elements(
            By.CSS_SELECTOR,
            ARTICLE_BODY,
        )

        if cards or body:
            return

        print(self.driver.title)
        print(self.driver.current_url)

        # with open("verification.html", "w", encoding="utf-8") as f:
        #     f.write(self.driver.page_source)

        raise VerificationPageException(
            "Expected page elements were not found."
        )

    def open_opinion_page(self):

        logger.info("Opening El País Opinion page...")

        self.driver.get(OPINION_URL)

    def accept_cookies(self):
        """
        Cookie banner changes from time to time.

        If it isn't found, continue normally.
        """

        try:

            cookie_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//button[contains(., 'Aceptar') or contains(., 'Accept')]",
                    )
                )
            )

            cookie_button.click()

            """
            Added because your code assumed "No banner" means "No overlay."
            Not true. The overlay still existed.
            """

            self.wait.until(
                EC.invisibility_of_element_located(
                    (
                        By.ID,
                        "acceptationCMPWall",
                    )
                )
            )

            logger.info("Cookie banner accepted.")

        except Exception:

            logger.info("Cookie banner not present.")

    def get_article_cards(self):

        try:

            self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, ARTICLE_CARD)
                )
            )

        except TimeoutException:

            self.check_verification_page()
            raise

        cards = self.driver.find_elements(
            By.CSS_SELECTOR,
            ARTICLE_CARD,
        )

        if not cards:
            self.check_verification_page()

        return cards

    def open_article(self, url):

        self.driver.get(url)

        self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ARTICLE_BODY)
            )
        )     

    """def open_article(self, url):

        self.wait.until(
            lambda driver: len(
                driver.find_elements(By.CSS_SELECTOR, ARTICLE_CARD)
            ) > index
        )

        cards = self.driver.find_elements(
            By.CSS_SELECTOR,
            ARTICLE_CARD,
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            cards[index],
        )

        cards[index].click()

        try:

            self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ARTICLE_BODY)
                )
            )

        except TimeoutException:

            print(self.driver.current_url)

            print(self.driver.title)

            with open("article_timeout.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)

            raise"""

    def get_first_five_articles(self):

        cards = self.get_article_cards()

        articles = []

        for card in cards:

            try:

                title = card.find_element(
                    By.CSS_SELECTOR,
                    ARTICLE_TITLE
                ).text

                url = card.find_element(
                    By.CSS_SELECTOR,
                    ARTICLE_TITLE
                ).get_attribute("href")

                articles.append(
                    {
                        "title": title,
                        "url": url,
                    }
                )

                if len(articles) == 10:
                    break

            except Exception:
                continue

        return articles

    """def get_first_five_articles(self):

        logger.info("Collecting article cards...")

        try:

            self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, ARTICLE_CARD)
                )
            )

        except TimeoutException:

            logger.warning("Timed out waiting for article cards.")

            self.check_verification_page()

            raise

        cards = self.driver.find_elements(
            By.CSS_SELECTOR,
            ARTICLE_CARD,
        )

        if not cards:
            self.check_verification_page()

        articles = []

        for card in cards:

            try:

                title_element = card.find_element(
                    By.CSS_SELECTOR,
                    ARTICLE_TITLE,
                )

                category_element = card.find_element(
                    By.CSS_SELECTOR,
                    ARTICLE_CATEGORY,
                )

                title = title_element.text.strip()

                url = title_element.get_attribute("href")

                category = category_element.text.strip()

                if not title:

                    continue

                articles.append(
                    {
                        "title": title,
                        "url": url,
                        "category": category,
                    }
                )

                if len(articles) == 5:

                    break

            except Exception:
                continue

        logger.info(f"{len(articles)} articles collected.")

        return articles"""

    def extract_article_details(self):
        """
        Open the article using Selenium and parse the rendered HTML
        with BeautifulSoup.
        """

        logger.info(f"Extracting article: {self.driver.current_url}")

        print("=" * 80)
        print("Current URL :", self.driver.current_url)
        print("Page title  :", self.driver.title)

        soup = BeautifulSoup(
            self.driver.page_source,
            "html.parser",
        )

        title = ""

        title_element = soup.select_one(ARTICLE_HEADING)

        if title_element:
            title = title_element.get_text(" ", strip=True)

        body = soup.select_one(ARTICLE_BODY)

        if body is None:
            raise Exception("Article body not found.")

        paragraphs = body.select(ARTICLE_PARAGRAPHS)

        content = "\n".join(
            p.get_text(" ", strip=True)
            for p in paragraphs
        )

        image_url = None

        image = soup.select_one(ARTICLE_IMAGE)

        if image:
            image_url = image.get("src")

        logger.info("Article extracted successfully.")

        return {
            "title": title,
            "content": content,
            "image_url": image_url,
        }

    """def go_back_to_opinion(self):

        self.driver.back()

        self.wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ARTICLE_CARD)
            )
        )"""

    def close(self):

        logger.info("Closing browser.")

        self.driver.quit()
"""
PHASE 3 THIS WAS NO CHANGES WERE MADE PHASE 2 AND PHASE 3 SAME
"""
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

    def check_verification_page(self): #In future you might change this 
        """
        Save the current page for debugging and raise an exception.
        """
        print("\nPage title:", self.driver.title)
        print("Current URL:", self.driver.current_url)

        with open("verification.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)

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

            logger.info("Cookie banner accepted.")

        except Exception:

            logger.info("Cookie banner not present.")

    def get_first_five_articles(self):

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

        return articles

    def extract_article_details(self, url):
        """
        Opens an article and extracts its title, content and image URL.
        """

        logger.info(f"Opening article: {url}")

        self.driver.get(url)

        #self.check_verification_page()

        try:

            self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ARTICLE_BODY)
                )
            )

        except TimeoutException:

            logger.warning("Article body not found.")

            self.check_verification_page()

            raise

        paragraphs = self.driver.find_elements(
            By.CSS_SELECTOR,
            f"{ARTICLE_BODY} {ARTICLE_PARAGRAPHS}"
        )

        content = "\n".join(
            paragraph.text.strip()
            for paragraph in paragraphs
            if paragraph.text.strip()
        )

        if not content:

            logger.warning("Article has no content.")

        image_url = None

        try:

            image = self.driver.find_element(
                By.CSS_SELECTOR,
                ARTICLE_IMAGE,
            )

            image_url = image.get_attribute("src")

        except Exception:

            logger.info("No cover image found.")

        logger.info("Article extracted successfully.")
        return {
            "content": content,
            "image_url": image_url,
        }

    def close(self):

        logger.info("Closing browser.")

        self.driver.quit()

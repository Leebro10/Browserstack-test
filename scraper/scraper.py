import re
import os # For images
import requests # For images
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

    def __init__(self, driver=None):

        options = webdriver.ChromeOptions()

        if HEADLESS:
            options.add_argument("--headless=new")

            options.add_argument("--start-maximized")

            options.add_argument("--disable-notifications")

            options.add_argument("--disable-popup-blocking")

        if driver is not None:

            self.driver = driver

        else:

             options = webdriver.ChromeOptions()

        if HEADLESS:
            options.add_argument("--headless=new")


            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options,
    )

        self.wait = WebDriverWait(self.driver, WAIT_TIME)

    def check_verification_page(self):  # In future I might change this
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

    def get_first_five_articles(self):

        cards = self.get_article_cards()

        articles = []

        for card in cards:

            try:

                title_element = card.find_element(
                    By.CSS_SELECTOR,
                    ARTICLE_TITLE,
                )

                title = title_element.text.strip()

                if not title:
                    continue

                url = title_element.get_attribute("href")

                if (
                    not url
                    or "/opinion/" not in url
                ):
                    continue

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

            logger.warning(
                f"Skipping unsupported page: {self.driver.current_url}"
            )

            return None

        paragraphs = body.select(ARTICLE_PARAGRAPHS)

        content = "\n".join(
            p.get_text(" ", strip=True)
            for p in paragraphs
        )

        image = soup.select_one(ARTICLE_IMAGE)

        if image:
            image_url = image.get("src")

        logger.info("Article extracted successfully.")

        return {
            "title": title,
            "content": content,
            "image_url": image_url,
        }

    def download_image(self, image_url, article_number):
        """
        Download an article image and save it in the images folder.
        """

        if not image_url:

            logger.warning("No image URL found.")

            return

        os.makedirs("images", exist_ok=True)

        extension = image_url.split("?")[0].split(".")[-1]

        filename = f"article_{article_number}.{extension}"

        filepath = os.path.join("images", filename)

        try:

            response = requests.get(image_url, timeout=20)

            response.raise_for_status()

            with open(filepath, "wb") as file:

                file.write(response.content)

            logger.info(f"Image saved: {filepath}")

        except requests.RequestException as e:

            logger.warning(f"Failed to download image: {e}")

    def close(self):

        logger.info("Closing browser.")

        self.driver.quit()
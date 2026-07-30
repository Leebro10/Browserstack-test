#From Chatgpt I got this incase you want to try with differrnt Python veersion, you can come back
""" This is actually a known compatibility issue, not a mistake in your code.

The error:

ModuleNotFoundError: No module named 'distutils'

happens because:

You're likely using Python 3.12 or newer.
undetected_chromedriver still depends on the distutils module.
distutils was removed from the Python standard library starting with Python 3.12.
First, let's confirm your Python version

Run:

python --version

If it shows Python 3.12.x or Python 3.13.x, then this is exactly the cause.

The recommended solution

For this project, I recommend not using undetected_chromedriver.

Here's why:

Your original scraper already worked most of the time.
The CAPTCHA only appeared after several consecutive runs.
The project requirement is to scrape El País—not to bypass anti-bot protections.
Adding undetected_chromedriver introduces compatibility issues and an extra dependency without guaranteeing the CAPTCHA won't appear.

Instead, we can make your scraper more robust by:

using the normal Selenium driver,
detecting verification pages,
retrying automatically after a delay,
logging failures clearly.

That approach is simpler, more stable, and easier to maintain.

If you still want to use undetected_chromedriver

If your Python version is 3.12+, you'd need to either:

Use Python 3.11 in your virtual environment, or
Find a version of undetected_chromedriver that supports Python 3.12+ (support has varied by release).
My recommendation

I'd recommend reverting to your previous Selenium setup (using webdriver_manager) and then implementing the retry logic. Based on what you've shown so far, that gives you a cleaner and more reliable solution for this project without running into Python compatibility issues.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import undetected_chromedriver as uc

import random
import time
#from webdriver_manager.chrome import ChromeDriverManager
from exceptions.scraper_exceptions import VerificationPageException

from config import (
    OPINION_URL,
    WAIT_TIME,
    HEADLESS,
    ARTICLE_CARD,
    ARTICLE_TITLE,
    ARTICLE_CATEGORY,
)

from utils.logger import logger


class ElPaisScraper:

    def __init__(self):

        options = uc.ChromeOptions()

        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/138.0.0.0 Safari/537.36"
)

        if HEADLESS:
            options.add_argument("--headless=new")

        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")

        self.driver = uc.Chrome(
            options=options,
            headless=HEADLESS,
        )

        self.wait = WebDriverWait(self.driver, WAIT_TIME)

    def check_verification_page(self):
        """
        Detect if El País has shown an anti-bot verification page.
        """

        page = self.driver.page_source.lower()

        verification_keywords = [
            "verification required",
            "slide right",
            "secure your access",
            "unusual activity",
            "captcha",
            "access denied",
            "checking your browser",
            "cloudflare",
            "robot",
        ]

        for keyword in verification_keywords:

            if keyword in page:

                logger.warning(
                    f"Verification page detected ({keyword})"
                )

                raise VerificationPageException(
                    f"Verification page detected ({keyword})"
                )

    def open_opinion_page(self):

        logger.info("Opening El País Opinion page...")

        self.driver.get(OPINION_URL)

        time.sleep(random.uniform(2, 5))

        self.check_verification_page()

    def accept_cookies(self):

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

            logger.warning(
                "Timed out while waiting for article cards."
            )

            self.check_verification_page()

            raise Exception(
                "Opinion article cards could not be found."
            )

        cards = self.driver.find_elements(
            By.CSS_SELECTOR,
            ARTICLE_CARD,
        )

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

    def close(self):

        logger.info("Closing browser.")

        self.driver.quit()
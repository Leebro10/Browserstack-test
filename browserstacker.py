from scraper.translator import translate_text
import os
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from selenium import webdriver
from scraper.scraper import ElPaisScraper
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

load_dotenv()

USERNAME = os.getenv("BROWSERSTACK_USERNAME")
ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")

URL = (
    f"https://{USERNAME}:{ACCESS_KEY}"
    "@hub-cloud.browserstack.com/wd/hub"
)

BROWSERS = [

{
    "browserName": "Chrome",
    "browserVersion": "latest",
    "bstack:options": {
        "os": "Windows",
        "osVersion": "11",
        "buildName": "ElPais Scraper",
        "sessionName": "Chrome Test"
    },
},

{
    "browserName": "Firefox",
    "browserVersion": "latest",
    "bstack:options": {
        "os": "Windows",
        "osVersion": "11",
        "buildName": "ElPais Scraper",
        "sessionName": "Firefox Test"
    },
},

{
    "browserName": "Safari",
    "browserVersion": "latest",
    "bstack:options": {
        "os": "OS X",
        "osVersion": "Sonoma",
        "buildName": "ElPais Scraper",
        "sessionName": "Safari Test"
    },
},

{
    "browserName": "Chrome",
    "bstack:options": {
        "deviceName": "Samsung Galaxy S24",
        "osVersion": "14.0",
        "buildName": "ElPais Scraper",
        "sessionName": "Chrome Test"
    },
},

{
    "browserName": "Safari",
    "bstack:options": {
        "deviceName": "iPhone 15",
        "osVersion": "17",
        "buildName": "ElPais Scraper",
        "sessionName": "Safari Test"
    },
},

]

def run_browser(capabilities):

    options = Options()

    for key, value in capabilities.items():
        options.set_capability(key, value)

    driver = webdriver.Remote(
        command_executor=URL,
        options=options,
    )

    scraper = ElPaisScraper(driver=driver)

    from selenium.webdriver.support.ui import WebDriverWait

    scraper.wait = WebDriverWait(scraper.driver, 30)

    try:

        scraper.open_opinion_page()

        scraper.accept_cookies()

        articles = scraper.get_first_five_articles()[:5]

        print(
            f"{capabilities['browserName']} : "
            f"{len(articles)} articles found"
        )

        for index, article in enumerate(articles, start=1):

            try:

                scraper.open_article(article["url"])

                details = scraper.extract_article_details()

                if details is None:
                    continue

                print(
                    f"\n{capabilities['browserName']} - Article {index}"
                )

                print(f"Spanish Title : {details['title']}")

                english_title = translate_text(details["title"])

                print(f"English Title : {english_title}")

            except TimeoutException:

                print(
                    f"{capabilities['browserName']} : "
                    f"Timed out opening Article {index}."
                )

            except Exception as e:

                print(
                    f"{capabilities['browserName']} : "
                    f"Article {index} failed - {e}"
                )

    finally:

        scraper.close()

if __name__ == "__main__":

    with ThreadPoolExecutor(max_workers=5) as executor:

        list(
            executor.map(
                run_browser,
                BROWSERS,
            )
        )
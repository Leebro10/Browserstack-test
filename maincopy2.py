"""
PHASE 3 maincopy2.py before making changes so I created maincopy2.py and scrapercopy2.py
 
"""
from scraper.scraper import ElPaisScraper
from exceptions.scraper_exceptions import VerificationPageException
import time

def main():

    MAX_RETRIES = 3

    for attempt in range(1, MAX_RETRIES + 1):

        scraper = ElPaisScraper()

        try:

            scraper.open_opinion_page()

            scraper.accept_cookies()

            articles = scraper.get_first_five_articles()

            print("\n")
            print("=" * 90)
            print("FIRST FIVE OPINION ARTICLES")
            print("=" * 90)

            for index, article in enumerate(articles, start=1):

                details = scraper.extract_article_details(article["url"])

                print()
                print(f"Article {index}")
                print("-" * 90)
                print(f"Category : {article['category']}")
                print(f"Title    : {article['title']}")
                print(f"URL      : {article['url']}")

                print(f"Image URL: {details['image_url']}")

                print("\nContent:")
                print(details["content"])

            break

        except VerificationPageException:

            print(f"\nVerification page detected (Attempt {attempt}/{MAX_RETRIES})")

            if attempt < MAX_RETRIES:

                wait_time = 10 * attempt

                print(f"Waiting {wait_time} seconds before retrying...")

                time.sleep(wait_time)

            else:

                print("\nMaximum retry attempts reached.")

        finally:

            scraper.close()

if __name__ == "__main__":
    main()
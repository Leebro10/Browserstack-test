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

            print("\n")
            print("=" * 90)
            print("FIRST FIVE OPINION ARTICLES")
            print("=" * 90)
            
            """
            Later we'll add translation and image downloading inside this loop
            """
            """
            for article in articles:
                details = scraper.extract_article_details(article["url"])

                print()
                print("-" * 90)
                print(article["title"])

                print()
            """

            articles = scraper.get_first_five_articles()

            for index, article in enumerate(articles, start=1):

                scraper.driver.get(article["url"])

                details = scraper.extract_article_details()

                print()
                print(f"Article {index}")
                print("-" * 90)

                print(f"Title : {details['title']}")

                if details["image_url"]:
                    print(f"Image URL: {details['image_url']}")
                else:
                    print("Image URL: Not available")

                print()
                print("Content:")

                if details["content"]:
                    print(details["content"])
                else:
                    print("Content could not be fetched.")

            """articles = scraper.get_first_five_articles()

            for index, article in enumerate(articles, start=1):

                scraper.open_article(article["url"])

                details = scraper.extract_article_details() 

                print()
                print(f"Article {index + 1}")
                print("-" * 90)

                print(f"Title : {details['title']}")

                if details["image_url"]:
                    print(f"Image URL: {details['image_url']}")
                else:
                    print("Image URL: Not available")

                print()
                print("Content:")

                if details["content"]:
                    print(details["content"])
                else:
                    print("Content could not be fetched.")

                #scraper.go_back_to_opinion()

            break

        except VerificationPageException:

            print(f"\nVerification page detected (Attempt {attempt}/{MAX_RETRIES})")

            if attempt < MAX_RETRIES:

                wait_time = 10 * attempt

                print(f"Waiting {wait_time} seconds before retrying...")

                time.sleep(wait_time)

            else:

                print("\nMaximum retry attempts reached.")
"""
        finally:

            scraper.close()

if __name__ == "__main__":
    main()
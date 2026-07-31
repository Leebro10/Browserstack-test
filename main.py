from scraper.scraper import ElPaisScraper
from exceptions.scraper_exceptions import VerificationPageException
from scraper.translator import translate_text
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

            articles = scraper.get_first_five_articles()

            count = 1

            for article in articles:

                scraper.driver.get(article["url"])

                try:
                    details = scraper.extract_article_details()
                    english_title = translate_text(details["title"])
                    print(f"Spanish Title : {details['title']}")
                    print(f"English Title : {english_title}")
                    if details is None:
                        continue

                except Exception:

                    print(f"Skipping article: {article['url']}")
                    continue

                print()
                print(f"Article {count}")
                print("-" * 90)

                print(f"Title : {details['title']}")

                if details["image_url"]:
                    print(f"Image URL: {details['image_url']}")
                else:
                    print("Image URL: Not available")
                if details["image_url"]:
                    scraper.download_image(
                        details["image_url"],
                        count
                    )

                print()
                print("Content:")

                if details["content"]:
                    print(details["content"])
                else:
                    print("Content could not be fetched.")

                count += 1

                if count > 5:
                    break

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
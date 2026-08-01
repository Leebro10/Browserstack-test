import json
from config import OUTPUT_FILE
from collections import Counter
import re
from scraper.scraper import ElPaisScraper
from exceptions.scraper_exceptions import VerificationPageException
from scraper.translator import translate_text
import time
from colorama import Fore, Style, init

init(autoreset=True)


def main():

    from config import MAX_RETRIES

    for attempt in range(1, MAX_RETRIES + 1):

        scraper = ElPaisScraper()

        try:

            scraper.open_opinion_page()

            scraper.accept_cookies()

            print("\n")
            print("=" * 90)
            print("ARTICLES SCRAPING IN PROCESS....")
            print("=" * 90)

            articles = scraper.get_first_five_articles()

            translated_titles = []
            scraped_articles = []

            count = 1

            for article in articles:

                scraper.driver.get(article["url"])

                try:

                    details = scraper.extract_article_details()

                    if details is None:
                        continue

                    english_title = translate_text(details["title"])
                    translated_titles.append(english_title)

                    scraped_articles.append(
                    {
                        "title": details["title"],
                        "translated_title": english_title,
                        "url": article["url"],
                        "image_url": details["image_url"],
                        "content": details["content"]
                    }
                )

                    print(f"Spanish Title : {details['title']}")
                    print(f"English Title : {english_title}")

                except Exception:

                    print(f"Skipping article: {article['url']}")
                    continue

                print()
                print(Fore.CYAN + f"ARTICLE {count}")
                print(Fore.CYAN + "-" * 90)

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
            # Save all scraped articles to JSON
            with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
                json.dump(
                    scraped_articles,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

            print()
            print(Fore.GREEN + "=" * 90)
            print(Fore.GREEN + "ARTICLES SAVED SUCCESSFULLY")
            print(Fore.GREEN + "=" * 90)

            print(Fore.CYAN + f"Location : {OUTPUT_FILE}")
            print(Fore.YELLOW + f"Total Articles : {len(scraped_articles)}")
            print()

            print()
            print(Fore.MAGENTA + "=" * 90)
            print(Fore.MAGENTA + "REPEATED WORDS ARE")
            print(Fore.MAGENTA + "=" * 90)

            all_words = []

            for title in translated_titles:

                words = re.findall(
                    r"[a-zA-Z']+",
                    title.lower()
                )

                all_words.extend(words)

            word_counts = Counter(all_words)

            found = False

            for word, frequency in word_counts.items():

                if frequency > 2:

                    print(Fore.GREEN + f"{word} : {frequency}")
                    found = True

            if not found:

                print(Fore.YELLOW + "No words appeared more than twice.")

            break

        except VerificationPageException:

            print(f"\nVerification page detected (Attempt {attempt}/{MAX_RETRIES})")

            if attempt < MAX_RETRIES:
                from config import RETRY_WAIT_SECONDS

                wait_time = RETRY_WAIT_SECONDS * attempt

                print(f"Waiting {wait_time} seconds before retrying...")

                time.sleep(wait_time)

            else:

                print("\nMaximum retry attempts reached.")

        finally:

            scraper.close()


if __name__ == "__main__":
    main()
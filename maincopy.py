"""
This code works before applying a max 3 times retry version
"""

from scraper.scraper import ElPaisScraper


def main():

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

            print()

            print(f"Article {index}")

            print("-" * 90)

            print("Category :", article["category"])

            print("Title    :", article["title"])

            print("URL      :", article["url"])

    finally:

        scraper.close()


if __name__ == "__main__":

    main()

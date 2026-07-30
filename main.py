from scraper.scraper import ElPaisScraper


def main():

    scraper = ElPaisScraper()

    scraper.open_opinion_page()

    articles = scraper.get_first_five_articles()

    print("\nFIRST FIVE ARTICLES\n")

    for i, article in enumerate(articles, start=1):

        print("=" * 80)

        print(f"Article {i}")

        print("Title :", article["title"])

        print("URL   :", article["url"])

    scraper.close()


if __name__ == "__main__":
    main()
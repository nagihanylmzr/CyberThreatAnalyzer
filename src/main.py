from crawler import NewsCrawler
from config import RAW_DATA_DIR
from utils import save_json


def main():

    crawler = NewsCrawler()

    news = crawler.fetch_news()

    print(f"{len(news)} news collected.")

    save_json(
        news,
        RAW_DATA_DIR / "news.json"
    )

    print("Saved to:", RAW_DATA_DIR / "news.json")


if __name__ == "__main__":
    main()
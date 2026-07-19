import requests
from bs4 import BeautifulSoup


class NewsCrawler:

    def __init__(self):
        self.url = "https://thehackernews.com/"

    def fetch_news(self):
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/126.0 Safari/537.36"
            )
        }

        response = requests.get(self.url, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        news_list = []

        articles = soup.select("div.body-post")

        for article in articles:

            title_tag = article.select_one("h2.home-title")
            link_tag = article.select_one("a.story-link")

            if not title_tag or not link_tag:
                continue

            news = {
                "title": title_tag.get_text(strip=True),
                "url": link_tag["href"],
                "source": "The Hacker News"
            }

            news_list.append(news)

        return news_list
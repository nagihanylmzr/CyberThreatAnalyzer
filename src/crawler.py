import random
import time

import requests
from bs4 import BeautifulSoup


class NewsCrawler:

    def __init__(self):
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/126.0 Safari/537.36"
            )
        }
        self.securityweek_url = "https://www.securityweek.com/"
        self.thehackernews_url = "https://thehackernews.com/"
        self.bleepingcomputer_url = "https://www.bleepingcomputer.com/news/security/"

    def fetch_securityweek(self):

        response = requests.get(
            self.securityweek_url,
            headers=self.headers,
            timeout=30
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        news = []

        articles = soup.select("article")

        for article in articles:

            title_tag = article.select_one("h2 a")

            if not title_tag:
                continue

            href = title_tag.get("href")

            if not href:
                continue

            news.append({
                "title": title_tag.get_text(strip=True),
                "url": href,
                "source": "SecurityWeek"
            })

        return news
    def fetch_thehackernews(self):

        response = requests.get(
            self.thehackernews_url,
            headers=self.headers,
            timeout=30
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        news = []

        for article in soup.select("div.body-post"):

            title = article.select_one("h2.home-title")
            link = article.select_one("a.story-link")

            if not title or not link:
                continue

            news.append({
                "title": title.get_text(strip=True),
                "url": link["href"],
                "source": "The Hacker News"
            })

        return news

    def fetch_bleepingcomputer(self):

        response = requests.get(
            self.bleepingcomputer_url,
            headers=self.headers,
            timeout=30
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        news = []

        articles = soup.select("#bc-home-news-main-wrap > li")

        for article in articles:

            title_tag = article.select_one("h4 a")

            if not title_tag:
                continue

            href = title_tag["href"]

            if "/news/security/" not in href:
                continue

            news.append({
                "title": title_tag.get_text(strip=True),
                "url": href,
                "source": "BleepingComputer"
            })

        return news

        soup = BeautifulSoup(response.text, "lxml")

        news = []

        for article in soup.select("li.c-card"):

            title = article.select_one("h4")
            link = article.select_one("a")

            if not title or not link:
                continue

            news.append({
                "title": title.get_text(strip=True),
                "url": link["href"],
                "source": "BleepingComputer"
            })

        return news

    def fetch_news(self):

        news = []

        news.extend(self.fetch_thehackernews())

        try:
            news.extend(self.fetch_bleepingcomputer())
        except Exception as e:
            print(f"BleepingComputer error: {e}")

        try:
            news.extend(self.fetch_securityweek())
        except Exception as e:
            print(f"SecurityWeek error: {e}")

        return news

    def fetch_article(self, url):

        time.sleep(random.uniform(2, 5))

        response = requests.get(
            url,
            headers=self.headers,
            timeout=30
        )

        if response.status_code == 429:
            print("Rate limit reached.")
            return ""

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        paragraphs = soup.select("div.articlebody p")

        if not paragraphs:
            paragraphs = soup.select("article p")

        return " ".join(
            p.get_text(" ", strip=True)
            for p in paragraphs
        )
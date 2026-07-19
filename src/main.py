from crawler import NewsCrawler
from config import RAW_DATA_DIR
from utils import save_json
from report import ReportGenerator
from database import DatabaseManager
from extractor import CompanyExtractor
from classifier import EntityClassifier
from scorer import ThreatScorer


def main():
    crawler = NewsCrawler()
    extractor = CompanyExtractor()
    classifier = EntityClassifier()
    database = DatabaseManager()
    report = ReportGenerator()
    scorer = ThreatScorer()

    database.create_tables()

    news = crawler.fetch_news()

    print(f"{len(news)} news collected.")

    all_companies = []

    for article in news:
        title = article.get("title", "")

        try:
            content = crawler.fetch_article(article["url"])
        except Exception as e:
            print(f"Article could not be fetched: {e}")
            continue

        # Risk puanı hesapla
        risk_score = scorer.score(content)

        # Entity'leri çıkar
        entities = extractor.extract_entities(content)

        # Şirketleri filtrele
        companies = []

        for entity in entities:
            if classifier.classify(entity) == "Company":
                companies.append(entity)

        # Rapor için şirketleri topla
        all_companies.extend(companies)

        # JSON bilgileri
        article["content"] = content
        article["entities"] = entities
        article["companies"] = companies
        article["risk_score"] = risk_score

        # Veritabanına kaydet
        article_id = database.insert_article(
            title,
            article["url"],
            article["source"],
            content,
            risk_score
        )

        for company in companies:
            database.insert_company(article_id, company)

        # Terminal çıktısı
        print(title)
        print(f"Risk Score: {risk_score}")
        print("Companies:", companies)
        print("-" * 50)

    # JSON kaydet
    save_json(
        news,
        RAW_DATA_DIR / "news.json"
    )

    # Raporlar
    print("\nTop Companies")
    for company, count in report.top_companies(all_companies):
        print(f"{company}: {count}")

    report.save_csv(all_companies)
    report.save_json(all_companies)
    report.save_chart(all_companies)

    print("\nReports created.")

    database.close()

    print("Saved to:", RAW_DATA_DIR / "news.json")


if __name__ == "__main__":
    main()
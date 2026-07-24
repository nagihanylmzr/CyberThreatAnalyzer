from crawler import NewsCrawler
from config import RAW_DATA_DIR
from utils import save_json
from report import ReportGenerator
from database import DatabaseManager
from extractor import CompanyExtractor
from classifier import EntityClassifier
from scorer import ThreatScorer
from cve_extractor import CVEExtractor


def main():
    crawler = NewsCrawler()
    extractor = CompanyExtractor()
    classifier = EntityClassifier()
    database = DatabaseManager()
    report = ReportGenerator()
    scorer = ThreatScorer()
    cve_extractor = CVEExtractor()

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

        # Risk Score
        risk_score = scorer.score(content)

        # CVE'leri çıkar
        cves = cve_extractor.extract(content)

        # Entity çıkar
        entities = extractor.extract_entities(content)

        # Şirketleri filtrele
        companies = []

        for entity in entities:
            if classifier.classify(entity) == "Company":
                companies.append(entity)

        all_companies.extend(companies)

        # JSON
        article["content"] = content
        article["entities"] = entities
        article["companies"] = companies
        article["risk_score"] = risk_score
        article["cves"] = cves

        # Veritabanı
        article_id = database.insert_article(
            title,
            article["url"],
            article["source"],
            content,
            risk_score
        )

        for company in companies:
            database.insert_company(article_id, company)

        for cve in cves:
            database.insert_cve(article_id, cve)

        # Terminal
        print(title)
        print(f"Risk Score: {risk_score}")
        print("Companies:", companies)
        print("CVEs:", cves)
        print("-" * 50)

    # JSON kaydet
    save_json(news, RAW_DATA_DIR / "news.json")

    # Raporlar
    print("\n========== TOP COMPANIES ==========")

    for company, count in report.top_companies(all_companies):
        print(f"{company}: {count}")

    print("\n========== TOP CVEs ==========")

    for cve, count in report.top_cves():
        print(f"{cve}: {count}")

    print("\n========== TOP RISK NEWS ==========")

    for title, score in report.top_risk_news():
        print(f"{score:2} | {title}")

    report.save_csv(all_companies)
    report.save_json(all_companies)
    report.save_chart(all_companies)
    report.save_risk_csv()
    report.save_cve_csv()

    print("\nReports created.")
    print("Saved to:", RAW_DATA_DIR / "news.json")

    database.close()


if __name__ == "__main__":
    main()
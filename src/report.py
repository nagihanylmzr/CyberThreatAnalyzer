import csv
import json
from pathlib import Path
from collections import Counter

import matplotlib.pyplot as plt

from src.database import DatabaseManager


class ReportGenerator:

    def __init__(self):

        self.database = DatabaseManager()

        self.output_dir = Path("outputs")
        self.csv_dir = self.output_dir / "csv"
        self.json_dir = self.output_dir / "json"
        self.chart_dir = self.output_dir / "charts"

        self.csv_dir.mkdir(parents=True, exist_ok=True)
        self.json_dir.mkdir(parents=True, exist_ok=True)
        self.chart_dir.mkdir(parents=True, exist_ok=True)

    # ==================================================
    # Dashboard Reports
    # ==================================================

    def top_companies(self, limit=10):

        return self.database.get_company_statistics()[:limit]

    def top_cves(self, limit=10):

        return self.database.get_cve_statistics()[:limit]

    def top_risk_news(self, limit=10):

        return self.database.get_top_risk_news(limit)

    def articles(self):

        return self.database.get_articles_summary()
    # ==================================================
    # Export Reports
    # ==================================================

    def export_companies_csv(self):

        results = self.top_companies()

        with open(
            self.csv_dir / "top_companies.csv",
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow(["Company", "Mentions"])

            writer.writerows(results)

    def export_cves_csv(self):

        results = self.top_cves()

        with open(
            self.csv_dir / "top_cves.csv",
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow(["CVE", "Mentions"])

            writer.writerows(results)

    def export_risk_csv(self):

        results = self.top_risk_news()

        with open(
            self.csv_dir / "top_risk_news.csv",
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow(["Risk Score", "Title"])

            for title, score in results:
                writer.writerow([score, title])

    def export_json(self):

        data = {
            "top_companies": self.top_companies(),
            "top_cves": self.top_cves(),
            "top_risk_news": self.top_risk_news()
        }

        with open(
            self.json_dir / "report.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(data, file, indent=4)

    def export_company_chart(self):

        results = self.top_companies()

        if not results:
            return

        companies = [company for company, _ in results]
        counts = [count for _, count in results]

        plt.figure(figsize=(10, 6))

        plt.bar(companies, counts)

        plt.title("Top Mentioned Companies")
        plt.xlabel("Company")
        plt.ylabel("Mentions")

        plt.xticks(rotation=45, ha="right")

        plt.tight_layout()

        plt.savefig(self.chart_dir / "top_companies.png")

        plt.close()

    def close(self):

        self.database.close()
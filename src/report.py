import json
import csv
import matplotlib.pyplot as plt
from pathlib import Path
from collections import Counter


class ReportGenerator:
    def save_chart(self, companies):

        results = self.top_companies(companies)[:10]

        names = [company for company, _ in results]
        counts = [count for _, count in results]

        plt.figure(figsize=(10, 6))
        plt.bar(names, counts)

        plt.title("Top Companies")
        plt.xlabel("Company")
        plt.ylabel("Mentions")

        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        plt.savefig("../outputs/charts/top_companies.png")
        plt.close()
    def __init__(self):
        self.csv_dir = Path("../outputs/csv")
        self.json_dir = Path("../outputs/json")

        self.csv_dir.mkdir(parents=True, exist_ok=True)
        self.json_dir.mkdir(parents=True, exist_ok=True)

    def top_companies(self, companies):
        counter = Counter(companies)
        return counter.most_common()

    def save_csv(self, companies):
        results = self.top_companies(companies)

        with open(
                self.csv_dir / "top_companies.csv",
                "w",
                newline="",
                encoding="utf-8"
        ) as file:

            writer = csv.writer(file)
            writer.writerow(["Company", "Count"])

            for company, count in results:
                writer.writerow([company, count])

    def save_json(self, companies):
        results = self.top_companies(companies)

        data = []

        for company, count in results:
            data.append({
                "company": company,
                "count": count
            })

        with open(
                self.json_dir / "report.json",
                "w",
                encoding="utf-8"
        ) as file:
            json.dump(data, file, indent=4)
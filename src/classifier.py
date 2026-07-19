from pathlib import Path


class EntityClassifier:

    def __init__(self):

        company_file = Path("../data/reference/companies.txt")

        with open(company_file, "r", encoding="utf-8") as file:
            self.company_keywords = {
                line.strip()
                for line in file
                if line.strip()
            }

    def classify(self, entity):

        if entity in self.company_keywords:
            return "Company"

        return "Other"
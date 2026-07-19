import spacy


class CompanyExtractor:

    IGNORE = {
        "CISA",
        "Microsoft 365",
        "KEV",
        "TLS",
        "AI",
        "WordPress",
        "OpenSSL",
        "Kubernetes",
        "Google AI",
    }

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def extract_entities(self, text):
        doc = self.nlp(text)

        companies = []

        for ent in doc.ents:

            if ent.label_ != "ORG":
                continue

            company = ent.text.strip()

            if len(company) < 3:
                continue

            if company in self.IGNORE:
                continue

            companies.append(company)

        return sorted(set(companies))
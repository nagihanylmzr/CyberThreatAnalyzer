class ThreatScorer:

    def __init__(self):
        self.weights = {
            "ransomware": 5,
            "zero-day": 5,
            "0-day": 5,
            "exploit": 4,
            "rce": 4,
            "malware": 3,
            "botnet": 3,
            "backdoor": 3,
            "phishing": 2,
            "vulnerability": 2,
            "cve": 2,
            "breach": 2,
            "stealer": 2
        }

    def score(self, text):

        text = text.lower()

        score = 0

        for keyword, weight in self.weights.items():
            if keyword in text:
                score += weight

        return score
import re


class CVEExtractor:

    def __init__(self):
        self.pattern = r"CVE-\d{4}-\d{4,7}"

    def extract(self, text):

        if not text:
            return []

        return list(set(re.findall(self.pattern, text)))
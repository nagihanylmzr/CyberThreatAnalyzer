import sqlite3
import os

class DatabaseManager:

    def __init__(self, db_name=None):

        if db_name is None:
            db_name = os.path.join(
                os.path.dirname(__file__),
                "cyber_threats.db"
            )

        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        # Articles
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                url TEXT UNIQUE,
                source TEXT,
                content TEXT,
                risk_score INTEGER
            )
        """)

        # Companies
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                article_id INTEGER,
                company_name TEXT,
                UNIQUE(article_id, company_name),
                FOREIGN KEY(article_id) REFERENCES articles(id)
            )
        """)

        # CVEs
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cves (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                article_id INTEGER,
                cve_id TEXT,
                UNIQUE(article_id, cve_id),
                FOREIGN KEY(article_id) REFERENCES articles(id)
            )
        """)

        self.connection.commit()

    def insert_article(self, title, url, source, content, risk_score):

        self.cursor.execute("""
            INSERT OR IGNORE INTO articles
            (title, url, source, content, risk_score)
            VALUES (?, ?, ?, ?, ?)
        """, (title, url, source, content, risk_score))

        self.connection.commit()

        self.cursor.execute(
            "SELECT id FROM articles WHERE url = ?",
            (url,)
        )

        return self.cursor.fetchone()[0]

    def insert_company(self, article_id, company_name):

        self.cursor.execute("""
            INSERT OR IGNORE INTO companies
            (article_id, company_name)
            VALUES (?, ?)
        """, (article_id, company_name))

        self.connection.commit()

    def insert_cve(self, article_id, cve_id):

        self.cursor.execute("""
            INSERT OR IGNORE INTO cves
            (article_id, cve_id)
            VALUES (?, ?)
        """, (article_id, cve_id))

        self.connection.commit()

    def get_articles(self):

        self.cursor.execute("""
            SELECT *
            FROM articles
        """)

        return self.cursor.fetchall()

    def get_companies(self):

        self.cursor.execute("""
            SELECT company_name
            FROM companies
        """)

        return [row[0] for row in self.cursor.fetchall()]

    def get_company_statistics(self):
        self.cursor.execute("""
            SELECT company_name, COUNT(*) as total
            FROM companies
            GROUP BY company_name
            ORDER BY total DESC
        """)

        return self.cursor.fetchall()

    def get_cve_statistics(self):
        self.cursor.execute("""
            SELECT cve_id, COUNT(*) as total
            FROM cves
            GROUP BY cve_id
            ORDER BY total DESC
        """)

        return self.cursor.fetchall()
    def get_cves(self):

        self.cursor.execute("""
            SELECT cve_id
            FROM cves
        """)

        return [row[0] for row in self.cursor.fetchall()]

    def get_top_risk_news(self, limit=10):

        self.cursor.execute("""
            SELECT title, risk_score
            FROM articles
            ORDER BY risk_score DESC
            LIMIT ?
        """, (limit,))

        return self.cursor.fetchall()

    def get_articles_summary(self):
        self.cursor.execute("""
            SELECT title, source, risk_score
            FROM articles
            ORDER BY risk_score DESC
        """)

        return self.cursor.fetchall()
    def close(self):
        self.connection.close()
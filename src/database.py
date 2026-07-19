import sqlite3
import os
import sqlite3

class DatabaseManager:
    import os

    def __init__(self, db_name="cyber_threats.db"):
        print("Database:", os.path.abspath(db_name))
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def create_tables(self):

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

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                article_id INTEGER,
                company_name TEXT,
                UNIQUE(article_id, company_name),
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

    def get_articles(self):

        self.cursor.execute("""
            SELECT *
            FROM articles
        """)

        return self.cursor.fetchall()

    def get_companies(self):

        self.cursor.execute("""
            SELECT article_id, company_name
            FROM companies
        """)

        return self.cursor.fetchall()

    def close(self):
        self.connection.close()
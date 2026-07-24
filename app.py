from flask import Flask, render_template

from src.database import DatabaseManager
from src.report import ReportGenerator

app = Flask(__name__)


@app.route("/")
def dashboard():

    database = DatabaseManager()
    report = ReportGenerator()

    article_count = len(database.get_articles())
    company_count = len(database.get_companies())
    cve_count = len(database.get_cves())

    top_companies = report.top_companies()
    top_cves = report.top_cves()
    top_risk = report.top_risk_news()

    database.close()
    report.close()
    return render_template(
        "dashboard.html",
        article_count=article_count,
        company_count=company_count,
        cve_count=cve_count,
        top_companies=top_companies,
        top_cves=top_cves,
        top_risk=top_risk
    )


@app.route("/companies")
def companies():

    report = ReportGenerator()

    companies = report.top_companies(limit=100)

    report.close()

    return render_template(
        "companies.html",
        companies=companies
    )

@app.route("/cves")
def cves():

    report = ReportGenerator()

    cves = report.top_cves(limit=100)

    report.close()

    return render_template(
        "cves.html",
        cves=cves
    )
@app.route("/articles")
def articles():

    report = ReportGenerator()

    articles = report.articles()

    report.close()

    return render_template(
        "articles.html",
        articles=articles
    )
if __name__ == "__main__":
    app.run(debug=True)
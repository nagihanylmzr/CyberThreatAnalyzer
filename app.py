from datetime import datetime
from flask import Flask, render_template, request, send_file

from src.database import DatabaseManager
from src.report import ReportGenerator

app = Flask(__name__)


# ==========================
# Dashboard
# ==========================

@app.route("/")
def dashboard():

    database = DatabaseManager()
    report = ReportGenerator()

    # Statistics
    article_count = len(database.get_articles())
    company_count = len(database.get_companies())
    cve_count = len(database.get_cves())

    # Top Companies
    top_companies = report.top_companies()
    company_labels = [company for company, count in top_companies]
    company_counts = [count for company, count in top_companies]

    # Top CVEs
    top_cves = report.top_cves()
    cve_labels = [cve for cve, count in top_cves]
    cve_counts = [count for cve, count in top_cves]

    # Highest Risk News
    top_risk = report.top_risk_news()
    risk_scores = [score for _, score in top_risk]

    # Average Risk
    average_risk = round(sum(risk_scores) / len(risk_scores), 1) if risk_scores else 0

    # Quick Insights
    top_company = top_companies[0] if top_companies else ("-", 0)
    top_cve = top_cves[0] if top_cves else ("-", 0)
    highest_risk = max(risk_scores, default=0)

    database.close()
    report.close()

    return render_template(
        "dashboard.html",
        article_count=article_count,
        company_count=company_count,
        cve_count=cve_count,
        top_companies=top_companies,
        top_cves=top_cves,
        top_risk=top_risk,
        company_labels=company_labels,
        company_counts=company_counts,
        cve_labels=cve_labels,
        cve_counts=cve_counts,
        average_risk=average_risk,
        top_company=top_company,
        top_cve=top_cve,
        highest_risk=highest_risk,
        current_date=datetime.now().strftime("%d %b %Y"),
        active_page="dashboard"
    )


# ==========================
# Companies
# ==========================

@app.route("/companies")
def companies():

    report = ReportGenerator()

    companies = report.top_companies(limit=100)

    report.close()

    return render_template(
        "companies.html",
        companies=companies,
        active_page="companies"
    )


# ==========================
# CVEs
# ==========================

@app.route("/cves")
def cves():

    report = ReportGenerator()

    cves = report.top_cves(limit=100)

    report.close()

    return render_template(
        "cves.html",
        cves=cves,
        active_page="cves"
    )


# ==========================
# Articles
# ==========================

@app.route("/articles")
def articles():

    report = ReportGenerator()

    search = request.args.get("search", "").strip()
    risk = request.args.get("risk", "all")

    articles = report.articles(search, risk)

    report.close()

    return render_template(
        "articles.html",
        articles=articles,
        search=search,
        risk=risk,
        active_page="articles"
    )


# ==========================
# Admin Panel
# ==========================

@app.route("/admin")
def admin():

    database = DatabaseManager()
    report = ReportGenerator()

    article_count = len(database.get_articles())
    company_count = len(database.get_companies())
    cve_count = len(database.get_cves())

    risk_scores = [score for _, score in report.top_risk_news()]
    average_risk = round(sum(risk_scores) / len(risk_scores), 1) if risk_scores else 0

    database.close()
    report.close()

    return render_template(
        "admin.html",
        article_count=article_count,
        company_count=company_count,
        cve_count=cve_count,
        average_risk=average_risk,
        current_date=datetime.now().strftime("%d %b %Y"),
        active_page="admin"
    )


# ==========================
# Export
# ==========================

@app.route("/export/<file_type>")
def export(file_type):

    report = ReportGenerator()

    if file_type == "companies":
        filename = report.export_companies_csv()

    elif file_type == "cves":
        filename = report.export_cves_csv()

    elif file_type == "risk":
        filename = report.export_risk_csv()

    elif file_type == "json":
        filename = report.export_json()

    else:
        report.close()
        return "Invalid export type", 404

    report.close()

    return send_file(filename, as_attachment=True)


# ==========================
# Run App
# ==========================

if __name__ == "__main__":
    app.run(debug=True)
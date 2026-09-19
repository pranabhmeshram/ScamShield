from flask import Flask, render_template, request, jsonify

from detector.url_analyzer import analyze_url
from detector.domain_info import get_domain_info

from database.database import (
    create_database,
    save_scan,
    get_scan_history
)

app = Flask(__name__)

# Create database
create_database()


# =========================
# HOME
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# URL SCANNER
# =========================

@app.route("/scan", methods=["POST"])
def scan():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Invalid request"
        }), 400

    url = data.get("url", "").strip()

    if not url:
        return jsonify({
            "error": "Please enter a URL"
        }), 400

    # Analyze URL
    result = analyze_url(url)

    # Get domain information
    domain_data = get_domain_info(url)

    # Add domain information to result
    result["domain_info"] = domain_data

    # Save scan in database
    save_scan(
        result["url"],
        result["score"],
        result["status"],
        result["reasons"]
    )

    return jsonify(result)


# =========================
# SCAN HISTORY
# =========================

@app.route("/history")
def history():

    records = get_scan_history()

    return render_template(
        "history.html",
        records=records
    )


# =========================
# DASHBOARD
# =========================

@app.route("/dashboard")
def dashboard():

    records = get_scan_history()

    total = len(records)

    low = 0
    medium = 0
    high = 0

    for record in records:

        status = record[3]

        if status == "Low Risk":
            low += 1

        elif status == "Medium Risk":
            medium += 1

        elif status == "High Risk":
            high += 1

    return render_template(
        "dashboard.html",
        total=total,
        low=low,
        medium=medium,
        high=high
    )


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":
    app.run(debug=True)
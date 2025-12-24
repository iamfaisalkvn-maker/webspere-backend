from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

PAGESPEED_API_KEY = os.environ.get("PAGESPEED_API_KEY")

PAGESPEED_URL = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"


def fetch_pagespeed(url):
    params = {
        "url": url,
        "strategy": "mobile",
        "key": PAGESPEED_API_KEY
    }
    response = requests.get(PAGESPEED_URL, params=params, timeout=30)
    return response.json()


def extract_scores(data):
    categories = data.get("lighthouseResult", {}).get("categories", {})

    def score(name):
        return round(categories.get(name, {}).get("score", 0) * 100)

    return {
        "performance": score("performance"),
        "seo": score("seo"),
        "accessibility": score("accessibility"),
        "best_practices": score("best-practices")
    }


@app.route("/")
def home():
    return "Webspere SEO API is running 🚀"


# 🟢 FREE AUDIT (ONLY PERFORMANCE)
@app.route("/analyze-free")
def analyze_free():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL required"}), 400

    data = fetch_pagespeed(url)
    scores = extract_scores(data)

    return jsonify({
        "url": url,
        "performance": scores["performance"]
    })


# 🔵 PAID AUDIT (FULL DATA)
@app.route("/analyze-paid")
def analyze_paid():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL required"}), 400

    data = fetch_pagespeed(url)
    scores = extract_scores(data)

    return jsonify({
        "url": url,
        "performance": scores["performance"],
        "seo": scores["seo"],
        "accessibility": scores["accessibility"],
        "best_practices": scores["best_practices"]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

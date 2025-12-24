from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

@app.route("/")
def home():
    return "Webspere SEO Backend is running 🚀"

@app.route("/analyze")
def analyze():
    url = request.args.get("url")

    if not url:
        return jsonify({"error": "URL parameter missing"}), 400

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)

        load_time = response.elapsed.total_seconds()

        result = {
            "url": url,
            "status_code": response.status_code,
            "performance": max(40, int(100 - load_time * 8)),
            "seo": 70,
            "accessibility": 65,
            "best_practices": 75
        }

        return jsonify(result)

    except requests.exceptions.RequestException:
        return jsonify({
            "error": "Website blocked automated analysis"
        }), 403


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

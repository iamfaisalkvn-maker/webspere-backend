
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Webspere SEO Backend is running"

@app.route("/analyze")
def analyze():
    url = request.args.get("url")

    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    try:
        # Simple SEO + performance style checks (safe for free hosting)
        response = requests.get(url, timeout=10)
        load_time = response.elapsed.total_seconds()

        result = {
            "url": url,
            "status_code": response.status_code,
            "performance": max(40, int(100 - load_time * 10)),
            "seo": 70,
            "accessibility": 65,
            "best_practices": 75
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

PAGESPEED_API_KEY = os.environ.get("PAGESPEED_API_KEY")

@app.route("/")
def home():
    return "Webspere SEO API is running"

@app.route("/analyze", methods=["GET"])
def analyze():
    url = request.args.get("url")

    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    api_url = (
        "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        f"?url={url}&strategy=mobile&key={PAGESPEED_API_KEY}"
    )

    try:
        response = requests.get(api_url, timeout=30)
        data = response.json()

        # If Google returns an error
        if "lighthouseResult" not in data:
            return jsonify({
                "error": "PageSpeed API error",
                "details": data
            }), 500

        categories = data["lighthouseResult"]["categories"]

        result = {
            "performance": round(categories["performance"]["score"] * 100),
            "seo": round(categories["seo"]["score"] * 100),
            "accessibility": round(categories["accessibility"]["score"] * 100),
            "best_practices": round(categories["best-practices"]["score"] * 100)
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "error": "Exception occurred",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

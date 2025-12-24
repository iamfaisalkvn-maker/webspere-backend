from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Read API key from Render Environment Variables
PAGESPEED_API_KEY = os.environ.get("PAGESPEED_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "Webspere SEO API is running 🚀"

@app.route("/analyze", methods=["GET"])
def analyze():
    url = request.args.get("url")

    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    if not PAGESPEED_API_KEY:
        return jsonify({"error": "PageSpeed API key not configured"}), 500

    api_url = (
        "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        f"?url={url}&strategy=mobile&key={PAGESPEED_API_KEY}"
    )

    try:
        response = requests.get(api_url, timeout=30)
        data = response.json()

        if "lighthouseResult" not in data:
            return jsonify({"error": "Invalid PageSpeed response"}), 500

        categories = data["lighthouseResult"]["categories"]

        def get_score(category):
            """
            Safely extract score.
            Returns 0 if category is missing.
            """
            return round(categories.get(category, {}).get("score", 0) * 100)

        result = {
            "url": url,
            "performance": get_score("performance"),
            "seo": get_score("seo"),
            "accessibility": get_score("accessibility"),
            "best_practices": get_score("best-practices")
        }

        return jsonify(result)

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Request failed",
            "details": str(e)
        }), 500

    except Exception as e:
        return jsonify({
            "error": "Exception occurred",
            "details": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

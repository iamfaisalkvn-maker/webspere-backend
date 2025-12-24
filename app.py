from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

PAGESPEED_API_KEY = os.environ.get("PAGESPEED_API_KEY")

@app.route("/analyze", methods=["GET"])
def analyze():
    url = request.args.get("url")

    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    api_url = (
        "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        f"?url={url}&strategy=mobile&key={PAGESPEED_API_KEY}"
    )

    response = requests.get(api_url)
    data = response.json()

    try:
        lighthouse = data["lighthouseResult"]["categories"]

        result = {
            "performance": lighthouse["performance"]["score"] * 100,
            "seo": lighthouse["seo"]["score"] * 100,
            "accessibility": lighthouse["accessibility"]["score"] * 100,
            "best_practices": lighthouse["best-practices"]["score"] * 100
        }

        return jsonify(result)

    except:
        return jsonify({"error": "Unable to analyze site"}), 500


@app.route("/")
def home():
    return "Webspere SEO API is running"


if __name__ == "__main__":
    app.run()

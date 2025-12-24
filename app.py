from flask import Flask, request, jsonify
import requests
import os
import hmac
import hashlib

app = Flask(__name__)

# ENV VARIABLES
PAGESPEED_API_KEY = os.environ.get("PAGESPEED_API_KEY")
RAZORPAY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET")

PAGESPEED_URL = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

# TEMP STORAGE (for demo – later DB)
VALID_PAYMENTS = set()


def fetch_pagespeed(url):
    params = {
        "url": url,
        "strategy": "mobile",
        "key": PAGESPEED_API_KEY
    }
    return requests.get(PAGESPEED_URL, params=params, timeout=30).json()


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


# 🟢 FREE AUDIT
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


# 🔔 RAZORPAY WEBHOOK
@app.route("/razorpay-webhook", methods=["POST"])
def razorpay_webhook():
    payload = request.data
    signature = request.headers.get("X-Razorpay-Signature")

    expected_signature = hmac.new(
        bytes(RAZORPAY_SECRET, "utf-8"),
        payload,
        hashlib.sha256
    ).hexdigest()

    if expected_signature != signature:
        return jsonify({"error": "Invalid signature"}), 400

    data = request.json
    payment_id = data.get("payload", {}).get("payment", {}).get("entity", {}).get("id")

    if payment_id:
        VALID_PAYMENTS.add(payment_id)

    return jsonify({"status": "payment verified"})


# 🔵 PAID AUDIT (SECURED)
@app.route("/analyze-paid")
def analyze_paid():
    url = request.args.get("url")
    payment_id = request.args.get("payment_id")

    if not url or not payment_id:
        return jsonify({"error": "URL and payment_id required"}), 400

    if payment_id not in VALID_PAYMENTS:
        return jsonify({"error": "Payment not verified"}), 403

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

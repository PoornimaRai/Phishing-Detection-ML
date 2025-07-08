from flask import Flask, request, render_template
from urllib.parse import urlparse
import pandas as pd
import joblib

app = Flask(__name__)

# Load model
model = joblib.load("decision_tree_model.pkl")

# Extract features from URL
def extract_features(url):
    parsed = urlparse(url)
    return {
        "length_url": len(url),
        "nb_dots": url.count('.'),
        "nb_subdomains": len(parsed.netloc.split('.')) - 2 if len(parsed.netloc.split('.')) > 2 else 0,
        "has_https": 1 if parsed.scheme == "https" else 0
    }

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    url = ""
    if request.method == "POST":
        url = request.form["url"]
        features = pd.DataFrame([extract_features(url)])
        pred = model.predict(features)[0]
        prediction = "Phishing" if pred == 1 else "Legitimate"
    return render_template("index.html", prediction=prediction, url=url)

if __name__ == "__main__":
    app.run(debug=True)


from flask import Flask, render_template, request
import requests
import matplotlib.pyplot as plt

app = Flask(__name__)

API_KEY = "40bac1a497f12efc8f8f5823fb885f05b19d4237de241e4a92706c08a4b98ef90e949a12eef215c3"

def check_ip(ip):
    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {
        "Key": API_KEY,
        "Accept": "application/json"
    }
    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    return data["data"]

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        ip = request.form["ip"]
        result = check_ip(ip)

        # Simple chart
        score = result["abuseConfidenceScore"]
        plt.bar(["Safe", "Threat"], [100-score, score])
        plt.savefig("static/chart.png")
        plt.close()

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)

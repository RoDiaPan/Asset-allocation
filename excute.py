from flask import Flask, send_from_directory, jsonify
import urllib.request
import json

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory(".", "asset_dashboard.html")

@app.route("/api/exchange-rate")
def exchange_rate():
    try:
        url = "https://api.exchangerate-api.com/v4/latest/TWD"
        with urllib.request.urlopen(url, timeout=5) as res:
            data = json.loads(res.read().decode())
        usd_per_twd = data["rates"]["USD"]
        twd_per_usd = round(1 / usd_per_twd, 2)
        return jsonify({ "rate": twd_per_usd, "date": data.get("date", "") })
    except Exception as e:
        return jsonify({ "error": str(e) }), 500

if __name__ == "__main__":
    app.run(debug=True, port=8080)
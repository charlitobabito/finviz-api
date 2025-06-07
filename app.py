from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import requests
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/ratings")
def get_ratings():
    symbol = request.args.get("symbol", "").upper()
    url = f"https://finviz.com/quote.ashx?t={symbol}"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, "html.parser")
    rows = soup.select("tr.styled-row")
    data = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 5:
            data.append({
                "date": cols[0].text.strip(),
                "action": cols[1].text.strip(),
                "analyst": cols[2].text.strip(),
                "rating": cols[3].text.strip(),
                "target": cols[4].text.strip()
            })

    return jsonify(data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

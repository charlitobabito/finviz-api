from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return 'API Finviz Analyst Ratings is live!'

@app.route('/ratings')
def get_ratings():
    symbol = request.args.get('symbol', '').upper()
    if not symbol:
        return jsonify({"error": "Missing symbol parameter"}), 400

    url = f'https://finviz.com/quote.ashx?t={symbol}'
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        table = soup.find('table', class_='fullview-ratings-outer')
        if not table:
            return jsonify([])

        rows = table.find_all('tr')[1:]  # Skip header
        data = []

        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 4:
                continue

            date = cols[0].get_text(strip=True)
            action = cols[1].get_text(strip=True)
            analyst = cols[2].get_text(strip=True)
            rating = cols[3].get_text(strip=True)
            target = cols[4].get_text(strip=True) if len(cols) > 4 else ""

            data.append({
                "date": date,
                "action": action,
                "analyst": analyst,
                "rating": rating,
                "target": target
            })

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

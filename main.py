import os
import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

SMMRAJA_API_URL = "https://smmraja.com/api/v2"
SMMRAJA_API_KEY = "7*B5@jWQ@0LHJ8AEH*x@"
USD_TO_INR = 85.0
PROFIT_MARGIN_PER_1K = 2.0  # ₹2 extra profit per 1000

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/services')
def get_services():
    try:
        payload = {
            "key": SMMRAJA_API_KEY,
            "action": "services"
        }
        res = requests.post(SMMRAJA_API_URL, data=payload, timeout=15).json()
        
        if not isinstance(res, list):
            return jsonify([])

        formatted_services = []
        for item in res:
            rate_usd = float(item.get('rate', 0))
            rate_inr = (rate_usd * USD_TO_INR) + PROFIT_MARGIN_PER_1K
            
            formatted_services.append({
                "service": item.get('service'),
                "name": item.get('name'),
                "category": item.get('category'),
                "selling_rate_inr": round(rate_inr, 2),
                "min": item.get('min'),
                "max": item.get('max')
            })
            
        return jsonify(formatted_services)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
  

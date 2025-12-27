from flask import request,Blueprint,jsonify
from service.fiis_web_scraping import get_fii
tickers = Blueprint("tickers", __name__)

@tickers.route("/<ticker>", methods=["GET"])
def get_tickers(ticker):
    if not ticker:
        return jsonify({"error": "Ticker não informado"}), 400
    get_fii_data = get_fii(ticker)
    try:
        if not get_fii_data:
            return jsonify({"error": "Ticker não encontrado"}), 404
        else:
            return jsonify(get_fii_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

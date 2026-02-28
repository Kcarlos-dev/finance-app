from flask import request,Blueprint,jsonify
from service.fiis_web_scraping import get_fii
from service.paper_web_scraping import get_paper,get_paper_dividends
from routes.middleware.auth import token_required
from service.google_gemini import analyze_investment_with_gemini
tickers = Blueprint("tickers", __name__)

@tickers.route("yields/<ticker>", methods=["GET"])
@token_required("admin","user")
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

@tickers.route("papers/<ticker>", methods=["GET"])
@token_required("admin","user")
def get_papers(ticker):
    if not ticker:
        return jsonify({"error": "Ticker não informado"}), 400
    get_paper_data = get_paper(ticker)
    try:
        if not get_paper_data:
            return jsonify({"error": "Ticker não encontrado"}), 404
        else:
            return jsonify(get_paper_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@tickers.route("dividends/<ticker>", methods=["GET"])
@token_required("admin","user")
def get_dividends(ticker):
    if not ticker:
        return jsonify({"error": "Ticker não informado"}), 400
    get_dividends_data = get_paper_dividends(ticker)
    try:
        if not get_dividends_data:
            return jsonify({"error": "Ticker não encontrado"}), 404
        else:
            return jsonify(get_dividends_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tickers.route("analyze/", methods=["POST"])
@token_required("admin","user")
def analyze_investment():
    data = request.get_json()
    if not data.get("data"):
        return jsonify({"error": "Dados não informados"}), 400
    return jsonify(analyze_investment_with_gemini(data.get("data")))
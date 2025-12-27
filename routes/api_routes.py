from flask import request,Blueprint,jsonify

tickers = Blueprint("tickers", __name__)

@tickers.route("/", methods=["GET"])
def get_tickers():
    return jsonify({"message": "Hello, World!"})
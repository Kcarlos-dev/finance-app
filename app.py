import logger_setup
from routes.api_routes import tickers
from flask import Flask

app = Flask(__name__)

app.register_blueprint(tickers, url_prefix="/tickers")

if __name__ == "__main__":
    app.run(debug=True)

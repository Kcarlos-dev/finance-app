import logger_setup
from routes.api_routes import tickers
from routes.user_routes import users
from flask import Flask
from flask_cors import CORS
from service.util.config import get_config
app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": get_config("CORS_ORIGINS")}}, supports_credentials=True)

app.register_blueprint(tickers, url_prefix="/tickers")
app.register_blueprint(users, url_prefix="/users")

if __name__ == "__main__":
    app.run(debug=True)

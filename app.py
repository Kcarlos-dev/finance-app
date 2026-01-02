import logger_setup
from routes.api_routes import tickers
from routes.user_routes import users
from flask import Flask

#Imagine que vc é um consultor de investimentos e teria que avaliar se vale apena investir nessa ação com base nesse dados, lembres-se ela é apenas figurativa, seja breve e com comentários, certeiros :
app = Flask(__name__)

app.register_blueprint(tickers, url_prefix="/tickers")
app.register_blueprint(users, url_prefix="/users")

if __name__ == "__main__":
    app.run(debug=True)

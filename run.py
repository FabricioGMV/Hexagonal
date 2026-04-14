from flask import Flask
from src.config.data_base import init_db
from src.routes import init_routes
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    """
    Função que cria e configura a aplicação Flask.
    """
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    jwt = JWTManager(app)

    init_db(app)

    init_routes(app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

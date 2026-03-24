from src.Application.Controllers.user_controller import UserController
from flask import jsonify, make_response

def init_routes(app):    
    @app.route('/api', methods=['GET'])
    def health():
        return make_response(jsonify({
            "mensagem": "API - OK; Docker - Up",
        }), 200)
    
    #@app.route('/users', methods=['GET'])
    #def list_all_users():
        #return UserController.get_all_users()
    
    #@app.route('/user', methods=['POST'])
    #def register_user():
        #return UserController.register_user()

    @app.route('/listar', methods=['GET'])
    def list_all_users():
        return UserController.get_all_users()
    
    @app.route('/criar', methods=['POST'])
    def register_user():
        return UserController.register_user()
    
    @app.route('/ativar', methods=['POST'])
    def activate_user():
        return UserController.activate_account()

    @app.route('/login', methods=['POST'])
    def login_user():
        return UserController.login()
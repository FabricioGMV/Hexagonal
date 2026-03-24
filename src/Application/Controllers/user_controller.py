from flask import request, jsonify, make_response
from src.Application.Service.user_service import UserService
from flask_jwt_extended import create_access_token
from src.Infrastructure.Model.user import User
from sqlalchemy.exc import IntegrityError
from src.config.data_base import db

class UserController:
    # ======== MÉTODO PARA REGISTRAR USUÁRIO ========
    @staticmethod
    def register_user():
        data = request.get_json()
        name = data.get('name')
        cnpj = data.get('cnpj')
        email = data.get('email')
        celular = data.get('celular')
        password = data.get('password')

        # ======== Tratamento de Exceções ========
        if not name or not cnpj or not email or not celular or not password:
            return make_response(jsonify({"erro": "Parâmetro(s) obrigatório(s) não informado(s)"}), 400)

        try:
            user = UserService.create_user(name, cnpj, email, celular, password)
            
            return make_response(jsonify({
                "mensagem": "User salvo com sucesso",
                "usuarios": user.to_dict()
            }), 201) 
            
        except IntegrityError:
            db.session.rollback()
            return make_response(jsonify({
                "erro": "Conflito de dados: E-mail, CNPJ ou Celular já cadastrados no sistema."
            }), 409)
            
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({
                "erro": f"Erro interno do servidor: {str(e)}"
            }), 500)
    
    # ======== MÉTODO PARA ATIVAR USUÁRIO ========
    @staticmethod
    def activate_account():
        data = request.get_json()
        email = data.get('email')
        code = data.get('codigo_ativacao')

        if not email or not code:
            return make_response(jsonify({"erro": "Email e código são obrigatórios"}), 400)

        is_activated = UserService.verify_code(email, code)

        if is_activated:
            return make_response(jsonify({"mensagem": "Conta ativada com sucesso! Você já pode fazer login."}), 200)
        else:
            return make_response(jsonify({"erro": "Código inválido ou usuário não encontrado."}), 400)
            
        
    # ======== Autenticação via JWT ========
    @staticmethod
    def login():
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or user.password != password:
            return make_response(jsonify({"erro": "E-mail ou senha incorretos."}), 401)

        if user.status != "Ativo":
            return make_response(jsonify({"erro": "Conta inativa. Por favor, ative sua conta com o código enviado para o seu WhatsApp."}), 403)

        access_token = create_access_token(identity=user.id)
        
        return make_response(jsonify({
            "mensagem": "Login realizado com sucesso",
            "token": access_token
        }), 200)
    
    # ======== MÉTODO PARA LISTAR USUÁRIOS ========
    @staticmethod
    def get_all_users():
        try:
            usuarios = UserService.get_all()
            return make_response(jsonify({
                "mensagem": "Usuários listados com sucesso",
                "quantidade": len(usuarios),
                "usuarios": usuarios
            }), 200)
        except Exception as e:
            return make_response(jsonify({"erro": f"Erro ao buscar usuários: {str(e)}"}), 500)

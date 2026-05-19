from flask import request, jsonify, make_response
from flask_jwt_extended import get_jwt_identity
from src.Application.Service.product_service import ProductService

class ProductController:
    @staticmethod
    def criar_produto():
        seller_id = get_jwt_identity()
        data = request.get_json()

        try:
            # Validação básica
            if not data.get('nome') or not data.get('preco') or not data.get('estoque_quantidade') or not data.get('estoque_unidade_id'):
                return make_response(jsonify({"erro": "Campos obrigatórios faltando."}), 400)

            produto = ProductService.criar_produto(data, seller_id)
            return make_response(jsonify({
                "mensagem": "Produto cadastrado com sucesso!",
                "produto": produto.to_dict()
            }), 201)
        except Exception as e:
            return make_response(jsonify({"erro": f"Erro ao cadastrar produto: {str(e)}"}), 500)

    @staticmethod
    def listar_produtos():
        seller_id = get_jwt_identity()
        try:
            produtos = ProductService.listar_produtos_por_seller(seller_id)
            return make_response(jsonify([p.to_dict() for p in produtos]), 200)
        except Exception as e:
            return make_response(jsonify({"erro": f"Erro ao listar produtos: {str(e)}"}), 500)

    @staticmethod
    def inativar_produto(produto_id):
        seller_id = get_jwt_identity()
        try:
            sucesso = ProductService.inativar_produto(produto_id, seller_id)
            if sucesso:
                return make_response(jsonify({"mensagem": "Produto inativado com sucesso!"}), 200)
            return make_response(jsonify({"erro": "Produto não encontrado ou não pertence a você."}), 404)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)
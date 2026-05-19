from src.Application.Controllers.user_controller import UserController
from src.Application.Controllers.dashboard_controller import DashboardController
from src.Application.Controllers.product_controller import ProductController
from src.Application.Controllers.venda_controller import VendaController
from src.Application.Service.auth_decorator import seller_required
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required
from flask import render_template

def init_routes(app):
    # ======== ROTAS WEB (FRONT-END) ========

    @app.route('/')
    def index():
        return render_template('auth/login.html')

    @app.route('/cadastro')
    def page_cadastro():
        return render_template('auth/cadastro.html')
    
    @app.route('/dashboard')
    def page_dashboard():
        return render_template('dashboard/index.html')
    
    @app.route('/produtos')
    def page_produtos():
        return render_template('produtos/index.html')
    
    @app.route('/vendas')
    def page_vendas():
        return render_template('vendas/index.html')
    
    # ======== ROTAS DE API (BACK-END) ========

    @app.route('/listar', methods=['GET'])
    @seller_required()
    def list_all_users():
        return UserController.get_all_users()
    
    @app.route('/criar', methods=['POST'])
    def register_user():
        return UserController.register_user()
        
    @app.route('/ativar', methods=['POST'])
    def activate_account():
        return UserController.activate_account()

    @app.route('/login', methods=['POST'])
    def login_user():
        return UserController.login()
    
    @app.route('/redefinir')
    def page_redefinir():
        return render_template('auth/redefinir.html')
    
    @app.route('/atualizar/id=<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        #user_id = request.args.get('id') //Padrão de mercado (RESTful) para passar o ID do recurso na URL
        return UserController.update_user(user_id)
    
    @app.route('/api/redefinir/solicitar', methods=['POST'])
    def solicitar_redefinir_senha():
        return UserController.solicitar_redefinir_senha()

    @app.route('/api/redefinir/confirmar', methods=['POST'])
    def confirmar_redefinir_senha():
        return UserController.confirmar_redefinir_senha()
    
    @app.route('/api/dashboard', methods=['GET'])
    @seller_required() # Protege a rota: só usuários logados e ativos acessam
    def api_dashboard():
        return DashboardController.get_dashboard_data()
    
    @app.route('/api/produtos', methods=['GET'])
    @seller_required()
    def listar_produtos():
        return ProductController.listar_produtos()

    @app.route('/api/produtos', methods=['POST'])
    @seller_required()
    def criar_produto():
        return ProductController.criar_produto()

    @app.route('/api/produtos/<int:produto_id>/inativar', methods=['PUT'])
    @seller_required()
    def inativar_produto(produto_id):
        return ProductController.inativar_produto(produto_id)
    
    # Provavelmente você tem algo parecido com isso no seu arquivo de rotas:
    @app.route('/api/produtos/<int:produto_id>', methods=['PUT'])
    @jwt_required()
    def atualizar_produto(produto_id):
        return ProductController.atualizar_produto(produto_id)
    
    @app.route('/api/vendas', methods=['POST'])
    @seller_required()
    def realizar_venda():
        return VendaController.realizar_venda()
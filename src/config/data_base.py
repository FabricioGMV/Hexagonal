import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    # Garante a criação da pasta de banco de dados se não existir
    db_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../.db'))
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
        
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(db_dir, 'minimercado.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    # Criação das tabelas em tempo de execução
    with app.app_context():
        from src.Infrastructure.Model.user import User
        from src.Infrastructure.Model.unidades import Unidade
        from src.Infrastructure.Model.produtos import Produto
        from src.Infrastructure.Model.vendas import Venda
        from src.Infrastructure.Model.vendas_itens import VendaItem
        db.create_all()
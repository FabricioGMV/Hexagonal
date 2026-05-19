from src.config.data_base import db
import random

class Produto(db.Model):
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    estoque_quantidade = db.Column(db.Float, nullable=False)
    
    # Chaves Estrangeiras para Unidades
    estoque_unidade_id = db.Column(db.Integer, db.ForeignKey('unidades.id'), nullable=False)
    conteudo_quantidade = db.Column(db.Float, nullable=True) # Pode ser nulo se for vendido a granel/peso
    conteudo_unidade_id = db.Column(db.Integer, db.ForeignKey('unidades.id'), nullable=True)
    
    # RN4 - Status Inicial: Todo produto novo cadastrado deve vir automaticamente como Ativo (True)
    status = db.Column(db.Boolean, default=True, nullable=False) 
    
    imagem_path = db.Column(db.String(255), nullable=True)
    codigo_barras = db.Column(db.String(20), unique=True, nullable=False)
    
    # Relacionamento com o Vendedor (Um Seller gerencia só os seus)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, **kwargs):
        super(Produto, self).__init__(**kwargs)
        # Gera o código de barras automaticamente com prefixo 785
        if not self.codigo_barras:
            self.codigo_barras = f"785{random.randint(100000000, 999999999)}"

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "preco": self.preco,
            "estoque_quantidade": self.estoque_quantidade,
            "status": "Ativo" if self.status else "Inativo",
            "codigo_barras": self.codigo_barras,
            "seller_id": self.seller_id
        }
from src.config.data_base import db
from src.Infrastructure.Model.produtos import Produto

class ProductService:
    @staticmethod
    def criar_produto(dados, seller_id):
        # RN4: O Produto já nasce com default=True (Ativo) graças à modelagem
        novo_produto = Produto(
            nome=dados['nome'],
            preco=dados['preco'],
            estoque_quantidade=dados['estoque_quantidade'],
            estoque_unidade_id=dados['estoque_unidade_id'],
            conteudo_quantidade=dados.get('conteudo_quantidade'), # Opcional
            conteudo_unidade_id=dados.get('conteudo_unidade_id'), # Opcional
            seller_id=seller_id
        )
        db.session.add(novo_produto)
        db.session.commit()
        return novo_produto

    @staticmethod
    def listar_produtos_por_seller(seller_id):
        # Um Seller só enxerga seus próprios produtos
        return Produto.query.filter_by(seller_id=seller_id).order_by(Produto.nome.asc()).all()
        
    @staticmethod
    def inativar_produto(produto_id, seller_id):
        produto = Produto.query.filter_by(id=produto_id, seller_id=seller_id).first()
        if produto:
            produto.status = False
            db.session.commit()
            return True
        return False
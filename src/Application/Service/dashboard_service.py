from src.Infrastructure.Model.produtos import Produto
from src.Infrastructure.Model.vendas import Venda
from src.Infrastructure.Model.vendas_itens import VendaItem
from src.config.data_base import db

class DashboardService:
    @staticmethod
    def obter_indicadores(seller_id):
        # 1. Total de produtos ativos e valor total do estoque
        produtos = Produto.query.filter_by(seller_id=seller_id, status=True).all()
        total_produtos = len(produtos)
        valor_estoque = sum(p.preco * p.estoque_quantidade for p in produtos)

        # 2. Total de vendas em R$
        vendas = Venda.query.filter_by(seller_id=seller_id).all()
        total_vendas_rs = sum(v.valor_total for v in vendas)

        # 3. Total de itens vendidos
        venda_ids = [v.id for v in vendas]
        if venda_ids:
            itens_vendidos = VendaItem.query.filter(VendaItem.venda_id.in_(venda_ids)).all()
            total_itens_vendidos = sum(item.quantidade for item in itens_vendidos)
        else:
            total_itens_vendidos = 0

        # 4. Últimas 5 vendas realizadas
        ultimas_vendas = Venda.query.filter_by(seller_id=seller_id).order_by(Venda.data_venda.desc()).limit(5).all()
        lista_ultimas_vendas = []
        
        for v in ultimas_vendas:
            # Pega o nome do primeiro produto para resumir na tabela, ou mostra "Múltiplos itens"
            itens = VendaItem.query.filter_by(venda_id=v.id).all()
            if len(itens) == 1:
                prod = Produto.query.get(itens[0].produto_id)
                resumo_produtos = prod.nome if prod else "Produto Excluído"
            elif len(itens) > 1:
                resumo_produtos = f"{len(itens)} itens variados"
            else:
                resumo_produtos = "Nenhum item"

            lista_ultimas_vendas.append({
                "id": v.id,
                "produto_resumo": resumo_produtos,
                "valor_total": v.valor_total,
                "data_venda": v.data_venda.strftime('%d/%m/%Y %H:%M')
            })

        return {
            "total_produtos": total_produtos,
            "valor_estoque": round(valor_estoque, 2),
            "total_vendas_rs": round(total_vendas_rs, 2),
            "total_itens_vendidos": total_itens_vendidos,
            "ultimas_vendas": lista_ultimas_vendas
        }
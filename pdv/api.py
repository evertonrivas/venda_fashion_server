from flask import Blueprint
from flask_restx import Api
from pdv.consumer import api as ns_consumer
from pdv.consumer import apis as ns_consumer_group


""" Módulo Ponto De Venda (Gestão de Força de Vendas). 
    Módulo para frente de loja onde realiza:
    - Gestão de Cadastros
        - Fornecedores
        - Clientes
        - Bancos
        - Templates de e-mail
    - Importação de NF compra
    - Venda de Produtos
        - Aplicação de Desconto
        - Cupom de Desconto (Parcerias)
        - Itens Express
        - Gestão de Trocas de produtos
        - Infos de Clientes (última compra, ticket médio)
        - Abertura e Fechamento de Caixa
        - Apontamento de retirada do Caixa
        - Gestão de promoções (por prazo, por item, por categoria de produto)
    - Emissão de NF (venda e devolução) - parceiro bling
    - Gestão de Produtos
        - Cadastro
        - Composição
        - Importação e exportação
    - Gestão de Pedidos
    - Gestão de Contas a Pagar
    - Gestão de Estoques
        - Ajuste
        - Inventário
        - Sugestão de Pedido (catgoria de produto, linha, marca)
    - Fluxo de Caixa
        - Importar extrato bancario
    

Keyword arguments: vendas, b2c, produtos, consumidor, 
"""

nss = [ns_consumer,ns_consumer_group]

blueprint = Blueprint("pdv",__name__,url_prefix="/pdv/api/v1/")

api = Api(blueprint,
    version="1.0",
    title="API Venda Fashion",
    description="Uma API REST para sistema de vendas - Módulo PDV",
    contact_email="evertonrivas@gmail.com",
    contact="Venda",
    contact_url="http://www.vendafashion.com")

for ns in nss:
    api.add_namespace(ns)
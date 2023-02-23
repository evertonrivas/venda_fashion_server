from http import HTTPStatus
from flask import request
from flask_restx import Resource,Namespace,fields
from models import B2bTablePrice,B2bTablePriceProduct,db
import sqlalchemy as sa

ns_price = Namespace("price-table",description="Operações para manipular dados de tabelas de preços")

prc_pag_model = ns_price.model(
    "Pagination",{
        "registers": fields.Integer,
        "page": fields.Integer,
        "per_page": fields.Integer,
        "pages": fields.Integer,
        "has_next": fields.Boolean
    }
)

prc_prod_model = ns_price.model(
    "Products",{
        "id_product": fields.Integer,
        "stock_quantity": fields.Integer,
        "price": fields.Fixed,
        "price_retail": fields.Fixed
    }
)

prc_model = ns_price.model(
    "TablePrice",{
        "id": fields.Integer,
        "name": fields.String,
        "start_date": fields.DateTime,
        "end_date": fields.DateTime,
        "active": fields.Boolean,
        "products": fields.List(fields.Nested(prc_prod_model))
    }
)

prc_return = ns_price.model(
    "TablePriceReturn",{
        "pagination": fields.Nested(prc_pag_model),
        "data": fields.List(fields.Nested(prc_model))
    }
)

@ns_price.route("/")
class PriceTableList(Resource):
    @ns_price.response(HTTPStatus.OK.value,"Obtem a listagem de pedidos",prc_return)
    @ns_price.response(HTTPStatus.BAD_REQUEST.value,"Falha ao listar registros!")
    @ns_price.param("page","Número da página de registros","query",type=int,required=True)
    @ns_price.param("pageSize","Número de registros por página","query",type=int,required=True,default=25)
    @ns_price.param("query","Texto para busca","query")
    def get(self):
        pag_num  =  1 if request.args.get("page")!=None else int(request.args.get("page"))
        pag_size = 25 if request.args.get("pageSize")!=None else int(request.args.get("pageSize"))
        search   = "" if request.args.get("query")!=None else "{}%".format(request.args.get("query"))

        if search!=None:
            rquery = B2bTablePrice.query.filter(sa.and_(B2bTablePrice.active==True,B2bTablePrice.name.like(search))).paginate(page=pag_num,per_page=pag_size)
        else:
            rquery = B2bTablePrice.query.filter(B2bTablePrice.active==True).paginate(page=pag_num,per_page=pag_size)

        return {
            "pagination":{
                "registers": rquery.total,
                "page": pag_num,
                "per_page": pag_size,
                "pages": rquery.pages,
                "has_next": rquery.has_next
            },
            "data":[{
                "id": m.id,
                "name": m.name,
                "start_date": m.start_date,
                "end_date": m.end_date,
                "active": m.active,
                "products": self.get_products(m.id)
            }for m in rquery.items]
        }
    
    def get_products(self,id:int):
        rquery = B2bTablePriceProduct.query.filter(B2bTablePriceProduct.id_table_price==id)
        return [{
            "id_product": m.id_product,
            "stock_quantity": m.stock_quantity,
            "price": m.price,
            "price_retail": m.price_retail
        }for m in rquery.items]

    @ns_price.response(HTTPStatus.OK.value,"Cria um novo pedido")
    @ns_price.response(HTTPStatus.BAD_REQUEST.value,"Falha ao criar pedido!")
    @ns_price.doc(body=prc_model)
    def post(self)->int:
        return 0

@ns_price.route("/<int:id>")
@ns_price.param("id","Id do registro")
class PriceTableApi(Resource):
    
    @ns_price.response(HTTPStatus.OK.value,"Obtem os dados de um carrinho")
    @ns_price.response(HTTPStatus.BAD_REQUEST.value,"Registro não encontrado!")
    def get(self,id:int):
        rquery = B2bTablePrice.query.get(id)
        squery = B2bTablePriceProduct.query.find(B2bTablePriceProduct.id_table_price==id)
        return {
            "id": rquery.id,
            "name": rquery.name,
            "start_date": rquery.start_date.strftime("%Y-%m-%d %H:%M:%S"),
            "end_date": rquery.end_date.strftime("%Y-%m-%d %H:%M:%S"),
            "active": rquery.active,
            "date_created": rquery.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            "date_updated": rquery.date_updated.strftime("%Y-%m-%d %H:%M:%S"),
            "products": [{
                "id_product": m.id_product,
                "stock_quantity": m.stock_quantity,
                "price": m.price,
                "price_retail": m.price_retail
            }for m in squery.items]
        }
    
    @ns_price.response(HTTPStatus.OK.value,"Atualiza os dados de um pedido")
    @ns_price.response(HTTPStatus.BAD_REQUEST.value,"Registro não encontrado!")
    @ns_price.doc(body=prc_model)
    def post(self,id:int)->bool:
        try:
            req = request.get_json()
            price = B2bTablePrice.query.get(id)
            price.name       = price.name if req.name==None else req.name
            price.start_date = price.start_date if req.start_date==None else req.start_date
            price.end_date   = price.end_date if req.end_date==None else req.end_date
            price.active     = price.active   if req.active==None else req.active
            db.session.commit()
            return True
        except:
            return False

    @ns_price.response(HTTPStatus.OK.value,"Exclui os dados de um carrinho")
    @ns_price.response(HTTPStatus.BAD_REQUEST.value,"Registro não encontrado!")
    def delete(self,id:int)->bool:
        try:
            price = B2bTablePrice.query.get(id)
            price.active = False
            db.session.commit()
            return True
        except:
            return False
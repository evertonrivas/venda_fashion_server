from http import HTTPStatus
from flask_restx import Resource,Namespace,fields
from flask import request
from models import B2bBrand,db
import json
from sqlalchemy import exc,and_,asc,desc
from auth import auth
from config import Config

ns_brand = Namespace("brand",description="Operações para manipular dados de marcas")

brand_pag_model = ns_brand.model(
    "Pagination",{
        "registers": fields.Integer,
        "page": fields.Integer,
        "per_page": fields.Integer,
        "pages": fields.Integer,
        "has_next": fields.Integer
    }
)

brand_model = ns_brand.model(
    "Brand",{
        "id": fields.Integer,
        "name": fields.String
    }
)

brand_return = ns_brand.model(
    "BrandReturn",{
        "pagination": fields.Nested(brand_pag_model),
        "data": fields.List(fields.Nested(brand_model))
    }
)

@ns_brand.route("/")
class CollectionList(Resource):
    @ns_brand.response(HTTPStatus.OK.value,"Obtem um registro de uma coleção",brand_return)
    @ns_brand.response(HTTPStatus.BAD_REQUEST.value,"Registro não encontrado!")
    @ns_brand.param("page","Número da página de registros","query",type=int,required=True)
    @ns_brand.param("pageSize","Número de registros por página","query",type=int,required=True,default=25)
    @ns_brand.param("query","Texto para busca","query")
    @ns_brand.param("list_all","Ignora as paginas e lista todos os registros",type=bool,default=False)
    @ns_brand.param("order_by","Campo de ordenacao","query")
    @ns_brand.param("order_dir","Direção da ordenação","query",enum=['ASC','DESC'])
    @auth.login_required
    def get(self):
        pag_num  =  1 if request.args.get("page") is None else int(request.args.get("page"))
        pag_size = Config.PAGINATION_SIZE.value if request.args.get("pageSize") is None else int(request.args.get("pageSize"))
        search   = "" if request.args.get("query") is None else "{}%".format(request.args.get("query"))
        list_all = False if request.args.get("list_all") is None else True
        order_by = "name" if request.args.get("order_by") is None else request.args.get("order_by")
        direction = asc if request.args.get("order_dir") == 'ASC' else desc

        try:
            if search=="":
                rquery = B2bBrand\
                    .query\
                    .filter(B2bBrand.trash == False)\
                    .order_by(direction(getattr(B2bBrand,order_by)))
                
            else:
                rquery = B2bBrand\
                    .query\
                    .filter(and_(B2bBrand.trash == False,B2bBrand.name.like(search)))\
                    .order_by(direction(getattr(B2bBrand,order_by)))

            if list_all==False:
                rquery = rquery.paginate(page=pag_num,per_page=pag_size)

                retorno = {
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
                        "date_created": m.date_created.strftime("%Y-%m-%d %H:%M:%S"),
                        "date_updated": m.date_updated.strftime("%Y-%m-%d %H:%M:%S") if m.date_updated!=None else None
                    } for m in rquery.items]
                }
            else:
                retorno = [{
                        "id":m.id,
                        "name":m.name,
                        "date_created": m.date_created.strftime("%Y-%m-%d %H:%M:%S"),
                        "date_updated": m.date_updated.strftime("%Y-%m-%d %H:%M:%S") if m.date_updated!=None else None
                    } for m in rquery]
            return retorno
        except exc.SQLAlchemyError as e:
            return {
                "error_code": e.code,
                "error_details": e._message(),
                "error_sql": e._sql_message()
            }

    @ns_brand.response(HTTPStatus.OK.value,"Cria uma nova coleção")
    @ns_brand.response(HTTPStatus.BAD_REQUEST.value,"Falha ao criar registro!")
    @ns_brand.doc(body=brand_model)
    @auth.login_required
    def post(self)->int:
        try:
            req = json.dumps(request.get_json())
            col = ns_brand()
            col.name = req.name
            db.session.add(col)
            db.session.commit()

            return col.id
        except exc.SQLAlchemyError as e:
            return {
                "error_code": e.code,
                "error_details": e._message(),
                "error_sql": e._sql_message()
            }

@ns_brand.route("/<int:id>")
@ns_brand.param("id","Id do registro")
class CollectionApi(Resource):
    @ns_brand.response(HTTPStatus.OK.value,"Retorna os dados dados de uma coleção")
    @ns_brand.response(HTTPStatus.BAD_REQUEST.value,"Registro não encontrado!")
    @auth.login_required
    def get(self,id:int):
        try:
            cquery = ns_brand.query.get(id)

            return {
                "id": cquery.id,
                "name": cquery.name,
                "date_created": cquery.date_created.strftime("%Y-%m-%d %H:%M:%S"),
                "date_updated": cquery.date_updated.strftime("%Y-%m-%d %H:%M:%S") if cquery.date_updated!=None else None
            }
        except exc.SQLAlchemyError as e:
            return {
                "error_code": e.code,
                "error_details": e._message(),
                "error_sql": e._sql_message()
            }
    
    @ns_brand.response(HTTPStatus.OK.value,"Atualiza os dados de uma coleção")
    @ns_brand.response(HTTPStatus.BAD_REQUEST.value,"Registro não encontrado!")
    @ns_brand.doc(body=brand_model)
    @auth.login_required
    def post(self,id:int)->bool:
        try:
            req = json.dumps(request.get_json())
            col = B2bBrand.query.get(id)
            col.name          = col.name if req.name is None else req.name
            col.trash         = col.trash if req.trash is None else req.trash
            db.session.commit()

            return True
        except exc.SQLAlchemyError as e:
            return {
                "error_code": e.code,
                "error_details": e._message(),
                "error_sql": e._sql_message()
            }
    
    @ns_brand.response(HTTPStatus.OK.value,"Exclui os dados de uma coleção")
    @ns_brand.response(HTTPStatus.BAD_REQUEST.value,"Registro não encontrado!")
    @auth.login_required
    def delete(self,id:int)->bool:
        try:
            grp = B2bBrand.query.get(id)
            grp.trash = True
            db.session.commit()
            return True
        except exc.SQLAlchemyError as e:
            return {
                "error_code": e.code,
                "error_details": e._message(),
                "error_sql": e._sql_message()
            }
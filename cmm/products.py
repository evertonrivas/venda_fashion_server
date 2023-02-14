from http import HTTPStatus
from typing import TypedDict
from flask_restx import Resource,fields,Namespace
from flask import request

api = Namespace("products",description="Operações para manipular dados de produtos")
apig = Namespace("products-grid",description="Operações para manipular dados das grades de produtos")

#API Models
sku_model = api.model(
    "sku",{
        "color": fields.String,
        "size": fields.Integer
    }
)

prod_model = api.model(
    "Product",{
        "id": fields.Integer,
        "idcategory": fields.Integer,
        "prodCode": fields.String,
        "barCode": fields.String,
        "refCode": fields.String,
        "name": fields.String,
        "description": fields.String,
        "observation": fields.String,
        "ncm": fields.String,
        "image": fields.String,
        "price": fields.Float,
        "measure_unit": fields.String,
        "structure": fields.String,
        "sku": fields.List(fields.Nested(sku_model))
    }
)


class ProductSku(TypedDict):
    color:str
    size: str

class Product(TypedDict):
    id:int
    prodCode:str
    barCode:str
    refCode:str
    name:str
    description:str
    observation:str
    ncm:str
    image:str
    price:float
    measure_unit:str
    structure:str
    sku:list[ProductSku]


####################################################################################
#                INICIO DAS CLASSES QUE IRAO TRATAR OS PRODUTOS.                   #
####################################################################################
@api.route("/")
class ProductsList(Resource):
    @api.response(HTTPStatus.OK.value,"Obtem a listagem de produto",[prod_model])
    @api.response(HTTPStatus.BAD_REQUEST.value,"Falha ao listar registros!")
    @api.param("page","Número da página de registros","query",type=int,required=True)
    @api.doc(description="Teste de documentacao")
    def get(self)-> list[Product]:

        return [{
            "id":request.args.get("page"),
            "prodCode": "10",
            "barCode": "7890000000000",
            "refCode": "BZ10",
            "name": "CALCA JEANS",
            "description": "CALCAS",
            "observation": "nada",
            "ncm": "10000",
            "image": "https://...",
            "price": 107.00,
            "measure_unit": "UN",
            "structure": "S",
            "sku":[{
                "color": "#FFFFFF",
                "size": "P"
            },
            {
                "color": "#FFFFFF",
                "size": "M"
            }]
        }]

    @api.response(HTTPStatus.OK.value,"Cria um novo produto no sistema")
    @api.response(HTTPStatus.BAD_REQUEST.value,"Falha ao criar novo produto!")
    @api.doc(parser=prod_model)
    def post(self)->bool:
        return False


@api.route("/<int:id>")
@api.param("id","Id do registro")
class ProductApi(Resource):

    @api.response(HTTPStatus.OK.value,"Obtem um registro de produto",prod_model)
    @api.response(HTTPStatus.BAD_REQUEST.value,"Registro não encontrado")
    def get(self,id:int)->Product:
        return None

    @api.doc(parser=prod_model)
    @api.response(HTTPStatus.OK.value,"Salva dados de um produto")
    @api.response(HTTPStatus.BAD_REQUEST.value,"Registro não encontrado")
    def post(self,id:int)->bool:
        return False
    
    @api.response(HTTPStatus.OK.value,"Exclui os dados de um produto")
    @api.response(HTTPStatus.BAD_REQUEST.value,"Registro não encontrado")
    def delete(self,id:int)->bool:
        return False

####################################################################################
#           INICIO DAS CLASSES QUE IRAO TRATAR AS GRADES DE  PRODUTOS.             #
####################################################################################

dist_model = apig.model(
    "GridDistribution",{
        "size": fields.Integer,
        "color": fields.String,
        "value": fields.Float,
        "is_percent":fields.Boolean
    }
)

grid_model = apig.model(
    "Grid",{
        "id":fields.Integer,
        "name": fields.String,
        "distribution": fields.List(fields.Nested(dist_model))
    }
)

class GridDist(TypedDict):
    size:str
    color:str
    value:float
    is_percent:bool

class Grid(TypedDict):
    id:int
    name:str
    distribution:list[GridDist]


@apig.route("/")
class GridList(Resource):

    @apig.response(HTTPStatus.OK.value,"Obtem os registros de grades existentes",[grid_model])
    @apig.response(HTTPStatus.BAD_REQUEST.value,"Falha ao listar registros!")
    @api.param("page","Número da página de registros","query",type=int,required=True)
    def get(self)->list[Grid]:

        return [{
            "id": request.args.get("page"),
            "name": "Grade 1",
            "distribution": [{
                "size": "G",
                "color": "#000000",
                "value": 10,
                "is_Percent": True
            }]
        }]

    @apig.response(HTTPStatus.OK.value,"Cria uma nova grade no sistema")
    @apig.response(HTTPStatus.BAD_REQUEST.value,"Falha ao criar nova grade!")
    @apig.doc(parser=grid_model)
    def post(self)->int:

        return 0


@apig.route("/<int:id>")
class Grid(Resource):
    @apig.response(HTTPStatus.OK.value,"Obtem um registro de uma grade",grid_model)
    @apig.response(HTTPStatus.BAD_REQUEST.value,"Registro não encontrado!")
    def get(self,id:int)->Product:

        return None

    @apig.doc(parser=prod_model)
    @apig.response(HTTPStatus.OK.value,"Salva dados de uma grade")
    @apig.response(HTTPStatus.BAD_REQUEST.value,"Registro não encontrado!")
    def post(self,id:int)->bool:

        return False
    
    @apig.response(HTTPStatus.OK.value,"Exclui os dados de uma grade")
    @apig.response(HTTPStatus.BAD_REQUEST.value,"Registro não encontrado!")
    def delete(self,id:int)->bool:

        return False